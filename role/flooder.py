import random


class Flooder:
	def __init__(self, ip, port):
		# Connection
		self.ip = ip
		self.port = port

		# Socket
		self.socket_type = 1
		self.socket_protocol = 0
		self.socket_options = {}

		# Packet
		self.packet_size = 256

	def get_random_message(self):
		return random._urandom(int(self.packet_size))

	@staticmethod
	def checksum(msg):
		s = 0
		for i in range(0, len(msg), 2):
			w = msg[i] + (msg[i+1]) << 8
			s += w

		s = (s >> 16) + (s & 0xffff)
		s += (s >> 16)

		s = ~s & 0xffff

		return s
