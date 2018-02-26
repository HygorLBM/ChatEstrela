#!/usr/bin/python

#-------------------------------------------------------------------------------------------------
# Nome do projeto : Chat Estrela!
# Autor: Hygor L.B. Marques
#-------------------------------------------------------------------------------------------------



#-------------------------------------------------------------------------------------------------

import math
import random

#Funcao que encontra todos primos entre 2 e um numero (n) passado por parametro.
#Um desses numeros (random) sera usado em "primorelativo(t)". Esse metodo de encontrar numeros primos e conhecido como "peneira de Eratosthenes",
#(Sieve of Erastothenes)
def eratosthenes(n):
    primos = range(2, n)
    p = t = 2
    while p**2 <= n:
        while t <= n:
            s = t * p
            if s in primos:
                del primos[primos.index(s)]
            t += 1
        p = t = primos[primos.index(p) + 1]
    return primos

#Funcao que define os primos relativos que vao ser usados para determinar a chave publica.
def primorelativo(t):
    nums = eratosthenes(t)
    return random.choice(nums)

#Retorna o maior divisor comum entre p1 e p2, posteriormente usados como os numeros primos que gerarao as chaves.
def euclid(p1, p2, debug=False):
    x1, x2, x3 = 1, 0, p2
    y1, y2, y3 = 0, 1, p1
    while y3 > 1:
        quociente = math.floor(x3/y3)
        t1, t2, t3 = (x1 - (quociente * y1), x2 - (quociente * y2), x3 - (quociente * y3))
        x1, x2, x3 = y1, y2, y3
        y1, y2, y3 = t1, t2, t3
    if y3 == 1:
        return (y2, True)
    if y3 == 0:
        return (x3, False)

#Funcao que encontra a quantidade de coprimos menores que o numero a partir dos fatores primos p e q.
def totiente(p, q):
    return (p - 1) * (q - 1)

#Funcao que recebera dois numeros primos e atraves do metodo de criptografia conseguira chaves publica e privada.
def keygen(p, q, e=None):
    n = p * q
    t = totiente(p, q)
    if e is None:
        e = primorelativo(t)
    d = int(euclid(e, t)[0] % t) 
    return (n, e, d, str((n, e, d)))


def rsa(message, public, private, decript=False):
    if decript is False:
        return int(message**public[1] % public[0])
    else:
        return int(message**private[1] % private[0])




import os, thread, socket, traceback, urllib, sys

from struct import unpack

# Essa funcao foi feita apenas pra simplificar o output de strings usados com frequencia em um chat.
def Imprimir(str):
	print str

# Funcao para pegar o input do teclado
def GetInput():
	data = raw_input().rstrip()
	return str(data)

#--------Funcao que apresenta os comandos do chat.-------------------------
def comandos():
	os.system('cls' if os.name == 'nt' else 'clear')
	Imprimir(('Local IP:'+LOCAL_IP, 'Porta:'+str(PORT)))

	print r'''
<|-------------------------------------------------------------------
 O ChatEstrela tem as seguintes funcoes:
<|-------------------------------------------------------------------

/add <IP>       Adiciona um IP(usuario) ao ChatEstrela. 
              
/ss <IP>        Inicia uma conexao privada+criptografada com o IP especificado.
                Voce so mandara mensagens para esse IP, se nesse modo.

/nick <Nick>    Muda o seu nick no chat.
                O seu nick inicial e o seu proprio IP local.

/meuip          Lista seu nick e seus IPs.

/ip             Lista todos enderecos de IP que estao recebendo suas mensagens.
             
/sair           Sai do chat se estiver no chat geral.
                Se estiver no chat privado, retorna ao chat geral

/help           Limpa a tela e exibe os comandos do chat. 
-----------------------------------------------------------------------'''



LOCAL_IP = socket.gethostbyname(socket.gethostname()) #Comando que pega o IP local da maquina.

PORT = 7720 # Porta que os pacotes serao mandados.

NICK_LISTA = {LOCAL_IP:LOCAL_IP} #Atribuicao inicial do nick de um usuario a seu IP local.

