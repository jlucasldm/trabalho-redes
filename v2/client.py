"""
MATA59 - REDE DE COMPUTADORES - UNIVERSIDADE FEDERAL DA BAHIA
IMPLEMENTAÇÃO DE UMA APLICAÇÃO CLIENTE-SERVIDOR

Discentes: 
    João Lucas Melo
    Shaísta Câmara

Docente: Gustavo Figueredo


[RESUMO]

Este trabalho possui como finalidade a implementação de uma aplicação de
depósito de arquivo com recuperação. Através do modelo cliente-servidor, a 
aplicação fornece os seguintes serviços:
  i) depósito de arquivos
 ii) recuperação de arquivos
iii) remoção de arquivos

No modo de depósito, o cliente informa ao servidor o arquivo a ser 
depositado e o número de cópias. O servidor guarda a quantidade informada
de cópias do arquivo em locais (abstrações para dispositivos) distintos.

No modo de recuperação, o cliente informa ao servidor o nome do arquivo a
ser recuperado do servidor. O servidor encontrará o arquivo, de algum dos
possíveis locais onde ele esteja armazenado, e o devolve ao cliente.

No modo de remoção, o cliente informa ao servidor o nome do arquivo a ser
removido do servido. O servidor então remove o arquivo solicitado em todas
os locais (abstrações para dispositivos) onde exista uma cópia do mesmo.

A implementação do projeto se deu através da programação, em python, de 
dois algoritmos: server.py e client.py. Como referenciado em seus nomes, 
ambos atuam como instâncias do servidor e cliente da aplicação, 
respectivamente. 

Através do uso de sockets, cliente e servidor comunicam entre si por uma 
conexão TCP. A escolha do protocolo em detrimento do UDP foi consequência 
da necessidade do serviço de transferência confiável de dados (já que a 
aplicação manuseia arquivos, transferindo-os de um hospedeiro a outro). 
Como somente o TCP é capaz de fornecer esse serviço, provendo a garantia
de que os dados serão entregues de um host a outro na ordem correta e sem 
estarem corrompidos, a escolha desse protocolo foi fundamental.

Seguindo as especificações solicitadas e incorporando os conceitos vistos 
em sala de aula, foi possível desenvolver uma aplicação coesa do modelo
cliente-servidor básico, mas fundamental para consolidação das discussões 
da disciplina.


[FUNCIONAMENTO GERAL]
A aplicação consiste em dois programas, server.py e client.py. Python foi
escolhido como linguagem de programação para a implementação por sua
facilidade de manipulação e pela familiaridade dos autores do trabalho
com a tecnologia. Ambos os programas atuam como instâncias de um servidor 
e um cliente, respectivamente. 

Os processos se comunicam por uma conexão TCP através do uso de sockets.
Uma vez que se trata de uma aplicação que manuseia arquivos, transferindo
de um processo a outro, é fundamental que o protocolo da camada de
transporte forneça um serviço confiável de transferência de dados. Por
esse motivo, o TCP foi escolhido em detrimento do UDP.

Inicialmente, server.py deve ser executado para instancializar o servidor.
É solicitado no prompt a porta desejada para a criação do socket TCP. O 
endereço IP do servidor é atribuído ao IP do sistema final onde o processo
está sendo executado. Uma saída é printada no terminal no seguinte formato:
"[LISTENING] server is listening on IP: ***.***.***.***, Port: ****"
Nesse momento, o socket TCP é criado e o servidor é instancializado. O
servidor então fica à espera da conexão de um cliente.

Instancializado o servidor, client.py pode ser executado. É solicitado no
prompt o endereço IP e porta para o estabelecimento da conexão TCP entre
os processos. Ambas as informações foram dadas pelo retorno no terminal de
server.py. Além disso, um valor para o nome do cliente será solicitado. A
importância dessa variável será discutida mais adiante. 

Passados os valores de endereço IP e porta correspondentes ao servidor, e
ainda fornecido um nome do cliente, processos cliente e servidor 
estabelecerão uma conexão TCP.

Ao estabelecer a conexão, recebendo o nome do cliente, o processo servidor
atribui o valor recebido à variável client_name e informa o cliente que o
nome foi recebido com sucesso. A variável client_name será usada durante 
todas as operações solicitadas pelo cliente, uma vez que, por decisão de 
implementação, client_name é usado para nomear diretórios nos diferentes 
locais (abstrações de dispositivos) do servidor. Por exemplo, para um 
cliente cujo nome é "thomas", o servidor deverá, para um(s) certo(s) 
diretório(s), possuir uma instância de um diretório chamado "thomas", 
referente ao local onde os arquivos do cliente "thomas" deverão ser 
armazenados, recuperados ou removidos.

Após retornar ao cliente o recebimento de client_name, o processo servidor 
faz uma busca em seus locais por um diretório de nome client_name. O 
resultado é impresso no terminal e retornado ao cliente. Duas situações
podem ocorrer:
  i) não haver um diretório client_name no servidor / não haver dados no
     diretório client_name:
        . O processo servidor printa no prompt a mensagem:
        [WARNING] No files found to {client_name}
        . O processo cliente recebe do servidor a mensagem:
        No files to {client_name} found
 ii) haver um diretório client_name com arquivos:
        . O processo servidor recupera todos os arquivos no local 
        client_name e printa no prompt a mensagem (onde files é uma lista
        contendo os arquivos no local client_name):
        [SUCESS] {client_name}'s files found: {files}
        . O processo cliente recebe do servidor a mensagem (onde 
        files_itens são os arquivos no local client_name):
        Files to thomas found: {files_itens}

Após a interação, é requisitado ao cleinte, no prompt, um valor op 
sinalizando o serviço a ser executado pelo servidor. op pode ter três 
formatos:
  i) DEP := serviço de depósito
 ii) REC := serviço de recuperação
iii) DEL := serviço de remoção

Atribuído o valor da operação à op, é ainda requisitado do cliente os 
valores dos parâmetros das respectivas operações. São elas:
DEP := filename (nome do arquivo a ser depositado no servidor)
       copies (número de cópias a serem depositadas no servidor)
REC := filename (nome do arquivo a ser recuperado pelo servidor)
DEL := filename (nome do arquivo a ser removido do servidor)

Definida a operação e os respectivos argumentos necessários, o cliente
envia os dados através do socket TCP para o servidor, que retornará ao
cliente as respectivas mensagens de sucesso e dados correspondentes às
operações solicitadas (no caso de recuperação de arquivo). O funcionamento
de cada operação será melhor abordado mais adiante.

Finalizada a operação, o cliente encerra a conexão TCP e o servidor retorna
ao estado de escuta, esperando uma conexão de um novo cliente.
"""

