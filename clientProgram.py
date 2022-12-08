# here is where we write the client side code

import socket

s = socket.socket()
host = input(str("Please enter the host address of the sender:"))
port = 10020
s.connect((host, port))
print("Client is connected....")

# getting the transfer_file
filename = input(str(" Enter a filename for the incoming file: "))
file = open(filename, 'wb')
file_data = s.recv(1024)
file.write(file_data)
print(file_data)
file.close()
print(" The file has been received ")