'''
Created on 30 de mai de 2017
@author: Gibson
'''
import socket,thread,sys

MAX_RECV=2097152
httpport=80
ServerPort=8080
blmsg='HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><header><title>ERROR</title></header><body><div align="center" style="border:1px solid red"><p>Acesso negado.</br>Site na blacklist.</p></div></body></html>\n'
denymsg='HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><header><title>ERROR</title></header><body><div align="center" style="border:1px solid red"><p>Acesso negado.</br>Site contem termos proibidos.</p></div></body></html>\n'

def main():


    ServerName='127.0.0.1'
    ServerAddress=ServerName,ServerPort
    
    try:
        ServerSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        ServerSocket.bind(ServerAddress)
        ServerSocket.listen(1)

        print "Aguardando conexao\n"

        while True:
            cliente,address=ServerSocket.accept()
            thread.start_new_thread(webproxy,(cliente,address))
        
        ServerSocket.close()
    
    except socket.error, (value, message):
        print message
           
def webproxy(cliente,address):
    reqdeny=0
    reqdeny1=0    
    print "\nusuario: ",address[0],address[1]
    msg=cliente.recv(MAX_RECV)
    indice_final = msg.find('\n')
    if indice_final != -1:

        msglist=msg.split('\n')
        website=(msglist[1].split())[1]       
        
        proxyflag=permission(website)
        
        if proxyflag == 0 or proxyflag == 2:
            
            if proxyflag == 0:
                reqdeny=permission_terms(msg)
            try:
                webaddress2=socket.gethostbyname(website)
                print webaddress2
                webaddress=website
                DEST=webaddress,httpport
                tcp=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
                tcp.connect(DEST)
                print "conectado a: \n",website
                tcp.sendall(msg)
        
                while True:
                    msgr=tcp.recv(MAX_RECV)
                    if proxyflag == 0:
                        reqdeny1=permission_terms(msgr)
                    #print msgr
                    if (len(msgr)>0 and reqdeny == 0 and reqdeny1 == 0):
                        cliente.send(msgr)
                        print "connected"
                    else:
                        break
                tcp.close()
            except socket.error, (value, message):
                print message
                
        if proxyflag == 1:
      #      print "blacklist"
            cliente.send(str.encode(blmsg))

            
        else: 
            if (reqdeny == 1 or reqdeny1 == 1):
           #     print "denied"
                cliente.send(str.encode(denymsg))
                blacklist_add(website)

    cliente.close()
            
def permission(website):  
    
    wl=open('whitelist.txt','r')
    bl=open('blacklist.txt','r')
    flag=0
    
    for line in wl:
        if website == line.rstrip('\n'):
            flag=2     
    for line in bl:
        if website == line.rstrip('\n'):
            flag=1
            
    wl.close()
    bl.close()
    
    return flag        
    
def permission_terms(msg):  
    
    denyterms=open('denyterms.txt','r')
    
    flag=0
        
    for line in denyterms:
        for element in msg.split():
            if element == line.rstrip():
                flag=1
            
    denyterms.close()
    
    return flag            

def blacklist_add(website):
    
    bl=open('blacklist.txt','a')
    bl.write('\n'+website)
    bl.close()
                     
main()