vlock = thread.allocate_lock() #Thread usada para lockar a lista IP_LISTA


DEBUG = 0

IP_LISTA = [] #Lista que recebe todos enderecos IP que estao conectados na sua maquina.



Imprimir('Bem-vindo ao *ChatEstrela*!!!')

#Atribuicao das variaveis que sao necessarias pra determinar chaves de encriptografia.
k = keygen(61, 53)
PubKey = (k[0], k[1])
PrivateKey = (k[0], k[2])

PubKey_Outro = () #A chave publica da outra pessoa, iniciada com 0.
PubKey_string = k[3] #O vetor k[0], k[1], k[2]

#Recebe uma string e retorna a string como uma tupla pra ser usada pela encriptografia RSA.
def ParaTupla(string):
	temp_tuple = tuple(string.split('|'))
	temp_list = []
	for k in temp_tuple:
		if k == '':
			continue
		temp_list.append(int(k))
	
	return tuple(temp_list)

#Funcao que recebe uma string e retorma uma tupla de Bytes.
def ParaBytes(value):
	return unpack('%sB' % len(value), value)
	
#Funcao que recebe tuplas e retorna uma string equivalente (necessario pq tuplas sao imutaveis)
def ParaString(temp_tuple):
	temp_string = ''
	for k in temp_tuple:
		temp_string = temp_string + str(k) + '|' 
		
	return temp_string


# Encriptar string
def encript(string):
	global PubKey_Outro
	if len(PubKey_Outro) == 0: 
		raise ValueError
	ciphertext = []
	for temp in string:
		ciphertext.append(rsa(temp, PubKey_Outro, None))
	ciphertext_string = ParaString(tuple(ciphertext))
	return ciphertext_string	

#Decifra a mensagem atraves da sua chave privada.
def decript(string):
	global PrivateKey
	cleartext = ''
	tuple_string = ParaTupla(string)
	for temp in tuple_string:
		cleartext = cleartext + chr(rsa(temp, None, PrivateKey, decript=True))
	return str(cleartext)


# Atribui sua chave privada na sua mensagem, de forma a so poder descripar usando sua chave publica.
# Importante porque determina que a mensagem foi mandada por tal usuario (que a chave publica foi usada)
def sign(string):
	global PrivateKey
	ciphertext = []
	for temp in string:
		ciphertext.append(rsa(temp, PrivateKey, None))
	ciphertext_string = ParaString(tuple(ciphertext))
	return ciphertext_string

	
#Decifra uma mensagem atraves da chave publica de outra pessoa.
#Importante pra determinar quem enviou aquela mensagem.
def unsign(string):
	global PubKey_Outro
	cleartext = ''
	tuple_string = ParaTupla(string)
	for temp in tuple_string:
		cleartext = cleartext + chr(rsa(temp, None, PubKey_Outro, decript=True))
	return str(cleartext)





#Funcao que de fato envia as mensagens para todos IP's presentes em sua lista de IP's.
def EnviaTexto(str):
	global PORT
	for ip_addr in IP_LISTA:
		try:
			d = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			d.sendto(str, (ip_addr, PORT))
			d.close()
		except:
			Imprimir('[!!]O seguinte IP nao esta conectado na rede: ' + ip_addr)
			vlock.acquire()
			IP_LISTA.remove(ip_addr)
			del NICK_LISTA[ip_addr]
			vlock.release()
			if DEBUG == 1:
				traceback.print_exc()
			else:
				pass


