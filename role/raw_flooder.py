from role import flooder


class RAWFlooder(flooder.Flooder):
	def __init__(self, ip, port):
		flooder.Flooder.__init__(self, ip, port)
		self.socket_type = 3
		self.socket_protocol = 255

	def run(self):
		exit()
