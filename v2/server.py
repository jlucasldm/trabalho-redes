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


[OPERAÇÃO DE DEPÓSITO]
A aplicação fornece três serviços: depósito de um arquivo no servidor,
recuperação de um arquivo no servidor e serviço de remoção. O cliente
seleciona a operação desejada de acordo com sgeuinte o padrão de fomato:
DEP := filename (nome do arquivo a ser depositado no servidor)
       copies (número de cópias a serem depositadas no servidor)
REC := filename (nome do arquivo a ser recuperado pelo servidor)
DEL := filename (nome do arquivo a ser removido do servidor)

Selecionada a operação, o cliente atribui seu valor à variável op e a 
transmite ao servidor através da conexão TCP. Ao receber op, o servidor
retorna ao cliente a mensagem:
[{endereço da conexão}] Operation {op} received

O servidor, ao rebeber o valor DEP, invoca a função deposit() e aguarda 
conexão do cliente, que enviará os valores necessários para executar a 
operação. Os demais argumentos necessários são:
filename := nome do arquivo, no diretório atual do processo cliente, a
            ser depositado no servidor
  copies := número de cópias do arquivo a ser armazenadas no servidor

Cabe comentar que o arquivo enviado irá sobrescrever a cópia no servidor,
caso exista.

Definidos os parâmetros e armazenados nas suas respectivas variáveis, o
cliente, individualmente, os envia ao servidor pelo socket TCP. Ao 
receber os dados, o servidor envia as seguintes respostas ao cliente:
[SUCESS] Number of copies recieved: {copies}
[SUCESS] File name recieved: {filename}

Um terceiro parâmetro é enviado ao servidor, o arquivo no diretório atual
do processo cliente. O arquivo, cujo nome é filename, é aberto e 
atribuído à variável file em client.py. O processo cliente então envia
file para o servidor através do socket TCP.

Ao receber o arquivo, o servidor itera sobre file de blocos em blocos de 
bytes (definido pela variável global HEADER, atribuído a 1024 bytes). Os
dados iterados são atribuídos à uma variável local file_bytes. Dessa
forma, a função deposit() consegue, com êxito, ter acesso à uma cópia de
file antes de efetivamente instancializar o arquivo no servidor.

Tendo acesso ao conteúdo do arquivo, deposit() então itera sobre os 
diretórios do servidor, buscando pelo diretório client_name para uma
quantidade copies de locais (dispositivos) existentes. Cada local é
nomeado por um inteiro, a partir do índice 0. Caso não exista o diretório
client_name em todos os copies locais no servidor, então são criados os
locais:
.\\server\\0\\client_name
.\\server\\1\\client_name
...
.\\server\\copies\\client_name

Para cada client_name, nos locais 0 a copies, o servidor cria um arquivo
filename e atribui a ele o conteúdo de file_bytes. O processo então
informa ao cliente o sucesso da operação. O cliente, ao receber a 
confirmação da operação, encerra a conexão TCP com o servidor, que retorna
ao estado de escuta e espera de uma nova conexão.


[OPERAÇÃO DE RECUPERAÇÃO]
A aplicação fornece três serviços: depósito de um arquivo no servidor,
recuperação de um arquivo no servidor e serviço de remoção. O cliente
seleciona a operação desejada de acordo com sgeuinte o padrão de fomato:
DEP := filename (nome do arquivo a ser depositado no servidor)
       copies (número de cópias a serem depositadas no servidor)
REC := filename (nome do arquivo a ser recuperado pelo servidor)
DEL := filename (nome do arquivo a ser removido do servidor)

Selecionada a operação, o cliente atribui seu valor à variável op e a 
transmite ao servidor através da conexão TCP. Ao receber op, o servidor
retorna ao cliente a mensagem:
[{endereço da conexão}] Operation {op} received

O servidor, ao rebeber o valor REC, invoca a função recover() e aguarda 
conexão do cliente, que enviará os valores necessários para executar a 
operação. O demais argumento necessário é:
filename := nome do arquivo, no diretório atual do processo cliente, a
            ser depositado no servidor

Definido o parâmetro e armazenado na sua respectiva variável, o cliente
o envia ao servidor pelo socket TCP. Ao receber filename, o servidor 
envia a seguinte resposta ao cliente:
[SUCESS] File name recieved: {filename}

O servidor então busca por todos os diretórios do servidor, buscando 
pelo diretório client_name em todos os locais (dispositivos) existentes. 
Cada local é nomeado por um inteiro, a partir do índice 0. O endereço
segue o seguinte formato:
.\\server\\0\\client_name

Encontrado o diretório em algum dos locais do servidor, o processo então
abre o arquivo filename e envia segmentos de bytes do tamanho HEADER (por
padrão adotado pela implementação, atribuído a 1024 bytes) ao cliente. O
cliente, por sua vez, recebe cada segmento e atribuí a uma variável
file_bytes. Após o envio e recebimento de todos os segmentos de bytes do
arquivo no servidor, o cliente cria um arquivo de nome filename em seu
diretório atual e atribui file_bytes ao seu conteúdo.

