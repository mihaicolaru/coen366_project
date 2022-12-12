# coen366_project
FTP simulation with sockets for COEN 366 course at Concordia University

simple file transfer protocol using python client-server programs communicating via python socket stream

the main goals are:
- give client program ability to download server directory to client directly
- give client program ability to upload files from client directory to server directory

supported file types:
any (.txt, .doc, .jpg, .pdf)

typical FTP interaction simulated:
- client connect to server
- if conntection successful:
  - client program can transfer files to server (put)
  - client program can retrieve files from server (get)
  - client program can change file names in server
- client program reads user command -> parses command -> forms message request -> sends request to server
- server program receives request -> parses request -> executes command -> forms message response -> sends response to server
- client program handles incoming response message
- when client quits, it closes communication with the server
- server should keep listenning passively for new connection requests from other clients

USAGE:
server and client must typically be in different directories (localhost)

1. server program is started with port number and debug bit as command-line arguments

2. client program is started with localhost IP address, same port number as server and debug bit as command-line arguments

3. when connection is successful, client can send put, get, change and help requests to server

4. bye command terminates client

files that are to be transfered from the client must be in the same directory as the program source file
test folder included in the project can be used to verify program functioning be copying the files to the client directory
