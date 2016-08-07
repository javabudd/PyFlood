from role import flooder


class UDPFlooder(flooder.Flooder):
	def __init__(self, ip, port):
		flooder.Flooder.__init__(self, ip, port)
		self.socket_type = 2
		self.socket_protocol = 17

	def run(self):
		exit()