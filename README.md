# coen366_project
FTP simulation with sockets for COEN 366 course at Concordia University

simple file transfer protocol using python client-server programs communicating via python socket stream

the main goals are:
- give client program ability to download server directory to client directly
- give client program ability to upload files from client directory to server directory

supported file types:
any (.txt, .doc, .jpg)

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
