import socket

# open socken
s = socket.socket()
host = input(str("Please enter the server IP address: "))
port = input(str("please enter the server port number: "))
s.connect((host,int(port)))
print("Client is connected....")

while 1:
    # get user command from std input
    command = input(str("please enter command: "))
    
    # split input string by " "

    # parse set of split input string with switch (inputset[0])

    # generate request msg in switch according to command

    # put filename
    # getting the transfer_file
    # filename = input(str(" Enter a filename for the incoming file: "))
    # file = open(filename, 'wb')
    # write file content and size (etc) in msg request
    

    # get filename

    # change old new

    # help

    # bye
    # break
    if command == 'bye':
        break

    # send request msg to server
    s.send(command.encode())

    # listen for response
    response = s.recv(1024)
    print(response.decode())
    # after response or timeout, loop
    
# after loop, close conntection to server
s.close()
print("connection closed")