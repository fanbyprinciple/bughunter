![](2024-04-22-15-06-33.png)


```python
import json
from Crypto.Util.number import long_to_bytes
from pwn import *
from sympy.ntheory.modular import crt
from sympy.simplify.simplify import nthroot

conn = remote('209.97.185.157', 32141)
rem = list()
num = list()
for i in range(3):
    conn.sendline(b'Y')
    a = conn.recvline()
    r = json.loads(a[74:-1].decode())
    m = r['time_capsule']
    n = r['pubkey'][0]
    e = 5
    m = int(m, 16)
    n = int(n, 16)
    rem.append(m)
    num.append(n)

x = crt(num, rem, check=True)
# print(f'x = {x[0]}')
flag = nthroot(x[0], 5)
print(flag)
print(long_to_bytes(flag))

conn.sendline(b'N')
conn.recvline()
conn.close()
```