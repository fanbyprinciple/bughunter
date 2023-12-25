#include <stdio.h>
#include <stdlib.h>

int main(void) {
    typedef unsigned char byte;
    FILE *f;
    size_t flagSize;
    byte *flag;
    unsigned int seed;
    long i;
    int rnd1, rnd2;

    f = fopen("flag.enc", "rb");
    // seek until the end of the file to get the size
    fseek(f, 0, SEEK_END);
    flagSize = ftell(f);
    // seek to the beginning
    fseek(f, 0, SEEK_SET);
    // allocate memory of the flag
    flag = malloc(flagSize);
    fread(flag, 1, flagSize, f);
    fclose(f);

    // take seed from the first 4 bytes
    int flagOffset = 4;
    memcpy(&seed, flag, flagOffset);
    srand(seed);

    for(i = flagOffset; i < (long)flagSize; i++) {
        rnd1 = rand();
        rnd2 = rand();
        rnd2 = rnd2 & 7;
        flag[i]  = 
            flag[i] >> rnd2 |
            flag[i] << 8 - rnd2;
        flag[i] = rnd1 ^ flag[i];
        printf("%c", flag[i]);
    }
}