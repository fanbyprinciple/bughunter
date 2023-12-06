import subprocess

# Replace this with the path to your binary
binary_path = "./S0lv3M3"

# Function to execute the binary with a given parameter
def execute_binary(parameter):
    try:
        # Execute the binary with the parameter
        result = subprocess.run([binary_path, parameter], capture_output=True, text=True, check=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr

# Loop to increase the number of 'a's up to 1000
for i in range(100000, 100000000):
    print(i)
    parameter = 'a' * i
    stdout, stderr = execute_binary(parameter)

    # print(stdout, stderr)
    # Check if 'flag' is in the output
    if 'INCORRECT' not in stdout or 'flag' in stderr:
        print(f"Found 'flag' with parameter '{parameter}':")
        print(stdout)
        break
else:
    print("Flag not found in any of the outputs.")

if ( argc == 2 )
  {
    s = (char *)argv[1];
    if ( strlen(s) == 25
      && s[3] - s[4] + s[1] * s[5] - s[6] + s[2] == 8450
      && s[3] * s[5] + s[6] + s[2] - s[4] * s[7] == -2396
      && s[6] + s[4] + s[8] * s[5] - s[7] + s[3] == 4169
      && s[4] - s[5] - s[8] + s[6] * s[7] - s[9] == 4266
      && s[7] + s[9] + s[8] * s[6] - s[10] + s[5] == 2784
      && s[6] - s[10] + s[8] + s[9] * s[7] - s[11] == 9757
      && s[7] + s[10] + s[12] * s[9] - s[8] + s[11] == 5656
      && s[11] + s[8] - s[12] * s[13] - s[9] - s[10] == -3848
      && s[9] * s[11] * s[14] + s[13] - s[12] * s[10] == 475686
      && s[10] * s[14] + s[11] * s[15] * s[13] * s[12] == 10520562
      && s[11] + s[13] - s[14] - s[16] * s[12] - s[15] == -4558
      && s[17] * s[13] * s[16] + s[15] * s[12] * s[14] == 594828
      && s[13] + s[17] + s[14] + s[15] - s[16] - s[18] == 118
      && s[16] + s[14] + s[18] - s[17] * s[19] - s[15] == -4474
      && s[17] + s[19] + s[16] + s[18] * s[20] + s[15] == 2786
      && s[20] * s[21] - s[17] - s[16] + s[19] * s[18] == 8910
      && s[19] + s[21] - s[18] * s[20] - s[17] + s[22] == -2287
      && s[21] * s[18] * s[19] + s[20] - s[23] * s[22] == 393581
      && s[22] - s[20] - s[21] + s[19] - s[23] * s[24] == -9975 )
    {
   