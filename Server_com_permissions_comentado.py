'''
Created on 30 de mai de 2017
@author: Gibson e Lais
'''

# IMPORTANDO MODULOS E BIBLIOTECAS
import socket,thread,sys

from modulo_cache import *
from modulo_permissao import *



# VARIAVEIS CONSTANTES
MAX_RECV=2097152
httpport=80
ServerPort=8080



           
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
        print "WEBSITE: ",website    

        
        # VERIFICAR SE EXISTE CACHE PARA ESSE SITE
        existe_cache = verificar_cache(website)

        #SE EXISTIR CACHE, USA AS INFORMACOES SALVAS, SE NAO CONECTA NORMALMENTE           
        if existe_cache != "":

            for msg_cache in existe_cache:
                cliente.send(msg_cache)
        else:
     
            #FLAG DE VERIFICACAO SE O SITE PODE SER ACESSADO
            proxyflag=permission(website)
            
            if proxyflag == 0 or proxyflag == 2:
                
                #SE O SITE NAO ESTIVER NA WHITE LIST, OS SEUS TERMOS DEVEM SER VERIFICADOS
                if proxyflag == 0:
                    #VERIFICACAO DOS TERMOS DA MENSAGEM DE REQUISICAO
                    reqdeny=permission_terms(msg)


                # CRIACAO DE CONEXAO ENTRE O SERVIDOR E O SITE QUE O USUARIO DESEJA ACESSAR     
                try:
                    
                    # ESTABELECENDO A CONEXAO ENTRE O CLIENTE E O SERVIDOR HTTP
                    tcp = estabelecedo_conexao(website, msg, httpport)
            
                    # LACO PARA OBTENCAO DA RESPOSTA DO SITE
                    while True:
                        
                        #RECEBE AS MENSAGEM DE RESPOSTA DO SITE
                        msgr=tcp.recv(MAX_RECV)
                        
                         #SE O SITE NAO ESTIVER NA WHITE LIST, OS SEUS TERMOS DEVEM SER VERIFICADOS
                        if proxyflag == 0:
                            #VERIFICACAO DOS TERMOS DA MENSAGEM DE RESPOSTA
                            reqdeny1=permission_terms(msgr)
                        
                        
                        # SE A MENSAGEM DE RESPOSTA FOR VAZIA, OU UMA FLAG DE TERMOS FOR ATIVA, A CONEXAO ACABOU
                        if (len(msgr)>0 and reqdeny == 0 and reqdeny1 == 0):

                            cliente.send(msgr)

                            # SALVAR NA CACHE DADOS DO SITE
                            recuperar_cache(website, msgr)

                            print "connected"
                        else:
                            break

                    tcp.close()
                    
                # MENSAGEM DE ERROS NO SOCKET    
                except socket.error, (value, message):
                    print message
            
            # SE A FLAG DE BLACKLIST FOR ATIVA        
            if proxyflag == 1:
          
                #MENSAGEM HTML DE ACESSO NEGADO PARA O USUARIO
                cliente.send(str.encode(blmsg))

                
            else: 

                # SE ALGUMA FLAG DE TERMOS PROIBIDOS FOR ATIVA
                if (reqdeny == 1 or reqdeny1 == 1):
               
                    #MENSAGEM HTML DE ACESSO NEGADO PARA O USUARIO
                    cliente.send(str.encode(denymsg))
                    blacklist_add(website)

    # FECHANDO CONEXAO
    cliente.close()
 


def estabelecedo_conexao(website, msg, httpport):
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

    return tcp





if __name__ == '__main__':
    
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










