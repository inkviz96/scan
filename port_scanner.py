from socket import socket, gethostbyname, AF_INET, SOCK_STREAM
from prettytable import PrettyTable
from colorama import *
import progressbar
import logging





class PortCheck:

	def start(self):
		self.target = input("Input target's ip or url: ")
		self.ports = [int(x) for x in input("Input ports \"like 80 443 8080\"(or empty for full scan): ").split()]
		if self.ports == []:
			self.ports = [20, 21, 22, 23, 24, 25, 26, 27, 29, 53, 67, 68, 79,
				 80, 88, 106, 110, 111, 113, 119,465, 500, 514, 414,
				 532, 548, 554, 587, 600, 623, 625, 626, 660, 687, 749,
				 985, 993,995, 1085, 1099, 1220, 1640, 1649, 1701, 1723, 1900, 2049,
				 2195, 2196, 2336, 3004,3031, 3283, 3284, 3306, 3659, 3689, 3690, 4111,
				 4488, 4500, 5003, 5100, 5222, 5223, 5228, 5297, 5350, 5351, 5353, 6970, 
				 7070, 8000, 8005, 8008, 8043, 8080, 8089, 8096, 8170, 8171, 8175, 8443, 
				 8800, 8843, 9418, 11211, 50003]


	def check_ports(self):
		targetIP = gethostbyname(self.target)
		portIsOpen = []
		portIsClose = []
		statusPortScan = len(self.ports)
		logging.info(targetIP)
		progressBarScan = progressbar.ProgressBar(maxval=statusPortScan)
		progressBarScan.start()
		contProgressBar = 0
		for portCount in self.ports:
			testSocket = socket(AF_INET, SOCK_STREAM)
			testSocket.settimeout(1)
			try:
				result = testSocket.connect_ex((targetIP, int(portCount)))
				if(result == 0):
					portIsOpen.append(portCount)
					progressBarScan.update(contProgressBar)
					contProgressBar += 1
				else:
					portIsClose.append(portCount)
					progressBarScan.update(contProgressBar)
					contProgressBar += 1
				testSocket.close()
			except:
				logging.warning("ERROR SOCKET!")
			
		progressBarScan.finish()

		return portIsOpen, portIsClose

	def portsTable(self, open_ports, close_ports):
		table_prots = PrettyTable([Back.WHITE + Fore.BLACK + "Port", "Availability"])
		[table_prots.add_row([Back.WHITE + Fore.GREEN + str(port), "Open"]) for port in open_ports]
		[table_prots.add_row([Back.WHITE + Fore.RED + str(port), "Close"]) for port in close_ports]
		table_prots.reversesort = False

		return table_prots


if __name__ == '__main__':
	init(autoreset=True)
	ant = PortCheck()
	ant.start()
	open_ports, close_ports = ant.check_ports()
	print(ant.portsTable(open_ports, close_ports))