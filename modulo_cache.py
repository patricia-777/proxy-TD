'''
TD - 2/2017
@author: Gibson e Lais
'''

# IMPORTANDO BIBLIOTECAS
import os, shutil

# VARIAVEIS CONSTANTES
FILE_EXIST = "False"


# FUNCAO QUE VERIFICA SE O SITE JA ESTA SALVO EM CACHE
def verificar_cache(website):
    # TENTA ABRIR O ARQUIVO COM REFERENTE AO SITE, SE CONSEGUIR ELE LE O ARQUIVO, RETORNA OS DADOS E MUDA O STATUS DA VARIAVEL FILE_EXIST
    # SE NAO EXISTIR O ARQUIVO ELE RETORNA VAZIO
    try:
        arquivo_cache = open("./cache/"+ website + ".txt", "r")
        dados_cache = arquivo_cache.readlines()

        arquivo_cache.close()

        FILE_EXIST = "True"

        return dados_cache

    except Exception, e:
        return ""


# FUNCAO QUE GRAVA NO CACHE OS DADOS DO SITE, CRIANDO UM ARQUIVO TXT COM O NOME SO SITE
# CASO O ARQUIVO EXISTA MAS NAO TENHA SIDO ENCONTRADO, GERA UM ERRO
def criar_cache(website, msg):
    if FILE_EXIST == "False":
        arquivo_cache = open("./cache/"+ website + ".txt", "w")
        arquivo_cache.write(msg)

        arquivo_cache.close()
    else:
        print "404: File Not Found"


def reiniciando_cache():
    diretorio = './cache'       
    
    shutil.rmtree(diretorio)
    os.makedirs(diretorio)
