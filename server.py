import socket
import threading

HEADER = 64  # сколько байтов может содержать сообщение
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "exit"
CONNECTED_LIST = []
CONN_LIST = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    try:

        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True

        while connected:
            msg = conn.recv(HEADER).decode(FORMAT)

            if msg:
                if msg == DISCONNECT_MESSAGE:

                    connected = False
                    del CONN_LIST[CONN_LIST.index(conn)]
                    del CONNECTED_LIST[CONNECTED_LIST.index(addr)]

                conn.send(msg.encode(FORMAT))
                print(f"[{addr}] {msg}")

        conn.close()

    except WindowsError:

        print(f"[ERROR] {addr} client crash")
        del CONN_LIST[CONN_LIST.index(conn)]
        del CONNECTED_LIST[CONNECTED_LIST.index(addr)]


def start():

    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")

    while True:

        conn, addr = server.accept()  # conn - объект сокета, addr - кортеж, адрес и порт клиента
        CONNECTED_LIST.append(addr)
        CONN_LIST.append(conn)

        thread = threading.Thread(target=handle_client, args=(conn, addr))  # обработчик клиента
        thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


start()
