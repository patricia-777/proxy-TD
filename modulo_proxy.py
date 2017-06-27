'''
TD - 2/2017
@author: Gibson e Lais
'''

# IMPORTANDO MODULOS E BIBLIOTECAS
import socket, thread, sys, time

from modulo_cache import *
from modulo_permissao import *
from modulo_log import *
from modulo_proxy import *

# VARIAVEIS CONSTANTES
MAX_RECV=2097152
httpport=80
TIME_OUT=10


# FUNCAO DO PROXY          
def webproxy(cliente,address):
    
    # FLAGS PARA VERIFICACAO DE TERMOS
    reqdeny=0
    reqdeny1=0    
    
    # MENSAGEM DE REQUISICAO HTTP 
    msg=cliente.recv(MAX_RECV)
    

    # VERIFICACAO SE A MENSAGEM NAO EH VAZIA
    indice_final = msg.find('\n')
    if indice_final != -1:

        # OBTENCAO DO SITE QUE O USUARIO QUER ACESSAR
        msglist=msg.split('\n')
        website=(msglist[1].split())[1]    

        # MOSTRANDO AO CLIENTE A REQUISICAO
        print "requisicao: ",website

        
        # VERIFICAR SE EXISTE CACHE PARA ESSE SITE
        existe_cache = verificar_cache(website)

        #SE EXISTIR CACHE, USA AS INFORMACOES SALVAS, SE NAO CONECTA NORMALMENTE           
        if existe_cache != "":

            for msg_cache in existe_cache:
                cliente.send(msg_cache)

            # GERANDO LOG PARA A REQUISICAO
            log(address, website, "PERMITIDO")


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
                    start=time.clock()
                    # ESTABELECENDO A CONEXAO ENTRE O CLIENTE E O SERVIDOR HTTP
                    tcp = estabelecedo_conexao(website, msg, httpport)
            
                    # LACO PARA OBTENCAO DA RESPOSTA DO SITE
                    while True:
                        
                        # TIMEOUT
                        if time.clock()-start > TIME_OUT:
                            log(address,website,"TIMEOUT")
                            break
                        
                        #RECEBE AS MENSAGEM DE RESPOSTA DO SITE
                        msgr=tcp.recv(MAX_RECV)

                        
                         #SE O SITE NAO ESTIVER NA WHITE LIST, OS SEUS TERMOS DEVEM SER VERIFICADOS
                        if proxyflag == 0:
                            #VERIFICACAO DOS TERMOS DA MENSAGEM DE RESPOSTA
                            reqdeny1=permission_terms(msgr)
                        
                        
                        # SE A MENSAGEM DE RESPOSTA FOR VAZIA, OU UMA FLAG DE TERMOS FOR ATIVA, A CONEXAO ACABOU
                        if (len(msgr)>0 and reqdeny == 0 and reqdeny1 == 0):

                            cliente.send(msgr)
                            start=time.clock()

                            # SALVAR NA CACHE DADOS DO SITE
                            criar_cache(website, msgr)

                            # GERANDO LOG PARA A REQUISICAO
                            log(address, website, "PERMITIDO")

                            print "conectado"

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

                # GERANDO LOG PARA A REQUISICAO
                log(address, website, "NEGADO")

                
            else: 

                # SE ALGUMA FLAG DE TERMOS PROIBIDOS FOR ATIVA
                if (reqdeny == 1 or reqdeny1 == 1):
               
                    #MENSAGEM HTML DE ACESSO NEGADO PARA O USUARIO
                    cliente.send(str.encode(denymsg))
                    blacklist_add(website)

                    # GERANDO LOG PARA A REQUISICAO
                    log(address, website, "NEGADO")


    # FECHANDO CONEXAO
    cliente.close()
    
 


def estabelecedo_conexao(website, msg, httpport):
    # OBTENCAO DO IP PELO NOME DO SITE
    webaddress2=socket.gethostbyname(website)
    webaddress=website
    DEST=webaddress,httpport
    tcp=socket.socket(socket.AF_INET,socket.SOCK_STREAM)


    #CONEXAO ENTRE SERVIDOR E SITE
    tcp.connect(DEST)
    
    #ENVIO DA MENSAGEM DE REQUISICAO FEITA PELO USUARIO PARA O SITE
    tcp.sendall(msg)

    return tcp




