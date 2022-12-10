import socket
import sys

#input host number
try:
    print("IP address given", sys.argv[1])
    print("Port given", sys.argv[2])
except IndexError:
    quit("No port or IP address given")

try:
    print("Debug enabled:", sys.argv[3])
    if sys.argv[3] == "1":
        debug = True
    else:
        debug = False
except IndexError:
    quit("debug bit not given")

# open socket
s = socket.socket()
host = sys.argv[1]
port = sys.argv[2]
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
        try:
            if debug:
                print("filename: ", string_set[1])  # put filename
        except IndexError:
            print("Filename not found")  # try open filename, file not found exception just prints file not found
            return False, "error"

        try:
            file = open(string_set[1], "r")
            if debug:
                print("file is open")
        except Exception:
            print("file not found")
            return False, "error"

        # if file is open

        FL = bin(len(string_set[1]))[2:]  # get length of filename, append to request (5 bits)
        i = 5 - len(FL)
        while i > 0:
            request = request + "0"
            i = i - 1
        if debug:
            print("FL is ", str(FL))
        request = request + str(FL)  # append filename length to request
        request = request + string_set[1]  # append filename to request
        file_data = file.read()  # read file data into a new string
        FS = bin(len(file_data))[2:]  # get size of file data string (4 bytes), append to request
        i = 32 - len(FS)
        while i > 0:
            request = request + "0"
            i = i - 1
        if debug:
            print("FS is ", str(FS))
        request = request + str(FS)   # append file data length to request
        request = request + file_data  # append file data to request

        return True, request
    elif string_set[0] == "get":
        # add opcode
        request = request + "001"
        # add try catch block to verify that argument was added
        try:
            if debug:
                print("filename: ", string_set[1])  # get filename
        except IndexError:
            print("File not found")
            return False, "error"

        FL = bin(len(string_set[1]))[2:] # get length of filename, append to request (5 bits)
        i = 5 - len(FL)
        while i > 0:
            request = request + "0"
            i = i - 1
        if debug:
            print("FL is ", str(FL))
        request = request + str(FL)  # append filename length to request
        request = request + string_set[1]  # append filename to request
        return True, request
    elif string_set[0] == "change":
        # add opcode
        request = request + "010"
        try:
            if debug:
                print(f"change:\nold filename: {string_set[1]}\nnew filename: {string_set[2]} ")  # change old new
            old_fl = bin(len(string_set[1]))[2:]  # get length of old filename, append to request (5 bits)
            i = 5 - len(old_fl)
            while i > 0:
                request = request + "0"
                i = i - 1
            if debug:
                print("FL is ", str(old_fl))
            request = request + str(old_fl)  # append old filename length to request
            request = request + string_set[1]  # append old filename to request
            new_fl = bin(len(string_set[2]))[2:]  # get length of new filename, append to request (1 byte)
            i = 8 - len(new_fl)
            while i > 0:
                request = request + "0"
                i = i - 1
            if debug:
                print("FL is ", str(new_fl))
            request = request + str(new_fl)  # append new filename length to request
            request = request + string_set[2]  # append new filename to request
        except IndexError:
            print("Filename missing")
            return False, "error"

        return True, request
    elif string_set[0] == "help":
        # add opcode
        request = request + "011" + "00000"
        if debug:
            print("help")  # help
        return True, request
    elif string_set[0] == "bye":
        if debug:
            print("connection is going to terminate and exit")  # bye
        return False, request
    else:
        if debug:
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
            print("Incorrect command")
            continue
        else:
            break

    # send request msg to server
    s.send(request.encode())

    # listen for response
    try:
        response = s.recv(1024).decode()
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

    res_code = response[0:3]
    if debug:
        print("response ", response)
    if res_code == '000':
        print("successful put or change")
    elif res_code == '001':
        print("successful get")
        FL = int("0b" + response[3:8], 2)
        if debug:
            print("filename length", FL)
        file_name = response[8:8+FL]
        if debug:
            print("filename", file_name)
        FS = int("0b" + response[8+FL:8+FL+32], 2)
        if debug:
            print("file size", FS)
        file_data = response[FL+40:]
        if debug:
            print("file data", file_data)

        new_file = open(file_name, "w")
        new_file.write(file_data)
        new_file.close()

    elif res_code == '010':
        print("Error: File not found")
    elif res_code == '011':
        print("Error: Unknown request")
    elif res_code == '101':
        print("Unsuccessful change")
    elif res_code == '110':
        help_message = response[8:]
        print("available commands:", help_message)

# after loop, close connection to server
s.close()
print("connection closed")
