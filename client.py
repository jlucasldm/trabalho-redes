import socket

# definindo a porta da aplicação
PORT = 5050

# defininfo um padrão de tamanho para as mensagens dos sockets
HEADER = 64

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

send("Hello, World!")
input()
send("Making my own plans")
input()
send("The worst is done")
send(DISCONNET_MESSAGE)