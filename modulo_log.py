'''
TD - 2/2017
@author: Gibson e Lais
'''

# IMPORTANDO BIBLIOTECAS
import os
from datetime import datetime

# SALVANDO NO ARQUIVO LOG.TXT AS INFORMACOES DE REQUISICAO
def log(address, website, status):

	now = datetime.now()
	mensagem_log = str(now.day) + "/" + str(now.month) + "/" + str(now.year) + " - " + str(now.hour) + ":" + str(now.minute) + " --> " + address[0] + " requisitou " + website + " (" + status + ")\n"

	try:
		
		arquivo_log = open("log.txt", "r")
		conteudo_log = arquivo_log.readlines()

		conteudo_log.append(mensagem_log)

		arquivo_log = open("log.txt", "w")
		arquivo_log.writelines(conteudo_log)
		pass
	except Exception, e:

		arquivo_log = open("log.txt", "w")
		arquivo_log.write(mensagem_log)
	
	arquivo_log.close()
	

# DELETANDO O ARQUIVO DE LOG NO COMECO DA EXECUCAO
def reiniciando_log():
	arquivo_log = 'log.txt'

	if os.path.isfile(arquivo_log):
		os.remove(arquivo_log)
