import sys
import socket
from time import time
from binascii import unhexlify

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Addr = "jeangourd.com"
Port = 31337
Zero = 0.025 # time to be  a zero 
One = 0.09 #time to be a one
Bits = 8 # ASCII mode


s.connect((Addr, Port))
convert_bin = ""
data = s.recv(4096)

while (data.rstrip("\n") != "EOF"):
	sys.stdout.write(data)
	sys.stdout.flush()
	t0 = time()
	data = s.recv(4096)
	t1 = time()
	delta = round(t1 - t0, 3)
	if (delta >= One):
		convert_bin += "1"
	else:
		convert_bin += "0"
s.close()

i = 0
msg = ""
while (i < len(convert_bin)):
	#Step through on byte at a time
	b = convert_bin[i:i + Bits]
	# Convert the byte to ascii
	n = int("0b{}".format(b), 2)
	try:
		msg += unhexlify("{0:x}".format(n))
	except TypeError:
		msg += "?"
	i += Bits
#print ("Hidden message: \"{}\"".format(msg[:msg.index("EOF")]))
print ("Hidden message: \"{}\"".format(msg))
