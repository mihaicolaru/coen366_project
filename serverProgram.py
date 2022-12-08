# here is where we write the server side code

import socket

s = socket.socket()
host = socket.gethostname()
port = 10020
s.bind((host,port))
s.listen(1)
print(host)
print("waiting for connectors")
connection, address = s.accept()
print(address,"Has been connected to the server")

# transferring file
transfer_file = input(str("Enter the filename that will be transferred: "))
transfer_file = open(transfer_file,'rb')
file_data = transfer_file.read(1024)
print(filedata)
s.send(filedata)
print("file has been sent")