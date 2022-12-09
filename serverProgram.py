# here is where we write the server side code

import socket

# need to give commandline argument for port number to listen to
s = socket.socket()
host = socket.gethostname()
port = 10020
s.bind((host,port))
s.listen(1)
print(host)
print("waiting for connectors")
connection, address = s.accept()
print(address,"Has been connected to the server")

# while (1)

# listen for request messages from server

# parge request message
# 3 first characters: opcode

# switch(opcode) (generate response string)
# put (000)
# get (001)
# change (010)
# help (011)

# send back response string

# if connection broken, go back to listening for connections


# transferring file
transfer_file = input(str("Enter the filename that will be transferred: "))
transfer_file = open(transfer_file,'rb')
file_data = transfer_file.read(1024)
print(file_data)
s.send(file_data)
print("file has been sent")