'''
TD - 2/2017
@author: Gibson e Lais
'''

# VARIAVEIS CONSTANTES
blmsg='HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><header><title>ERROR</title></header><body><div align="center" style="border:1px solid red"><p>Acesso negado.</br>Site na blacklist.</p></div></body></html>\n'
denymsg='HTTP/1.1 200 OK\nContent-Type: text/html\n\n<html><header><title>ERROR</title></header><body><div align="center" style="border:1px solid red"><p>Acesso negado.</br>Site contem termos proibidos.</p></div></body></html>\n'



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

