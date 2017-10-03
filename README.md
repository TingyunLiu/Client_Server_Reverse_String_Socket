-------------------------
Command Line Instructions
-------------------------
Example: ./server <req_code>
		 ./client <server_address>, <n_port>, <req_code>, <msg>

Note: Always running the server program first, then run the client program. The client
		program will finished once get the reversed string back from the server,
		but the server will still be running and waiting for another client.
	  <req_code> for server and client must be equal and integer.
	  <server_address> must be the server's IP address, which can be get by the command:
	  	'curl ipecho.net/plain' in server's environment.
	  <n_port> for client must be equal to the integer that server printed.
	  <msg> is the string that client wants to send to the server.


-------------------
Compiler version 
-------------------
The program can be compiled by Python 2.7.12


-------------------
Running Environment 
-------------------
The program has been run and tested on ubuntu environments.
