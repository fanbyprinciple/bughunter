https://book.hacktricks.xyz/crypto-and-stego/crypto-ctfs-tricks

Esoteric chaaallenges solver

http://esolangpark.vercel.app/ide/chef

+-- all comes undeeer esoteric

solving encryption challegne

Cryptography
1) Time Traveler
We have two stages of encryption:
Stage 1: Encryption based on a random permutation of [0, 8).
Stage 2: The current time is used as a seed and appended to the encrypted message.
Perform a XOR operation with 0x42 to get the final byte array.
We can decrypt using the following method:
To recover the time, simply get the last 18 bytes of your output and perform a XOR
operation with with 0x42.
Feed this time to Stage 2 to obtain the encrypted message from Stage 1 (removing the
last 18 characters, since the time is unrelated to the original message)
Reverse the encryption in stage 1 by brute-forcing the key with 8! permutations

# cypher quest

flag.ec chall.py

# rsa cracker 

output.txt gen.py

# chef programming language

dcode.fr

# musical notes



