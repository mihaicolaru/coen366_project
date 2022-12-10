import socket
import sys

# get port number
try:
    print("port given: ", sys.argv[1])
except IndexError:
    quit("no port given") 

try:
    print("debug enabled: ", sys.argv[2])
    if sys.argv[2] == 1:
        debug = True
    else:
        debug = False
except IndexError:
    quit("debug bit not given")

s = socket.socket()
host = '127.0.0.1'
port = sys.argv[1]
# port = input(str("enter port server will listen on: "))
s.bind((host,int(port)))
s.listen(1)
print(host)

while 1:
    print("waiting for clients")
    connection, address = s.accept()
    print(address," has been connected to the server")
    connected = True

    response = ""
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
        except ConnectionAbortedError:
            print("connection was aborted")
            break

        if len(request) == 0:
            print("no data")
            break

        print("request: ",request)

        # parse request message
        # 3 first characters: opcode
        opcode = request[0:3]
        print("opcode: ",opcode)

        response = ""
        if opcode == '000':
            
            print("put command")

            print("rest of request: ",request[3:])

            FL = int("0b" + request[3:8], 2)
            print("filename length: ",FL)

            file_name = request[8:8+FL]
            print("filename: ",file_name)
            
            FS = int("0b" + request[8+FL:8+FL+32], 2)
            print("file size: ",FS)

            file_data = request[8+FL+32:]
            print("file data: ",file_data)

            new_file = open(file_name, "w")
            new_file.write(file_data)
            new_file.close()
            response = "00000000"


        elif opcode == '001':
            print("get command")
            print("rest of request: ",request[3:])
        elif opcode == '010':
            print("change command")
            print("rest of request: ",request[3:])
        elif opcode == '011':
            # add rescode
            response = "110"
            print("help command")
            command_list = "list of acceptable commands:\nput (filename)\t\t\t\tsend file to server\nget (filename)\t\t\t\tget file from server\nchange (old filename) (new filename)\tchange server file name\nhelp\t\t\t\t\tdisplay this message"
            list_length = bin(len(command_list))[2:]
            i = 5 - len(list_length)
            while i > 0:
                response = response + "0"
                i = i - 1
            
            response = response + str(list_length)
            response = response + command_list
        else:
            print("opcode error")
            
        


        # send back response
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