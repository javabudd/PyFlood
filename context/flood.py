from role import raw_flooder
from role import udp_flooder
from role import tcp_flooder
from multiprocessing import Process


class Flood(Process):
	UDP = 1
	TCP = 2
	RAW = 3

	types = {
		UDP: udp_flooder.UDPFlooder,
		TCP: tcp_flooder.TCPFlooder,
		RAW: raw_flooder.RAWFlooder
	}

	def __init__(self, ip, port, flood_type):
		Process.__init__(self)
		self.ip = ip
		self.port = port
		self.flood_type = flood_type

	def run(self):
		flooder = self.types.get(self.flood_type)(self.ip, self.port)
		flooder.run()

	@classmethod
	def get_list(cls):
		return cls.types
