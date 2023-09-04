import socket
import threading
import pandas as pd
from datetime import datetime


host = '127.0.0.1' # host ip / Local host ip
port = 55555


chat_data = pd.DataFrame(columns=['Timestamp', 'Nickname', 'Message'])


def handle(client, nickname):
    while True:
        try:
            message = client.recv(1024).decode('ascii')


            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


            chat_data.loc[len(chat_data)] = [timestamp, nickname, message]


            chat_data.to_csv("chat_history.csv", index=False)


            broadcast(message.encode('ascii'), nickname)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nicknames.remove(nickname)
            break


def broadcast(message, sender_nickname):
    global clients  
    for client in clients:
        client.send(message)


def start_server():
    global clients, nicknames  
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    clients = []
    nicknames = []

    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'), nickname)
        client.send('Connected to server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client, nickname))
        thread.start()

if __name__ == "__main__":
    start_server()

