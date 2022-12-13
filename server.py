import socket
import threading
import os
from os.path import exists, normpath

# Cada instância do servidor irá ser executado em uma porta diferente.
# Todos os arquivos serão armazenados, acessados e deletados nos 
# diretórios dir/{PORT}, para uma dada porta de uma dada instância da 
# aplicação servidor. 

HEADER = 1024
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DIRECTORY = 'dir'
DISCONNET_MESSAGE = "!DISCONNECT"

def start(PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(SERVER, PORT)
    server.listen()
    print(f"[LISTENING] server is listening on IP: {SERVER}, Port: {PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print("[ACTIVE CONNECTIONS] ", threading.active_count() - 1)

print("[START] server is running...")


def handle_client(conn, addr, PORT):
    print("[NEW CONNECTION]", addr," connected.")
    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            print("[", addr, "]:", msg,)
            conn.send("Msg received".encode(FORMAT))

            # caso a mensagem seja de encerramento da conexão
            if msg == DISCONNET_MESSAGE:
                connected = False

            # cliente evia uma mensagem do formato: 
            # operação nome_do_arquivo
            # a mensagem é fragmentada e os valores são atribuídos às 
            # variáveis.
            op, filename = msg.split(" ")

            # as operações podem ser:
            # DEP := Depositar arquivo
            # REC := Recuperar arquivo
            # DEL := Deletar arquivo

            if op == "DEP":
                if not exists(f"{DIRECTORY}/{PORT}"):
                    os.makedirs(f"{DIRECTORY}/{PORT}")
                try:
                    pass
                except Exception as e:
                    pass
                pass
            elif op == "REC":
                pass
            elif op == "DEL":
                pass
    
    conn.close()


def deposit(conn, filename, PORT):
    # definindo o diretorio e nome do arquivo
    filename = normpath(f"{DIRECTORY}/{PORT}/{filename}")
    f = open(filename, "wb")

    # escreve até ler todos os possíveis bytes a serem escritos
    while True:
        bytes_to_write = conn.recv(HEADER)
        if not bytes_to_write:
            break
        f.write(bytes_to_write)

def recover(conn, filename, PORT):
    # caso o arquivo não exista
    if not exists(f"{DIRECTORY}/{PORT}/{filename}"):
        msg = (f"File {filename} not found").encode(FORMAT)
        msg_length = len(msg)
        msg_length = str(msg_length).encode(FORMAT)
        msg_length += b' ' * (1024 - len(msg_length))
        conn.send(msg_length)
        conn.send(msg)
    else:
        # definindo o diretorio e nome do arquivo
        filename = normpath(f"{DIRECTORY}/{PORT}/{filename}")
        f = open(filename, "rb")

        # lê até ler todos os possíveis bytes a serem lidos
        while True:
            bytes_to_read = f.read(HEADER)
            if not bytes_to_read:
                break
            conn.send(bytes_to_read)

def delete(conn, filename, PORT):
    if exists(f"{DIRECTORY}/{PORT}/{filename}"):
        os.remove(f"{DIRECTORY}/{PORT}/{filename}")
    else:
        msg = (f"File {filename} not found").encode(FORMAT)
        msg_length = len(msg)
        msg_length = str(msg_length).encode(FORMAT)
        msg_length += b' ' * (1024 - len(msg_length))
        conn.send(msg_length)
        conn.send(msg)



start(5050)