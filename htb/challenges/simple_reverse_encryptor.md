```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{

 /*
 * creating a file object to load in the encrypted flag.
 * if successful, fp will point to the start of the file
 * object.
 **/

 FILE *fp = fopen("flag.enc", "rb");         
 
 if (fp != NULL)
 {

  /*
  * mimicking the sequence of function calls in the
  * assembly. 
  * 
  * 1. fseek() moves the file pointer to the
  *   of the file. 
  * 2. ftell() returns the size of the file
  *    and we store it in a long (32-bit value) called
  *    size. 
  * 3. rewind(fp) moves the file pointer to the
  *    beginning of the file. 
  * 4. we dynamically allocate memory on the heap via 
  *    malloc() with size as an argument. we set the 
  *    data type to char, as they're a byte in size. 
  *  we do the same check for a nullptr as above.
  *
  **/

  fseek(fp, 0, SEEK_END);
  long size = ftell(fp);
  rewind(fp);

  char *fileContents = malloc(size);
  
  if (fileContents != NULL)
  {

   /*
   * reading the file into our dynamically allocated memory.
   * afterwards, we print out the contents in hex to compare 
   * to our hexdump. this is just making sure the file was
   * read into our program correctly.
   *
   * thereafter we make an int called seed. we use memcpy
   * to copy the first 32 bits of data (the size of an int) from
   * our allocated memory into the seed variable. then we print it
   * and load into into srand(), followed by initializing our
   * two random numbers.
   * 
   **/ 

   fread(fileContents, sizeof(char), size, fp);
   
   for (int i = 0; i < size; i++)
   {
    printf("%02X", fileContents[i]);
   }
   printf("\n\n");

   int seed;
   memcpy(&seed, fileContents, sizeof(seed));
   printf("Seed: %d\n", seed);

   srand(seed);
   int rand1, rand2;

   for (int i = 4; i < size; i++)
   {

   /*
   * starting at the 5th byte and going until the end, we set our 
   * random numbers accordingly. we print out the byte we're working
   * with and the two random numbers. then we do our right shift followed
   * by our XOR, and print out the final byte. i pause the program before
   * doing the next iteration just for debugging purposes.
   *
   **/

    rand1 = rand();
    rand2 = rand() & 7;

    printf("current byte: %02X\n", fileContents[i]);
    printf("right shift: %d\n", rand2);
    printf("XOR key: %d\n", rand1);

    fileContents[i]  = ((unsigned char)fileContents[i] >> (rand2)) | ((fileContents[i]) << (8 - rand2));
    printf("byte after rotate right: %02X\n", fileContents[i]);

    fileContents[i] = rand1 ^ fileContents[i];
    
    printf("byte after full decryption: %02X\n", fileContents[i]);
    getchar();   
   }

   /*
   * finally, this loop will just print the flag out.
   **/

   for (int i = 4; i < size; i++)
   {
    printf("%c", fileContents[i]);
   }
  
  }
  
  free(fileContents);
  fclose(fp); 
 }

return 0;
}

```


Search
Write
Sign up

Sign in



HackTheBox — Simple Encryptor Write Up
southbre
southbre

·
Follow

8 min read
·
Apr 20, 2023
--


1



prompt:


brief:

so this is a “challenge” hosted on HackTheBox; a standalone activity that can be done without an internet connection. you only need the file(s) provided to you, which in this case is an 64-bit ELF executable which encrypts files, and a file containing our flag, which was run through the encryptor, so we unfortunately can’t see it.

when we try running the binary, we get an error: “No such file or directory: flag”. furthermore, when we run strings, we don’t see anything of note other than some C functions for writing and reading to files, and the strings “flag” and “flag.enc”

overview of some C functions

so, we see what’s happening underneath the hood with IDA. i was unfamiliar with a lot of the C code here as my programming experience to date has been exclusively python and C++. nonetheless, google exists, so here’s a breakdown of each of the commands we see:

FILE *fopen(const char *filename, const char *mode)

