import socket

# definindo a porta da aplicação
PORT = 5050

# defininfo um padrão de tamanho para as mensagens dos sockets
HEADER = 1024

# defininfo formato de decodificação das mensagens dos sockets
FORMAT = 'utf-8'

# auto-explicativo
DISCONNET_MESSAGE = "!DISCONNECT"

# definindo o ip do servidor, dispositivo hospedando a aplicação do lado
# do servidor 
SERVER = "192.168.1.3"

# definindo o formato de endereço
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

def send_file(filename):
    f = open(filename, "rb")
    while True:
        bytes_read = f.read(HEADER)
        if not bytes_read:
            break
        client.send(bytes_read)
    f.close()
    print(client.recv(2048).decode(FORMAT))

# client_name
send("thomas")
# operacao
send("DEP")
# numero de copias
send("1")
# filename
send("test")
# file
send_file("test")