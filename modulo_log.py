'''
Created on 16 de jun de 2017
@author: Gibson e Lais
'''

from datetime import datetime


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
	