import socket

# definindo um padrão de tamanho para as mensagens dos sockets
HEADER = 1024
# definindo formato de decodificação das mensagens dos sockets
FORMAT = 'utf-8'

def main():
    SERVER = input("enter the ip address in the format x.x.x.x: ")
    PORT = int(input("enter the port: "))
    CLIENT_NAME = input("enter your name: ")

    # definindo o formato de endereço
    ADDR = (SERVER, PORT)
    
    # criando o socket client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    # enviando CLIENT_NAME pelo socket
    send(client, CLIENT_NAME)

    # recebendo resposta do servidor
    print(client.recv(HEADER).decode(FORMAT))
    # list_files(client)

    # selecionando operação
    op = input("enter a operation: ")
    if op == "DEP":
        deposit(client, op)
        pass
    elif op == "REC":
        recover(client, op)
        pass
    elif op == "DEL":
        delete(client, op)
        pass

    client.close()

def deposit(client, op):
    # pegando os parametros para mandar ao servidor
    filename = input("enter the file name to deposit: ")
    copies = input("enter the number of copies: ")

    # mandando para o servidor
    send(client, op)
    send(client, copies)
    send(client, filename)
    send_file(client, filename)
    pass

def recover(client, op):
    # pegando os parametros para mandar ao servidor
    filename = input("enter the file name to recover: ")

    # mandando para o servidor
    send(client, op)
    send(client, filename)
    recv_file(client, filename)
    pass

def delete(client, op):
    # pegando os parametros para mandar ao servidor
    filename = input("enter the file name to delete: ")

    # mandando para o servidor
    send(client, op)
    send(client, filename)
    pass

# recebe os dados do socket
def list_files(client):
    msg_length = client.recv(HEADER).decode(FORMAT)
    msg_length = int(msg_length)
    files = client.recv(msg_length).decode(FORMAT)
    print(files)

# função auxiliar para envio de mensagens ao servidor
def send(client, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(HEADER).decode(FORMAT))

# função auxiliar para envio de arquivos ao servidor
def send_file(client, filename):
    f = open(filename, "rb")
    while True:
        bytes_read = f.read(HEADER)
        if not bytes_read:
            break
        client.send(bytes_read)
        client.recv(HEADER).decode(FORMAT)
    f.close()

# função auxiliar para o recebimento de arquivos do servidor
def recv_file(client, filename):
    f = open(filename, "wb")
    file_bytes = bytes()
    while True:
        bytes_read = client.recv(HEADER)
        print(f"bytes recieved: {bytes_read}")
        if not bytes_read:
            print("sai")
            break
        file_bytes += bytes_read
    # print(f"file_bytes: {file_bytes}")
    f.write(file_bytes)
    f.close()


main()
