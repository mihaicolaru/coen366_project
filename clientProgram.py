import socket

# open socket
s = socket.socket()
host = input(str("Please enter the server IP address: "))
port = input(str("please enter the server port number: "))
s.connect((host, int(port)))
print("Client is connected....")


# get user command from std input
def parse_input(input_string):
    request = ""
    string_set = input_string.split(" ")
    if string_set[0] == 'put':
        print("filename: ", string_set[1])  # put filename
        request = request + "000"
        return False, request
    elif string_set[0] == "get":
        print("filename: ", string_set[1])  # get filename
        request = request + "001"
        return False, request
    elif string_set[0] == "change":
        try:
            print(f"change:\nold filename: {string_set[1]}\nnew filename: {string_set[2]} ")  # change old new
        except IndexError:
            print("Filename missing")

        request = request + "010"
        return False, request
    elif string_set[0] == "help":
        print("help")  # help
        request = request + "011" + "00000"
        return False, request
    else:
        print("connection is going to terminate and exit")  # bye and break/after response or timeout, loop
        return True, ""

while 1:
    # get user command from std input
    command = input(str("please enter command: "))

    # split input string by " "
    terminated, request = parse_input(command)
    # parse set of split input string with switch (inputset[0])

    # generate request msg in switch according to command

    # bye
    # break
    if terminated:
        break

    # send request msg to server
    s.send(request.encode())

    # listen for response
    response = s.recv(1024)
    print(response.decode())


# after loop, close conntection to server
s.close()
print("connection closed")