evidently this one just opens up a file. two arguments: one the file to be opened, and second the mode (typically read, write). you’ll see later that when we write some code to reverse the encryption algorithm, we store the return value in a pointer to a FILE object, which will point to the beginning of the file.
int fseek(FILE *stream, long int offset, int whence)

this one moves the file pointer of an opened file to a particular location. this can be helpful if we wanted to access a particular part of our file.
long int ftell(FILE *stream)

in the context of this program, ftell() is used to return the size of the file.
void *malloc(size_t size)

this is effectively “new” but in C. all this does is allocate memory on the program heap. if you’re unfamiliar, every program contains a block of memory known as the heap for holding variables that will be consistently used throughout a program’s runtime. the “antithesis” of the heap, if we’d go as far to consider them opposites, is the stack, which is stores variables and data that are local to whatever function is currently being executed. the takeaway here is stack memory doesn’t persist, heap memory does.
size_t fread(void *ptr, size_t size, size_t nmemb, FILE *stream)

let’s break down the arguments.

void *ptr: this is where the read data will be stored.
size_t size: this is how big each chunk of read data is going to be, the measurement being in bytes. for example, if we wanted to read the file a byte at a time, we’d set this to 1.
size_t nmemb: this is the amount of chunks to be read. so if size was set to 1, and nmemb is set to 2, then 2 bytes will be read into memory pointed to by *ptr
FILE *stream: lastly, this is the file that we’re reading from.
time_t time(time_t *t)

time() returns a 32-bit number containing the number of seconds that have passed since midnight, january 1st, 1970. this is the UNIX epoch, a fancy way of saying this is the arbitrary point in time from when UNIX operating systems begin measuring time. in my brief research, this is a borderline randomly chosen time.
void srand(unsigned int seed)

CTFs for some reason love using rand(), and for good reason. but i’ll elaborate below. while rand() generates a “random” number, srand takes in an integer as an argument, and any future number generated by rand() will use this seed as the base of it’s number generation.
int rand(void)

so the reason i say rand() is good for (simple) CTFs is because the algorithm it uses for generating a number isn’t really random. you can easily find it online. any call to rand() returns a not-really-random number that was created with the assistance of the seed provided in srand (though i’m pretty sure rand() can exist by itself).
IDA:

the main() function starts at 0x0000000000001289. the binary can be broken down into 4 steps:

file contents being read
creating the seed for rand()
the encryption algorithm
writing to flag.enc
file contents being read

the first thing we see is the binary opening up a file, “flag” with the mode “read bytes” (rb). this is presumably the original flag file. next, fseek() is called with the SEEK_END flag, so this file pointer will be placed at the very end of the file. ftell() is called, giving us the size of the file and it’s stored into the local variable at [rbp-20h]. soon after, this local variable is pushed as an argument for malloc(), so there’s a block of memory being created on the heap that is the same size as the file, “flag.” next, we see the entire file being read into the allocated memory space.


creating the seed for rand()

after the file is closed, we see time being called, which returns a 32-bit number containing the amount of seconds since the UNIX epoch, as previously discussed. this is store in a local variable at [rbp-38h] and thereafter pushed as an argument for srand().

the encryption algorithm

see the screenshot below containing the line by line description for the algorithm. but, basically, rand() is called and the lowest 8 bits are stored in the ecx register (movzx ecx, al; where movzx means “move with zero extend” which will fill the highest 24-bits of the register with zeros). the file is read one byte at a time, known because of the “movzx eax, byte ptr [rax]” performed at the beginning of each iteration, which just moves a byte of the memory pointed to by rax into eax (the lowest 32-bits of the same register). an XOR is performed between the random 8 digit number and the byte from the file.

afterwards, rand() is called again, the result of which undergoes an AND operation with the number 7, which is 111 in binary. some knowledge of boolean algebra will inform you that anything “AND 1” is itself, and anything “AND 0” is 0. essentially, we’re filling the register with 0s with the exception of the lowest 3 bits, which will be the least significant digits in the randomly generated number.

the same byte of data that’s been XORed is then rotated left by the amount determined by the call to rand() & 7.

