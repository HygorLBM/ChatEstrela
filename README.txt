
README (Instructions in Portuguese - PT/BR)

Executar o arquivo ChatEstrelaFINAL.py
1. O nick inicial eh o ip local da maquina, caso queira alterar entrar com /nick novonick
2. /help para mostrar os comandos do chat.
3. A topologia é estrela, portanto todos os peers tem acesso a uma lista de ips e nicks que contem o endereco de todos
4. /add enderecoip ira adicionar um novo ip ao chat
5. /ss enderecoip envia uma msg privada para o endereco desejado, o comando /sair sai do modo de envio de msgs privadas
e retorna para o chat geral
6. Caso o peer que adicionou os enderecos caia, os outros continuam a aplicacao normalmente.

Exemplo de Execucao do Chat com o node03 e node02 do cluster

Bem-vindo ao *ChatEstrela*!!!    /Inicio automatico com o nick como o ip
.---------------------------------------------------------
|Seu nick: 192.168.0.30
|Seu IP local: 192.168.0.30
|Porta usada:7720
.--------------Use /help para ver os comandos--------------
/nick node03   /alteracao do nick para node3
<--------------------------------------
Nick alterado para: node03  /confirmacao da alteracao do nick
-------------------------------------->
/add 192.168.0.20   /adicionou o endereco do node02 na lista
192.168.0.20 entrou.  /confirmacao
Teste1 /msg enviada
node02: teste2 /msg recebida
/ss 192.168.0.20 /envio de mensagem privada para node02
***Conversa privada***   
Enviando apenas para192.168.0.20  /confirmacao de msg privada
testeprivado  /envio de msg privada
node02**: testeprivado2 /recebimento de msg privada
/sair /sair do modo msg privada
***Fim da conversa privada*** /confirmacao de saida do modo de msg privada