# Funcao que permite receber todos pacotes em uma thread separada de modo que o usuario ainda possa enviar mensagens(input).
def OuvirSocket():
	global PORT
	global LOCAL_IP
	global IP_LISTA
	global vlock
	global NICK_LISTA
    
	Imprimir('.---------------------------------------------------------')
	Imprimir('|Seu nick: '+NICK_LISTA[LOCAL_IP])
	Imprimir('|Seu IP local: '+LOCAL_IP)
	Imprimir('|Porta usada:' +str(PORT))
	Imprimir('.--------------Use /help para ver os comandos--------------')

	while 1:
		d = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #abre o socket UDP
		d.bind(('', PORT)) # Socket criado fica ouvindo a porta PORT
		while 1:
			data, addr = d.recvfrom(1024) # socket recebe msg e armazena em data
			if not data: break # se nao houver data para a execucao do programa
			if not addr[0] in IP_LISTA and addr[0] != LOCAL_IP: # se o ip nao for o seu ou se ja esta na lista
				vlock.acquire()  # trava acesso as listas para evitar acesso durante uma mudanca
				IP_LISTA.append(addr[0]) # adiciona o ip na lista de enderecos ip
				NICK_LISTA[addr[0]] = addr[0] # adiciona o nickname na lista de nicks, relacionado ao seu endereco ip
				vlock.release() # destrava o acesso as listas
				Envia_SugeSincroni() # envia sugestao de sincronizacao para avisar aos outros peers que ha uma nova conexao

			if data[:16] == r'\sugestao_sincro': # notifica que ha uma nova conexao
				RequiSincro() # requisita que todos os peers facam sincronizacao
				Imprimir(NICK_LISTA[addr[0]] + ' entrou.')
				continue

			if data[:5] == r'/sair': # sai da aplicacao e exclui o endereco de ip da lista
				vlock.acquire()
				IP_LISTA.remove(addr[0])
				del NICK_LISTA[addr[0]]
				vlock.release()
				

			if data[:13] == r'\sinc_requisi': # requisicao de sincronizacao
				SincData() # sincroniza os dados com todos os peers
				continue	

			if data[:10] == r'\sinc_data': # os peers enviaram os dados para sincronizacao
				TEMP_IP_LISTA = str(data[11:]).split('|') 
				for temp_ip in TEMP_IP_LISTA:
					if not temp_ip in IP_LISTA and temp_ip != LOCAL_IP: # se nao for o seu ip e nem ja estiver na lista de ips
						vlock.acquire()  # trava o acesso as listas para evitar memoria corrompida
						IP_LISTA.append(temp_ip) # inclui o endereco de ip na lista de enderecos de ip
						vlock.release() # destrava o acesso as listas
				continue

			if data[:10] == r'\nick_data': # alguem mudou o nick e sincroniza com os outros peers 
				TEMP_NICK_LISTA = str(data[11:]).split(';')
				for temp_nick in TEMP_NICK_LISTA:
					small_list = temp_nick.split('|')
					vlock.acquire() # trava acesso alista
					NICK_LISTA[small_list[0]] = small_list[1] 
					vlock.release() # destrava o acesso as listas
				continue

			if data[:7] == r'\pubkey':
				global PubKey_Outro, PubKey_string
				if len(PubKey_Outro) != 0:
					continue
				PubKey_Outro = tuple(map(int, data[8:-1].split(','))) 
				try:

					e = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
					e.sendto('\pubkey'+PubKey_string, (addr[0], PORT))
					e.close()
				except:
	
					Imprimir('Impossivel enviar a chave publica para: ' + addr[0])
				continue				


			if data[:10] == r'\encriptad': 
				try:
					data = decript(data[10:])
				except:
					Imprimir('Impossivel traduzir mensagem')
					if DEBUG == 1:
						traceback.print_exc()
					continue
				try:
					data = unsign(data)
				except:
					Imprimir('Impossivel decifrar a mensagem')
					if DEBUG == 1:
						traceback.print_exc()
					continue
					
				Imprimir(NICK_LISTA[addr[0]] + '**: ' + str(data))

				continue

			Imprimir(NICK_LISTA[addr[0]] + ': ' + str(data))

		d.close()

def Envia_SugeSincroni(): #envia o tag de sugestao de sincronizacao
	EnviaTexto('\sugestao_sincro')

def RequiSincro(): #envia o tag de requisicao de sincronizacao
	EnviaTexto('\sinc_requisi')

def SincData(): #sincroniza os dados para todos os peers
	global IP_LISTA
	EnviaTexto('\sinc_data ' + '|'.join(IP_LISTA))
	EnviaTexto(r'\nick_data ' + ";".join(["%s|%s" % (k, v) for k, v in NICK_LISTA.items()]))


