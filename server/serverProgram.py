# Mihai Olaru 40111734
# Charlie Huang 40111215
# this file contains the implementation for the server side of the project
# we are the sole authors this file

import socket
import sys
import os

# get port number
try:
    print("port given: ", sys.argv[1])
except IndexError:
    quit("no port given") 

debug = False

# get debug bit
try:
    print("debug enabled: ", sys.argv[2])
    if sys.argv[2] == "1":
        debug = True
    else:
        debug = False

    print(debug)
except IndexError:
    quit("debug bit not given")

s = socket.socket()
host = '127.0.0.1'
port = sys.argv[1]
s.bind((host,int(port)))
s.listen(1)
if debug:
    print(host)

while 1:
    print("waiting for clients")
    connection, address = s.accept()
    print(address," has been connected to the server")

    response = ""
    while 1:
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
            if debug:
                print("no data")
            break
        if debug:
            print("request: ",request)

        # parse request message
        # 3 first characters: opcode
        opcode = request[0:3]
        if debug:
            print("opcode: ",opcode)

        # put request
        response = ""
        if opcode == '000':            
            print("put command")
            if debug:
                print("rest of request: ",request[3:])

            FL = int("0b" + request[3:8], 2)
            if debug:
                print("filename length: ",FL)

            file_name = request[8:8+FL]
            if debug:
                print("filename: ",file_name)
            
            FS = int("0b" + request[8+FL:8+FL+32], 2)
            if debug:
                print("file size: ",FS)
            
            # loop receive based on file size

            num_reads = FS/1024
            with open(file_name, "wb") as new_file:
                while num_reads > 0:
                    if debug:
                        print("getting file data chunk")
                    try:
                        file_data = connection.recv(1024)
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

                    new_file.write(file_data)

                    num_reads = num_reads - 1
            new_file.close()
            # if debug:
            #     print("file data: ",file_data)
            
            response = "00000000"

        # get request
        elif opcode == '001':
            print("get command")
            if debug:
                print("rest of request: ",request[3:])

            FL = int("0b" + request[3:8], 2)    # get filename length
            if debug:
                print("filename length: ",FL)

            file_name = request[8:8+FL]     # get filename
            if debug:
                print("filename: ",file_name)

            try:
                response = "001" + request[3:8] + file_name   # add rescode, filename length and filename to response
                if debug:
                    print("successful response header: ", response)
                
                target_file = open(file_name, "rb")  # open requested file
                file_data = target_file.read()     # get file contents
                target_file.close()

                FS = bin(len(file_data))[2:]    # get size of file
                i = 32 - len(FS)
                while i > 0:
                    response = response + "0"
                    i = i - 1
                response = response + str(FS)   # append file size (padded) to response

                if debug:
                    print("sending response")
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

                with open(file_name, "rb") as target_file:
                    while 1:
                        read_bytes = target_file.read(1024)
                        if not read_bytes:
                            if debug:
                                print("end of target file reached")
                            break
                        connection.send(read_bytes)
                target_file.close()
                continue
            
            except FileNotFoundError:
                print("file not found error")
                response = "0100000"
            except Exception:
                print("file error")
                response = "0100000"

        # change request
        elif opcode == '010':
            try:
                response = "00000000"
                print("change command")
                if debug:
                    print("rest of request: ",request[3:])

                old_fl = int("0b" + request[3:8], 2)
                if debug:
                    print("old filename size: ",old_fl)

                old_filename = request[8:8+old_fl]
                if debug:
                    print("old filename: ", old_filename)

                new_fl = int("0b" + request[8+old_fl:8+old_fl+8], 2)
                if debug:
                    print("new filename size: ",new_fl)

                new_filename = request[8+old_fl+8:]
                if debug:
                    print("new filename: ", new_filename)
            except IndexError:
                print("filename missing")
                response = "10100000"
            
            try:
                os.rename(old_filename.encode(), new_filename.encode())
                print("changed name successfully")
            except FileNotFoundError:
                print("file not found")
                response = "10100000"
            except Exception:
                print("could not rename file")
                response = "10100000"
        
        # help request
        elif opcode == '011':
            # add rescode
            response = "110"
            print("help command")
            command_list = "put, get, change, help, bye"
            if debug:
                print("list of commands: ", command_list)
            list_length = bin(len(command_list))[2:]
            if debug:
                print("help response length: ", list_length)
            i = 5 - len(list_length)
            while i > 0:
                response = response + "0"
                i = i - 1
            
            response = response + str(list_length)
            response = response + command_list

            if debug:
                print("full help response: ", response)
        else:
            print("unknown request error")
            response = "01100000"
            
        if debug:
            print("sending response")
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