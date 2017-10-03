from sys import argv
from socket import *


#****************************************************************************************
# Usage function to handle command line argument
#****************************************************************************************
def usage():
	# print the usage of the function for client
  	print "This is the usage function"
  	print "Usage: <server_address>, <n_port>(int), <req_code>(int), and <msg> in the given order"
  	exit()


#****************************************************************************************
# Stage 1: Negotiation using UDP sockets for client
# The function takes in server_ip, negotiation port, client request code and it returns
#		the client random port to connect to the server using TCP socket.
#****************************************************************************************
def client_UDP_socket_negotiation(server_ip, n_port, client_req_code):
 	# create client UDP socket
	client_socket = socket(AF_INET, SOCK_DGRAM)			

	# attach server name, port to message, send the request code to the server
	client_socket.sendto(client_req_code, (server_ip, n_port)) 
	
	# reveive the r_port and server address
	client_r_port, server_address = client_socket.recvfrom(1024) 
	# send the r_port for the server to confirm
	client_socket.sendto(str(client_r_port), server_address) 

	# reveive acknowledgement info from the server
	ack, server_address = client_socket.recvfrom(1024) 

	# the client closes the UDP socket with the server
	client_socket.close() 

	# check is acknowledgement is "ok" or "no"
	if ack != "ok":	
		# if not "ok", then exit
		exit() 

	# return r_port for TCP socket to connect to the server
	return client_r_port


#****************************************************************************************
# Stage 2: Transaction using TCP sockets
# The function takes in server_ip, client_r_port and prints the reversed string that get
#		from the server.
#****************************************************************************************
def client_TCP_socket_transaction(server_ip, client_r_port):
	# create client TCP socket
	client_tcp_socket = socket(AF_INET, SOCK_STREAM) 
	# connect to the server
	client_tcp_socket.connect((server_ip, int(client_r_port))) 

	# send the string to the server, no need to attach server name, port
	client_tcp_socket.send(string) 

	# receive the reversed string from the server
	reversed_string = client_tcp_socket.recv(1024) 
	# print the reversed string
	print '{}{}{}'.format("CLIENT_REVERSED_MSG=\'",reversed_string,"\'")
	 
	# close the client TCP socket
	client_tcp_socket.close() 


#****************************************************************************************
# Client program: it takes four command line inputs:
#		  <server_address> , <n_port>, <req_code>, and <msg> in the given order,
#		  it prints the reversed string.
#****************************************************************************************
# Check if command line arguments are valid
if (len(argv) != 5) or (not argv[2].isdigit()) or (not argv[3].isdigit()):
	# call usage if not valid
	usage()

# get the server ip from command line argument
server_ip = argv[1]
# get the n_port from command line argument
n_port = int(argv[2]) 
# get the client request code from command line argument
client_req_code = argv[3]
# get the original string from command line argument
string = argv[4] 

# create UDP socket for client and process negotiation stage
client_r_port = client_UDP_socket_negotiation(server_ip, n_port, client_req_code)

# create TCP socket for client and process transaction stage (string reverse) 
client_TCP_socket_transaction(server_ip, client_r_port)
