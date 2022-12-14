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
    # PORT = int(input("porta: "))
    PORT = 5050
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
        print(files_found)
    else:
        print(f"[WARNING] No files found to {client_name}")
        
    conn.send(f"Files to {client_name} found: {files_found}".encode(FORMAT))

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
        conn.send(f"byte recieved".encode(FORMAT))

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
        
    print(f"[SUCESS] File {filename} deleted")
    conn.send(f"[SUCESS] File {filename} deleted".encode(FORMAT))

def handle_client(conn, addr):
    print("hi there")
    pass

main()