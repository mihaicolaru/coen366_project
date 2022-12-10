import socket

# open socket
s = socket.socket()
host = input(str("Please enter the server IP address: "))
port = input(str("please enter the server port number: "))
s.connect((host, int(port)))
print("client is connected....")


# get user command from std input
# generate request msg in switch according to command
def parse_input(input_string):
    request = ""
    string_set = input_string.split(" ")
    if string_set[0] == 'put':
        # add opcode
        request = request + "000"

        # try catch to check if argument was passed
        print("filename: ", string_set[1])  # put filename

        # try open filename, file not found exception just prints file not found

        # if file is open
        # get length of filename, append to request (5 bits)
        # append filename to request
        # read file data into a new string
        # get size of file data string (4 bytes), append to request
        # append file data to request        
        
        return True, request
    elif string_set[0] == "get":
        # add opcode
        request = request + "001"
        # add try catch block to verify that argument was added
        print("filename: ", string_set[1])  # get filename
        
        # get length of filename, append to request (5 bits)
        # append filename to request

        return True, request
    elif string_set[0] == "change":
        # add opcode
        request = request + "010"

        try:
            print(f"change:\nold filename: {string_set[1]}\nnew filename: {string_set[2]} ")  # change old new
        except IndexError:
            print("Filename missing")
            return False, "error"
        
        # get length of old filename, append to request (5 bits)
        # append old filename to request
        # get length of new filename, append to request (1 byte)
        # append new filename to request
        
        return True, request
    elif string_set[0] == "help":
        # add opcode
        request = request + "011" + "00000"
        print("help")  # help
        
        return True, request
    elif string_set[0] == "bye":
        print("connection is going to terminate and exit")  # bye
        return False, request
    else:
        print("incorrect input")
        return False, "error"

while 1:
    # get user command from std input
    command = input(str("please enter command: "))

    # parse command
    send_request, request = parse_input(command)
    
    # check if we need to get new command or terminate
    if not send_request:
        if request == "error":
            continue
        else:
            break

    # send request msg to server
    s.send(request.encode())

    # listen for response
    response = s.recv(1024)
    print(response.decode())


# after loop, close conntection to server
s.close()
print("connection closed")
