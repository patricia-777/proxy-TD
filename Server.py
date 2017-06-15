'''
Created on 30 de mai de 2017

@author: Gibson
'''
import socket,thread,sys

MAX_RECV=2097152
httpport=80
ServerPort=8080
    
def main():


    ServerName='127.0.0.1'
    ServerAddress=ServerName,ServerPort
    ServerSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    ServerSocket.bind(ServerAddress)
    ServerSocket.listen(1)

    print "Aguardando conexao\n"

    while True:
        cliente,address=ServerSocket.accept()
        thread.start_new_thread(webproxy,(cliente,address))
        
    ServerSocket.close()
    

def webproxy(cliente,address):    
    print "\nusuario: ",address[0],address[1]
    msg=cliente.recv(MAX_RECV)
   # print msg
    msglist=msg.split('\n')
    print "LISTA: ",msglist
    if msglist:
        website=(msglist[1].split())[1]
   # print website
        webaddress=socket.gethostbyname(website)
    #print "conectando a: ",webaddress
   # print "\n"
        DEST=webaddress,httpport
        tcp=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        tcp.connect(DEST)
        print "conectado a: \n",website
        tcp.sendall(msg)
    
        while True:
            msgr=tcp.recv(MAX_RECV)
        #print msgr
            if (len(msgr)>0):
                cliente.send(msgr)
            else:
                tcp.close()
                break
    cliente.close()
    #print "\n Conexao finalizada"
    return

main()



