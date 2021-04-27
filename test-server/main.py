import os
import time
import string
import random

try:
	server_port = os.environ["SERVER_PORT"]
	tests_amount = int(os.environ.get("TESTS_AMOUNT", 10))
	loop_period = int(os.environ.get("LOOP_PERIOD", 1))
except KeyError as e:
	raise KeyError("Server port was not found. Error: {}. Aborting tests".format(e))
except ValueError as e:
	raise ValueError("Key could not be parsed. Error: {}. Aborting tests".format(e))

letters = string.ascii_lowercase
for i in range(0, tests_amount):
	# generate random string
	random_string = ''.join(random.choice(letters)
	                        for j in range(10))

	# exec netcat in bash
	stream = os.popen(
		f"echo '{random_string}' | netcat server {server_port}")
	# access the stream from command line to get the server response
	output = stream.read().strip('\n')
	
	expected_result = f"Your Message has been received: b'{random_string}'"
	assert output == expected_result, f"output should be '{expected_result}' but it is '{output}'"
	
	print(f"Test {i + 1} of {tests_amount} passed successfully")
	time.sleep(loop_period)

print("Tests passed successfully")

