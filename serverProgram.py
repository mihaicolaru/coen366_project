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
        # listen for request messages from client, in try catch block in case connection broken
        try:
            request = connection.recv(1024).decode()
        except BlockingIOError:
            print("reading")
        except ConnectionResetError:
            print("connection was reset")
            break
        except BrokenPipeError:
            print("connection was broken")
            break

        if len(request) == 0:
            print("no data")
            break

        print("request: ",request)
        # parge request message
        # 3 first characters: opcode

        opcode = request[0:3]
        print("opcode: ",opcode)
        if opcode == '000':
            print("put command")
        elif opcode == '001':
            print("get command")
        elif opcode == '010':
            print("change command")
        elif opcode == '011':
            print("help command")
        else:
            print("opcode error")
        # FL = request[3:7]
        # file_name = request[7:7+FL+1]
        
        # FS = request[7+FL+2:7+FL+2]


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
        except ConnectionAbortedError:
            print("connection was aborted")
            break

        # if connection broken, go back to listening for connections

print("server terminating")
connection.close()