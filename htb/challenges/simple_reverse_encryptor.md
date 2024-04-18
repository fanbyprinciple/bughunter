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