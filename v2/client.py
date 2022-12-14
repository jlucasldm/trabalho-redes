import socket

# definindo a porta da aplicação
# PORT = 5050
# definindo um padrão de tamanho para as mensagens dos sockets
HEADER = 1024
# definindo formato de decodificação das mensagens dos sockets
FORMAT = 'utf-8'
# auto-explicativo
DISCONNET_MESSAGE = "!DISCONNECT"
# definindo o ip do servidor, dispositivo hospedando a aplicação do lado
# do servidor 
# SERVER = "192.168.1.3"

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

# # client_name
# send("thomas")
# # operacao
# send("DEP")
# # numero de copias
# send("3")
# # filename
# send("test")
# # file
# send_file("test")


# # client_name
# send("thomas")
# # operacao
# send("REC")
# # filename
# send("test")
# # recebendo o arquivo
# recv_file("test")

# # client_name
# send("thomas")
# # operacao
# send("DEL")
# # filename
# send("test")