from sys import argv
from socket import *


#****************************************************************************************
# Usage function to handle command line argument
#****************************************************************************************
def usage():
	# print the usage of the function for client
  	print "This is the usage function"
  	print "Usage: it takes <req_code>(int)"
  	exit()


#****************************************************************************************
# Helper function for creating a socket for server and extracting the port number
# The function takes in a type of socket and returns the server socket
#****************************************************************************************
def server_socket_creation(type_of_socket):
	# create server UDP/TCP socket
	server_socket = socket(AF_INET, type_of_socket)
	# bind server UDP/TCP socket to a random available local port
	server_socket.bind(("",0))

	# extract the n_port(negotiation port) or r_port(random port)
	port_number = server_socket.getsockname()[1] 
	# print n_port/r_port for clients to connect
	if type_of_socket is SOCK_DGRAM: # UDP
		print "SERVER_PORT=",port_number
	elif type_of_socket is SOCK_STREAM: # TCP
		print "SERVER_TCP_PORT=",port_number
	else:
		print "ERROR: it should be UDP or TCP socket"
		# error case
		server_socket.close()
		exit()

	return server_socket


#****************************************************************************************
# Helper function for receiving a string and send the reversed string back to the client
# The function takes in a socket connection
#****************************************************************************************
def reverse_string(connection):
	# receive message from the client. 1024 bytes is sufficient for the input buffer 
	string = connection.recv(1024) 
	# print the reveived string
	print '{}{}{}'.format("SERVER_RCV_MSG=\'",string,"\'") 

	# reverse the string
	reversed_string = string[::-1]
	# send the reversed string back to the client
	connection.send(reversed_string)


#****************************************************************************************
# Server program: it takes <req_code>, it prints the negotiation port number of UDP,
#		  first, then prints the random port number of TCP, and received message.
#****************************************************************************************
# Check if command line arguments are valid
if (len(argv) != 2) or (not argv[1].isdigit()):
	# call usage if not valid
	usage()

# create UDP socket for server and process negotiation stage
server_socket = server_socket_creation(SOCK_DGRAM)

# loop forever, server keeps running
while True: 

	# get the server request code from command line argument
	server_req_code = argv[1] 

	# receive the client request code
	client_req_code, client_address = server_socket.recvfrom(1024) 
	# check if the request codes are the same
	if int(server_req_code) != int(client_req_code): 
		# if not the same, then do nothing for current client, go to next
		continue

	# create TCP socket and print r_port
	server_tcp_socket = server_socket_creation(SOCK_STREAM)
	server_r_port = server_tcp_socket.getsockname()[1]

	# server begins listening for incoming TCP requests
	server_tcp_socket.listen(1) 

	# server send the r_port to client using the UDP socket
	server_socket.sendto(str(server_r_port), client_address) 
	# receive the r_port from client
	received_client_r_port, client_address = server_socket.recvfrom(1024) 
	# check if the server r_port and client r_port are the same
	if int(server_r_port) != int(received_client_r_port):
		# not equal, so send no to client	
		server_socket.sendto("no", client_address)
		# not the same, then do nothing for current client, go to next 
		continue
	# send "ok" acknowledgement to the client using the UDP socket
	server_socket.sendto("ok", client_address) 

	# server waits on accept() for incoming requests, new socket created on return
	client_tcp_socket_connection, addr = server_tcp_socket.accept() 
	# reverse the received string and send it back to the client
	reverse_string(client_tcp_socket_connection)

	# close connection to this client
	client_tcp_socket_connection.close()

# close the UDP socket, would not come here
server_socket.close()

