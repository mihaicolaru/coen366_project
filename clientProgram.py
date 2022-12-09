# here is where we write the client side code

import socket

s = socket.socket()
host = input(str("Please enter the host address of the sender:"))
port = 10020
s.connect((host, port))
print("Client is connected....")

# start while(1)

# get user command from std input

# split input string by " "

# parse set of split input string with switch (inputset[0])
# generate request msg in switch according to command

# put filename
# getting the transfer_file
filename = input(str(" Enter a filename for the incoming file: "))
file = open(filename, 'wb')
# write file content and size (etc) in msg request
file_data = s.recv(1024)
file.write(file_data)
print(file_data)
file.close()
print(" The file has been received ")

# get filename

# change old new

# help

# bye
# break

# send request msg to server, listen for response

# after response or timeout, loop


# after loop, close conntection to server

