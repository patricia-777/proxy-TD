'''
Created on 30 de mai de 2017

@author: Gibson
'''

import socket

httpport=80
ServerName='127.0.0.1'
ServerPort=8080
ServerAddress=ServerName,ServerPort
ServerSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ServerSocket.bind(ServerAddress)
ServerSocket.listen(10)

print "Aguardando conexao"

cliente,address=ServerSocket.accept()
print "usuario: ",address[0],address[1]

while True:
    msg=cliente.recv(1048576)
    print msg
    msglist=msg.split('\n')
    website=(msglist[1].split())[1]
    webaddress=socket.gethostbyname(website)
    print "conectando a: ",webaddress
    print "\n"
    DEST=webaddress,httpport
    tcp=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    tcp.connect(DEST)
    tcp.sendall(msg)

    msgr=tcp.recv(1048576)
    print msgr
    while True:
        cliente.sendall(msgr)
        break
    cliente.close()
    tcp.close()
    break