Por fim, o servidor informa ao cliente o sucesso da operação. O cliente, 
ao receber a confirmação da operação, encerra a conexão TCP com o servidor, 
que retorna ao estado de escuta e espera de uma nova conexão.


[OPERAÇÃO DE REMOÇÃO]
A aplicação fornece três serviços: depósito de um arquivo no servidor,
recuperação de um arquivo no servidor e serviço de remoção. O cliente
seleciona a operação desejada de acordo com sgeuinte o padrão de fomato:
DEP := filename (nome do arquivo a ser depositado no servidor)
       copies (número de cópias a serem depositadas no servidor)
REC := filename (nome do arquivo a ser recuperado pelo servidor)
DEL := filename (nome do arquivo a ser removido do servidor)

Selecionada a operação, o cliente atribui seu valor à variável op e a 
transmite ao servidor através da conexão TCP. Ao receber op, o servidor
retorna ao cliente a mensagem:
[{endereço da conexão}] Operation {op} received

O servidor, ao rebeber o valor DEL, invoca a função delete() e aguarda 
conexão do cliente, que enviará o valore necessário para executar a 
operação. O demais argumento necessário é:
filename := nome do arquivo, no diretório atual do processo cliente, a
            ser depositado no servidor

Definido o parâmetro e armazenado na sua respectiva variável, o cliente
o envia ao servidor pelo socket TCP. Ao receber filename, o servidor 
envia a seguinte resposta ao cliente:
[SUCESS] File name recieved: {filename}

O servidor então busca por todos os diretórios do servidor, buscando 
pelo diretório client_name em todos os locais (dispositivos) existentes. 
Cada local é nomeado por um inteiro, a partir do índice 0. O endereço
segue o seguinte formato:
.\\server\\0\\client_name

Para cada local encontrado, o servidor checa a existência de filename no
diretório. Caso encontrado, o servidor remove o arquivo e retorna ao
cliente uma mensagem do tipo:
[SUCESS] File {filename} deleted

Caso o arquivo não seja encontrado em nenhum local, o servidor retorna ao
cliente uma mensagem do tipo:
[WARNING] FILE {filename} not found

O cliente, ao receber a confirmação da operação, encerra a conexão TCP com 
o servidor, que retorna ao estado de escuta e espera de uma nova conexão.

