from Crypto.Util.number import getStrongPrime, isPrime, inverse, bytes_to_long
FLAG = open('flag.txt', 'r').read()

while True:
    p = getStrongPrime(512)
    q = 2*p + 1
    if (isPrime(q)):
        break

n = p*q
phi = (p-1)*(q-1)
e = 0x10001
d = inverse(e, phi)

pt = bytes_to_long(FLAG.encode())
ct = pow(pt,e,n)

open('output.txt', 'w').write(f'e: {e}\nd: {d}\nphi: {phi}\nct: {ct}')