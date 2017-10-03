#!/bin/bash

#Run script for client
#Number of parameters: 4
#Parameter:
#    $1: <server_address>
#    $2: <n_port>
#    $3: <req_code>
#    $4: message

python client.py $1 $2 $3 "$4"