"""

import socket
import os
import threading
from utils import message_formatter

HEADER = 1024
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DIRECTORY = '.\\server\\'
DISCONNET_MESSAGE = "!DISCONNECT"

def main():
    PORT = int(input("enter the port: "))
    ADDR = (SERVER, PORT)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] server is listening on IP: {SERVER}, Port: {PORT}")

    while True:
        conn, addr = server.accept()
        print(f"[START] server is running. Accepted connection at address: \n{addr}")
        
        # recebendo a primeira mensagem do cliente
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)

        # primeira mensagem deve ser o nome do cliente, para checagem
        # em seu diretório 
        msg = conn.recv(msg_length).decode(FORMAT)
        print("[", addr, "] Message received. Client name: ", msg)
        conn.send(f"[{addr}] Message received. Client name: {msg}".encode(FORMAT))

        # encerra a sessão se enviada a mensagem de desconexão
        if msg == DISCONNET_MESSAGE:
            conn.close()

        client_name = msg
        # checagem do diretorio do cliente
        list_files(conn, client_name)

        # recebendo a operação do cliente
        # as opeações seguem a forma:
        # DEP := depositar
        # REC := recuperar
        # DEL := deletar
          
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        op = conn.recv(msg_length).decode(FORMAT)
        print(f"[{addr}] Operation {op} received", op)
        conn.send(f"[{addr}] Operation {op} received".encode(FORMAT))

        if op == "DEP":
            deposit(conn, client_name)
        elif op == "REC":
            recover(conn, client_name)
        elif op == "DEL":
            delete(conn, client_name)
        else:
            conn.close()

def list_files(conn, client_name):
    file_list = []
    # percorrer todas as intâncias do servidor e salvar os arquivos sem 
    # repetições

    # se DIRECTORY não existe, é criado
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)

    # todas as subpastas (máquinas) de DIRECTORY
    directories = os.listdir(DIRECTORY)
    
    # para cada subpasta do servidor, vamos procurar o diretorio do cliente
    for folder in directories:
        # setando o path da subpasta
        folder_path = DIRECTORY + folder + "\\"
        # retornando tudo do diretorio folder_path
        folder_files = os.listdir(folder_path)

        if client_name in folder_files:
            # print(f"[SUCCESS] There is a {client_name} folder")
            client_path = folder_path + client_name + "\\"
            client_files = os.listdir(client_path)

            # pegando todos os arquivos em .\server\maquina\cliente e 
            # armazenando na lista file_list
            for files in client_files:
                if files not in file_list:
                    file_list.append(files)

    # colocar todos os arquivos em uma string
    files_found = ""
    if file_list:
        print(f"[SUCESS] {client_name}'s files found: {file_list}")
        for files in file_list:
            files_found += files + ","
        files_found = files_found[:-1]
    else:
        print(f"[WARNING] No files found to {client_name}")

    if files_found:
        conn.send(f"Files to {client_name} found: {files_found}".encode(FORMAT))
    else:
        conn.send(f"No files to {client_name} found".encode(FORMAT))

def deposit(conn, client_name):
    # recebendo o numero de copias
    msg_length = conn.recv(HEADER).decode(FORMAT)
    msg_length = int(msg_length)
    copies = conn.recv(msg_length).decode(FORMAT)
    copies = int(copies)
    print(f"[SUCESS] Number of copies recieved: {copies}")
    conn.send(f"[SUCESS] Number of copies recieved: {copies}".encode(FORMAT))

    # recebendo o nome do arquivo
    msg_length = conn.recv(HEADER).decode(FORMAT)
    msg_length = int(msg_length)
    filename = conn.recv(msg_length).decode(FORMAT)
    print(f"[SUCESS] File name recieved: {filename}")
    conn.send(f"[SUCESS] File name recieved: {filename}".encode(FORMAT))

    # recebendo os dados do arquivo
    file_bytes = bytes()
    while True:
        bytes_read = conn.recv(HEADER)
        if not bytes_read:
            break
        file_bytes += bytes_read

    # fazer upload da quantidade de arquivo para uma quantidade copies de
    # máquinas, cujos nomes correspondem aos índices de [0, ..., copies]
    for instance in range(copies):
        if not os.path.exists(DIRECTORY + str(instance) + "\\" + client_name + "\\"):
            os.makedirs(DIRECTORY + str(instance) + "\\" + client_name + "\\")
        f = open(DIRECTORY + str(instance) + "\\" + client_name + "\\" + filename, "wb")
        f.write(file_bytes)
        f.close()

    conn.send(f"[SUCESS] File {filename} created".encode(FORMAT))
    print(f"[SUCESS] File {filename} created")

def recover(conn, client_name):
    # recebendo o nome do arquivo
    msg_length = conn.recv(HEADER).decode(FORMAT)
    msg_length = int(msg_length)
    filename = conn.recv(msg_length).decode(FORMAT)
    print(f"[SUCESS] File name recieved: {filename}")
    conn.send(f"[SUCESS] File name recieved: {filename}".encode(FORMAT))

    # se DIRECTORY não existe, é criado
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)

    # todas as subpastas (máquinas) de DIRECTORY
    directories = os.listdir(DIRECTORY)

    # para cada subpasta do servidor, vamos procurar o diretorio do cliente
    for folder in directories:
        # setando o path da subpasta
        folder_path = DIRECTORY + folder + "\\"
        # retornando tudo do diretorio folder_path
        folder_files = os.listdir(folder_path)

        if client_name in folder_files:
            # print(f"[SUCCESS] There is a {client_name} folder")
            client_path = folder_path + client_name + "\\"
            client_files = os.listdir(client_path)

            if filename in client_files:
                f = open(client_path + "\\" + filename, "rb")
                while True:
                    bytes_read = f.read(HEADER)
                    conn.send(bytes_read)
                    print(f"bytes sent: {bytes_read}")
                    if not bytes_read:
                        break
                f.close()

                # print(f"[SUCESS] File {filename} recovered")
                # conn.send(f"[SUCESS] File {filename} recovered".encode(FORMAT))
                return

def delete(conn, client_name):
    # recebendo o nome do arquivo
    msg_length = conn.recv(HEADER).decode(FORMAT)
    msg_length = int(msg_length)
    filename = conn.recv(msg_length).decode(FORMAT)
    print(f"[SUCESS] File name recieved: {filename}")
    conn.send(f"[SUCESS] File name recieved: {filename}".encode(FORMAT))

    # variável de sinalização de remoção
    removed = False

    # se DIRECTORY não existe, é criado
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)

    # todas as subpastas (máquinas) de DIRECTORY
    directories = os.listdir(DIRECTORY)

    # para cada subpasta do servidor, vamos procurar o diretorio do cliente
    for folder in directories:
        # setando o path da subpasta
        folder_path = DIRECTORY + folder + "\\"
        # retornando tudo do diretorio folder_path
        folder_files = os.listdir(folder_path)

        if client_name in folder_files:
            # print(f"[SUCCESS] There is a {client_name} folder")
            client_path = folder_path + client_name + "\\"
            client_files = os.listdir(client_path)

            if filename in client_files:
                os.remove(client_path + "\\" + filename)
                removed = True
        
    if removed:
        print(f"[SUCESS] File {filename} deleted")
        conn.send(f"[SUCESS] File {filename} deleted".encode(FORMAT))
    else:
        print(f"[WARNING] FILE {filename} not found")
        conn.send(f"[WARNING] FILE {filename} not found".encode(FORMAT))

def handle_client(conn, addr):
    print("hi there")
    pass

main()