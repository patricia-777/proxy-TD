'''
Created on 30 de mai de 2017
@author: Gibson
'''
import socket,thread,sys

# VARIAVEIS CONSTANTES

MAX_RECV=2097152
httpport=80
ServerPort=8080
blmsg='HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><header><title>ERROR</title></header><body><div align="center" style="border:1px solid red"><p>Acesso negado.</br>Site na blacklist.</p></div></body></html>\n'
denymsg='HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><header><title>ERROR</title></header><body><div align="center" style="border:1px solid red"><p>Acesso negado.</br>Site contem termos proibidos.</p></div></body></html>\n'


# MAIN
def main():

    # NOME DO SERVIDOR E PORTA #
    ServerName='127.0.0.1'
    ServerAddress=ServerName,ServerPort
    
    # CRIACAO DO SOCKET DO SERVIDOR #
    try:
        ServerSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        ServerSocket.bind(ServerAddress)
        ServerSocket.listen(1)

        print "Aguardando conexao\n"

        # CONEXAO ENTRE SERVIDOR PROXY E USUARIO
        while True:
            cliente,address=ServerSocket.accept()
            
            # AO ESCUTAR UM CLIENTE, GERA UMA NOVA THREAD PARA AQUELE USUARIO
            thread.start_new_thread(webproxy,(cliente,address))
        
        ServerSocket.close()
    
    # MENSAGENS DE ERROR NO SOCKET 
    except socket.error, (value, message):
        print message
           
           
# FUNCAO DO PROXY          
def webproxy(cliente,address):
    
    # FLAGS PARA VERIFICACAO DE TERMOS
    reqdeny=0
    reqdeny1=0    
    print "\nusuario: ",address[0],address[1]
    
    # MENSAGEM DE REQUISICAO HTTP 
    msg=cliente.recv(MAX_RECV)
    
    # VERIFICACAO SE A MENSAGEM NAO EH VAZIA
    indice_final = msg.find('\n')
    if indice_final != -1:

        # OBTENCAO DO SITE QUE O USUARIO QUER ACESSAR
        msglist=msg.split('\n')
        website=(msglist[1].split())[1]       
        
        #FLAG DE VERIFICACAO SE O SITE PODE SER ACESSADO
        proxyflag=permission(website)
        
        if proxyflag == 0 or proxyflag == 2:
            
            #SE O SITE NAO ESTIVER NA WHITE LIST, OS SEUS TERMOS DEVEM SER VERIFICADOS
            if proxyflag == 0:
                #VERIFICACAO DOS TERMOS DA MENSAGEM DE REQUISICAO
                reqdeny=permission_terms(msg)
                
            # CRIACAO DE CONEXAO ENTRE O SERVIDOR E O SITE QUE O USUARIO DESEJA ACESSAR     
            try:
                # OBTENCAO DO IP PELO NOME DO SITE
                webaddress2=socket.gethostbyname(website)
                print webaddress2
                webaddress=website
                DEST=webaddress,httpport
                tcp=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                
                #CONEXAO ENTRE SERVIDOR E SITE
                tcp.connect(DEST)
                print "conectado a: \n",website
                #ENVIO DA MENSAGEM DE REQUISICAO FEITA PELO USUARIO PARA O SITE
                tcp.sendall(msg)
        
                # LACO PARA OBTENCAO DA RESPOSTA DO SITE
                while True:
                    #RECEBE AS MENSAGEM DE RESPOSTA DO SITE
                    msgr=tcp.recv(MAX_RECV)
                    
                     #SE O SITE NAO ESTIVER NA WHITE LIST, OS SEUS TERMOS DEVEM SER VERIFICADOS
                    if proxyflag == 0:
                        #VERIFICACAO DOS TERMOS DA MENSAGEM DE RESPOSTA
                        reqdeny1=permission_terms(msgr)
                    #print msgr
                    
                    # SE A MENSAGEM DE RESPOSTA FOR VAZIA, OU UMA FLAG DE TERMOS FOR ATIVA, A CONEXAO ACABOU
                    if (len(msgr)>0 and reqdeny == 0 and reqdeny1 == 0):
                        cliente.send(msgr)
                        print "connected"
                    else:
                        break
                tcp.close()
                
            # MENSAGEM DE ERROS NO SOCKET    
            except socket.error, (value, message):
                print message
        
        # SE A FLAG DE BLACKLIST FOR ATIVA        
        if proxyflag == 1:
      #      print "blacklist"
            #MENSAGEM HTML DE ACESSO NEGADO PARA O USUARIO
            cliente.send(str.encode(blmsg))

            
        else: 
            # SE ALGUMA FLAG DE TERMOS PROIBDOS FOR ATIVA
            if (reqdeny == 1 or reqdeny1 == 1):
           #     print "denied"
                #MENSAGEM HTML DE ACESSO NEGADO PARA O USUARIO
                cliente.send(str.encode(denymsg))
                blacklist_add(website)

    cliente.close()
       
#FUNCAO PARA VERIFICAR SE O SITE PODE SER ACESSADO           
def permission(website):  
    
    wl=open('whitelist.txt','r')
    bl=open('blacklist.txt','r')
    flag=0
    
    # SE O SITE ESTIVER NO ARQUIVO DE WHITELIST, FLAG=2
    # CADA LINHA DO ARQUIVO CONTEM UM SITE
    for line in wl:
        if website == line.rstrip('\n'):
            flag=2     
            
    #SE O SITE ESTIVER NO ARQUIVO DE BLACKLIST, FLAG=1
    # CADA LINHA DO ARQUIVO CONTEM UM SITE
    for line in bl:
        if website == line.rstrip('\n'):
            flag=1
    
    #SE O SITE NAO ESTIVER EM NENHUM DOS ARQUIVOS, FLAG=0
            
    wl.close()
    bl.close()
    
    return flag        

#FUNCAO PARA VERIFICAR SE A MENSAGEM CONTEM TERMOS PROIBIDOS    
def permission_terms(msg):  
    
    denyterms=open('denyterms.txt','r')
    
    flag=0
    
    #PERCORRE O ARQUIVO DENY_TERMS PARA VER SE A MENSAGEM CONTEM ALGUMA PALAVRA QUE ESTA NO ARQUIVO
    #CADA LINHA DO ARQUIVO CONTEM UMA PALAVRA PROIBIDA
    #A MENSAGEM EH QUEBRADA PALAVRA POR PALAVRA    
    for line in denyterms:
        for element in msg.split():
            if element == line.rstrip():
                flag=1
            
    denyterms.close()
    
    return flag            

#FUNCAO PARA ADICIONAR O SITE PARA O ARQUIVO DE BLACKLIST
def blacklist_add(website):
    
    bl=open('blacklist.txt','a')
    bl.write('\n'+website)
    bl.close()
                     
main()