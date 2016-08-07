from struct import pack
from random import _urandom
from array import array


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
		self.random_bytes = 120

	def get_random_message(self):
		return _urandom(int(self.random_bytes))

	if pack("H", 1) == "\x00\x01":  # big endian
		@staticmethod
		def checksum(pkt):
			if len(pkt) % 2 == 1:
				pkt += bytes("\0".encode('utf-8'))
			s = sum(array("H", pkt))
			s = (s >> 16) + (s & 0xffff)
			s += s >> 16
			s = ~s
			return s & 0xffff
	else:
		@staticmethod
		def checksum(pkt):
			if len(pkt) % 2 == 1:
				pkt += bytes("\0".encode('utf-8'))
			s = sum(array("H", pkt))
			s = (s >> 16) + (s & 0xffff)
			s += s >> 16
			s = ~s
			return (((s >> 8) & 0xff) | s << 8) & 0xffff
