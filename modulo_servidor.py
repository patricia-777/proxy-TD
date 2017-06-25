'''
TD - 2/2017
@author: Gibson e Lais
'''

# IMPORTANDO MODULOS E BIBLIOTECAS
import socket, thread, sys, time

from modulo_cache import *
from modulo_log import *
from modulo_proxy import *



# VARIAVEIS CONSTANTES
ServerPort=8080




if __name__ == '__main__':
    
    # NOME DO SERVIDOR E PORTA #
    ServerName='192.168.15.5'
    ServerAddress=ServerName,ServerPort
    
    # CRIACAO DO SOCKET DO SERVIDOR #
    try:
        ServerSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        ServerSocket.bind(ServerAddress)
        ServerSocket.listen(10)

        print "Aguardando conexao\n"

        # APAGANDO A CACHE ANTERIOR
        reiniciando_cache()

        # APAGANDO OS LOGS ANTERIORES
        reiniciando_log()

        # CONEXAO ENTRE SERVIDOR PROXY E USUARIO
        while True:

            cliente,address=ServerSocket.accept()

            # MOSTRANDO O CLIENTE QUE FEZ A REQUISICAO
            print "\nusuario: ",address[0],address[1]
            
            # AO ESCUTAR UM CLIENTE, GERA UMA NOVA THREAD PARA AQUELE USUARIO
            thread.start_new_thread(webproxy,(cliente,address))
        
        ServerSocket.close()
    
    # MENSAGENS DE ERROR NO SOCKET 
    except socket.error, (value, message):
        print message










