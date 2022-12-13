import socket
import threading

# definindo a porta da aplicação
PORT = 5050

# defininfo um padrão de tamanho para as mensagens dos sockets
HEADER = 64

# definindo o endereço IP do servidor, dispositivo na rede local
# SERVER = "192.168.1.3" equivalente ao comando abaixo:
SERVER = socket.gethostbyname(socket.gethostname())

# definindo o formato de endereço
ADDR = (SERVER, PORT)

# defininfo formato de decodificação das mensagens dos sockets
FORMAT = 'utf-8'

# auto-explicativo
DISCONNET_MESSAGE = "!DISCONNECT"

# print(SERVER)
# print(socket.gethostname())

# checar o que esse comando faz, exatamente. mas, basicamente, cria um 
# socket para o servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# condicionamos qualquer contato por ADDR para se comunicar com o socket
# server 
server.bind(ADDR)

def handle_client(conn, addr):
    print("[NEW CONNECTION]", addr," connected.")

    connected = True
    while connected:
        # em recv() informamos quantos bytes de informação esperamos do 
        # socker conn
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNET_MESSAGE:
                connected = False

            print("[", addr, "]:", msg,)
            conn.send("Msg received".encode(FORMAT))
    
    conn.close()

def start():
    server.listen() # auto-explicativo
    print("[LISTENING] server is listening on ", SERVER)

    while True:
        # accept() -> (socket object, address info)
        # Wait for an incoming connection. Return a new socket 
        # representing the connection, and the address of the client. 
        # For IP sockets, the address info is a pair (hostaddr, port).
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print("[ACTIVE CONNECTIONS] ", threading.active_count() - 1)

print("[START] server is running...")
start()