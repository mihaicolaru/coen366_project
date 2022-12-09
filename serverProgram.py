import socket

# get port number
s = socket.socket()
host = '127.0.0.1'
port = input(str("enter port server will listen on: "))
s.bind((host,int(port)))
s.listen(1)
print(host)

while 1:
    print("waiting for clients")
    connection, address = s.accept()
    print(address," has been connected to the server")
    connected = True

    while connected:
        # listen for request messages from server, in try catch block in case connection broken
        request = connection.recv(1024).decode()
        # try:
        #     request = connection.recv(1024).decode()
        #     if len(request) == 0:
        #         print("read 0 bytes")
        # except BlockingIOError:
        #     print("reading")
        # except ConnectionResetError:
        #     print("connection was reset")
        #     break
        # except BrokenPipeError:
        #     print("connection was broken")
        #     break

        print(request)
        # parge request message
        # 3 first characters: opcode

        # switch(opcode) (generate response string)
        # put (000)
        # get (001)
        # change (010)
        # help (011)

        # send back response string
        response = 'received: ' + request
        try:
            connection.send(response.encode())
        except ConnectionResetError:
            print("connection was reset")
            break
        except BrokenPipeError:
            print("connection was broken")
            break

        # if connection broken, go back to listening for connections

print("server terminating")
connection.close()