so in short, we go byte by byte, XOR the byte with a randomly generated 8 digit number, then rotate the data left by (rand() & 7) bits.


writing to flag.enc

once the whole file has been iterated through, we see a file being opened called “flag.enc”. the instruction at 0x00000000000013E5 is “lea rax, [rbp+seed]”. if we scroll back up to the local variable declarations in main, we can see that seed corresponds to [rbp-38h], which is storing the return from time. fwrite() is called in the following fashion:

fwrite(flagEncptr, 1, 4, seed)

meaning 4 bytes will the written at the beginning of flag.enc, containing the seed. afterwards, the rest of the encrypted flag will be written into flag.enc


reversing the encryption:

so first, let’s look at the hexdump of the file. when we’re reading in the file in our program later on, we can compare the result with our hexdump to make sure the bytes match.


below is the C code that reverses the encryption (with detailed documentation ofc). i initially wanted to patch the binary in a debugger, but that would’ve required way more knowledge in writing x64 assembly than i’m comfortable with. i hadn’t even considered writing a script initially, and when i did, i thought about doing so in python, however manipulating files is much easier and convenient using a lower-level language like C. additionally, the original code for the encryptor was clearly written in C, so makes sense in terms of consistency.

we can really just write the code by following the assembly, up until the encryption part. once we get there, we just switch the order of the XOR and the rotate, and reverse the direction of the rotate (so, in short, we’ll be rotating the bytes right, then performing an XOR with a randomly generated number).

one caveat to point out is that i initially tried doing this challenge on a mac, since i was confident there wouldn’t be too much of a difference being that we’re dealing with an ELF executable. when running the C code there, the first decrypted byte was 54 (“T”) as opposed to 48 (“H”). it’s helpful that the flag is in a familiar format, being “HTB{flag_content_here}” so we can know immediately when our output is wrong.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{

 /*
 * creating a file object to load in the encrypted flag.
 * if successful, fp will point to the start of the file
 * object.
 **/

 FILE *fp = fopen("flag.enc", "rb");         
 
 if (fp != NULL)
 {

  /*
  * mimicking the sequence of function calls in the
  * assembly. 
  * 
  * 1. fseek() moves the file pointer to the
  *   of the file. 
  * 2. ftell() returns the size of the file
  *    and we store it in a long (32-bit value) called
  *    size. 
  * 3. rewind(fp) moves the file pointer to the
  *    beginning of the file. 
  * 4. we dynamically allocate memory on the heap via 
  *    malloc() with size as an argument. we set the 
  *    data type to char, as they're a byte in size. 
  *  we do the same check for a nullptr as above.
  *
  **/

  fseek(fp, 0, SEEK_END);
  long size = ftell(fp);
  rewind(fp);

  char *fileContents = malloc(size);
  
  if (fileContents != NULL)
  {

   /*
   * reading the file into our dynamically allocated memory.
   * afterwards, we print out the contents in hex to compare 
   * to our hexdump. this is just making sure the file was
   * read into our program correctly.
   *
   * thereafter we make an int called seed. we use memcpy
   * to copy the first 32 bits of data (the size of an int) from
   * our allocated memory into the seed variable. then we print it
   * and load into into srand(), followed by initializing our
   * two random numbers.
   * 
   **/ 

   fread(fileContents, sizeof(char), size, fp);
   
   for (int i = 0; i < size; i++)
   {
    printf("%02X", fileContents[i]);
   }
   printf("\n\n");

   int seed;
   memcpy(&seed, fileContents, sizeof(seed));
   printf("Seed: %d\n", seed);

   srand(seed);
   int rand1, rand2;

   for (int i = 4; i < size; i++)
   {

   /*
   * starting at the 5th byte and going until the end, we set our 
   * random numbers accordingly. we print out the byte we're working
   * with and the two random numbers. then we do our right shift followed
   * by our XOR, and print out the final byte. i pause the program before
   * doing the next iteration just for debugging purposes.
   *
   **/

    rand1 = rand();
    rand2 = rand() & 7;

    printf("current byte: %02X\n", fileContents[i]);
    printf("right shift: %d\n", rand2);
    printf("XOR key: %d\n", rand1);

    fileContents[i]  = ((unsigned char)fileContents[i] >> (rand2)) | ((fileContents[i]) << (8 - rand2));
    printf("byte after rotate right: %02X\n", fileContents[i]);

    fileContents[i] = rand1 ^ fileContents[i];
    
    printf("byte after full decryption: %02X\n", fileContents[i]);
    getchar();   
   }

   /*
   * finally, this loop will just print the flag out.
   **/

   for (int i = 4; i < size; i++)
   {
    printf("%c", fileContents[i]);
   }
  
  }
  
  free(fileContents);
  fclose(fp); 
 }

return 0;
}
Reverse Engineering
--