#Funcao que verifica o input(mensagem) enviada e se ela esta relacionada a algum comando do chat.
def Input(input_string):
	global LOCAL_IP
	global IP_LISTA
	global NICK_LISTA
	global vlock
	global PubKey
	global PubKey_string
	global PubKey_Outro
	global PORT

	if input_string[:4] == r'/add': #adicionar novo endereco ip
		if not input_string[5:] in IP_LISTA and input_string[5:] != LOCAL_IP:
			vlock.acquire()  #trava o acesso as listas
			IP_LISTA.append(input_string[5:]) #adiciona o endereco ip na lista de enderecos ips
			NICK_LISTA[input_string[5:]] = input_string[5:] #adiciona o nick na lista de nicks
			vlock.release() # destrava o acesso as listas
			Envia_SugeSincroni() #envia sincronizacao
			return 0

	if input_string[:5] == r'/help': #para abrir o menu
		comandos()

	if input_string[:3] == r'/ss': # envio de msg privada
		print '***Conversa privada***'
		print 'Enviando apenas para' + input_string[4:] 
		try:
			d = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #abertudo do socket para envio da chave publica
			d.sendto('\pubkey'+PubKey_string, (input_string[4:], PORT)) #envio da chave publica por udp
			d.close() #fecha o socket
		except:

			Imprimir('Nao foi possivel enviar para: ' + input_string[4:])
			print '***Fim da conversa privada.***'
			return 0
		while 1:
			EInput = GetInput()
			if EInput[:5] == r'/sair':
				PubKey_Outro = (0)
				print '***Fim da conversa privada***'
				return 0
			try:
				EInput = sign(ParaBytes(EInput))
			except:
				Imprimir('Problema de autenticacao!')
				print '***Fim da conversa privada***'
				return 0
			try:
				EEInput = encript(ParaBytes(EInput))
			except ValueError:
				Imprimir('Voce nao possui a chave publica desse usuario.(Verifique se o IP esta correto!)')
				print '***Fim da conversa privada***'
				return 0
			except:
				Imprimir('Nao foi possivel encriptar sua mensagem =( ')
				if DEBUG == 1:
					traceback.print_exc()
				print '***Fim da conversa privada***'
				return 0
				
			
			try:
				e = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				e.sendto(r'\encriptad'+ EEInput, (input_string[4:], PORT))
				e.close()
			except:
				Imprimir('Nao foi possivel enviar para: ' + input_string[4:])
				if DEBUG == 1:
					traceback.print_exc()
				print '***Fim da conversa privada***'
				return 0
		return 0

	if input_string[:5] == r'/sair': #solicitacao de saida
		EnviaTexto(NICK_LISTA[LOCAL_IP] + ' saiu do ChatEstrela.')
		sys.exit(1)
		return 0

	if input_string[:5] == r'/nick': #alteracao do nick
		NICK_LISTA[LOCAL_IP] = input_string[6:]
		Envia_SugeSincroni()
		Imprimir('<--------------------------------------')
		Imprimir('Nick alterado para: '+NICK_LISTA[LOCAL_IP])
		Imprimir('-------------------------------------->')

	if input_string[:3] == r'/ip': # mostra todos os ips da lista
		Imprimir('Veja a lista dos IPs adicionados ao seu chat: ')
		Imprimir(IP_LISTA)
		return 0

	if input_string[:6] == r'/meuip': # mostra seu ip e seu nick atuais
		Imprimir('----------------------------------------------------------')
		Imprimir('|Nick: ' + NICK_LISTA[LOCAL_IP] + '| Local IP: ' +LOCAL_IP)
		Imprimir('----------------------------------------------------------')
		Imprimir('')

		
	if (input_string[:6] != r'/meuip' and input_string[:6] != r'/meuip' and input_string[:5] != r'/nick' and input_string[:5] !=r'/sair'):
		EnviaTexto(input_string) #envio das mensagens





if __name__ == "__main__":
	thread.start_new_thread(OuvirSocket, ())
	while 1:
		Input(GetInput())