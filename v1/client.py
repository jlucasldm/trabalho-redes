import socket

HEADER = 1024
FORMAT = 'utf-8'
DISCONNET_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.3"
# ADDR = (SERVER, PORT)
DIRECTORY = "local"

def contact(PORT):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(SERVER, PORT)

    msg = input()

    # se a mensagem é do formato de encerramento da conexão
    if msg.count(" ") == 0:
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
        print(client.recv(2048).decode(FORMAT))
    else:
        op, filename, tolerance = msg.split(" ")

    if op == "DEP":
        # enviando ao servidor os parametros de entrada de uma
        # operação
        message = (f"DEP {filename} {tolerance}").encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)

        #
        pass
    elif op == "REC":
        pass
    elif op == "DEL":
        pass

contact("Hello, World!")
input()
contact("Making my own plans")
input()
contact("The worst is done")
contact(DISCONNET_MESSAGE)