1


southbre
Written by southbre
2 Followers
cs student. reverse engineer enthusiast. b-vitamin taker.

Follow

More from southbre
Indefinite — HackTheBox
southbre
southbre

Indefinite — HackTheBox
Today I decided to do a write-up on this one retired HackTheBox Challenge named “Indefinite”, whose prompt can be read above. As a…
18 min read
·
Nov 12, 2023
--

Bookstore — TryHackMe
southbre
southbre

Bookstore — TryHackMe
today we’re doing a write-up for bookstore, a box on TryHackMe which has you enumuerating a web server, abusing an insecure API containing…
14 min read
·
Apr 29, 2023
--

Practical Malware Analysis, Chapter 12 — Covert Launching Techniques
southbre
southbre

Practical Malware Analysis, Chapter 12 — Covert Launching Techniques
Today we’re doing a deep dive into the five malware samples provided by the lab at the end of chapter 12 in Practical Malware Analysis by…
16 min read
·
Feb 17, 2023
--

See all from southbre
Recommended from Medium
Lokibot Malware Unpacking Process & Analysis
_A|p
_A|p

Lokibot Malware Unpacking Process & Analysis
LokiBot is malware to steal sensitive information. I will analyze its unpacking process here.
11 min read
·
Nov 5, 2023
--

Hardware Hacking | HackTheBox Debugging Interface
B@dr
B@dr

Hardware Hacking | HackTheBox Debugging Interface
Hello Guys , Today we’re going to solve another hardware hacking challenge where we demonstrated an analysis of an archived file that was…
4 min read
·
Nov 30, 2023
--

Lists

Album artwork of Rod McKuen’s Season in the Sun.

Staff Picks
624 stories
·
906 saves



Stories to Help You Level-Up at Work
19 stories
·
566 saves



Self-Improvement 101
20 stories
·
1635 saves



Productivity 101
20 stories
·
1507 saves
GHIDRA TUTORIAL: USAGE
Zaid Khaishagi
Zaid Khaishagi

GHIDRA TUTORIAL: USAGE
This is a continuation of the Ghidra Tutorial series. In the previous article, we discussed what Ghidra is and what it is used for. We went…
18 min read
·
Jan 1, 2024
--

Decrypting the Mystery of MedusaLocker
Shayan Ahmed Khan
Shayan Ahmed Khan

Decrypting the Mystery of MedusaLocker
In this analysis, I will not cover the stage1 and stage2 of MedusaLocker which includes initial access using a maldoc and execution using a…
9 min read
·
Nov 13, 2023
--

Running Ghidra Debugger IN-VM
Olof Astrand
Olof Astrand

Running Ghidra Debugger IN-VM
Starting up ghidras debugger tool can be a bit confusing the first time you use it. Here I will go through how to do it first with a local…
4 min read
·
Jan 21, 2024
--

Practical Malware Analysis Ch.5 Labs
jon
jon

Practical Malware Analysis Ch.5 Labs
Analyze the malware found in the file Lab05–01.dll using only IDA Pro. The goal of this lab is to give you hands-on experience with IDA…
6 min read
·
Nov 3, 2023
--

See more recommendations
Help

Status

About

Careers

Blog

Privacy

Terms

Text to speech

Teams