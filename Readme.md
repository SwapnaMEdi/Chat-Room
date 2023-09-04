# Chatting Room

A simple chat application for real-time communication.

## Server.py

```
# Import necessary libraries
import socket  # For handling network connections
import threading  # For multi-threading support
import pandas as pd  # For data storage and manipulation
from datetime import datetime  # For timestamping

# Define the host and port for the chat server
host = 'host ip' # host ip / Local host ip
port = 55555

# Initialize an empty DataFrame to store chat messages
chat_data = pd.DataFrame(columns=['Timestamp', 'Nickname', 'Message'])

# Function to handle incoming chat messages and save them to CSV
def handle(client, nickname):
    while True:
        try:
            # Receive and decode the incoming message from the client
            message = client.recv(1024).decode('ascii')

            # Get the current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Add the message with timestamp to the DataFrame
            chat_data.loc[len(chat_data)] = [timestamp, nickname, message]

            # Save the chat_data DataFrame to a CSV file instantly
            chat_data.to_csv("chat_history.csv", index=False)

            # Broadcast the message to all clients
            broadcast(message.encode('ascii'), nickname)
        except:
            # Handle client disconnect
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nicknames.remove(nickname)
            break

# Function to broadcast a message to all clients
def broadcast(message, sender_nickname):
    global clients  # Declare clients as a global variable
    for client in clients:
        client.send(message)

# Function to start the chat server
def start_server():
    global clients, nicknames  # Declare clients and nicknames as global variables
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

        # Create a new thread to handle the client
        thread = threading.Thread(target=handle, args=(client, nickname))
        thread.start()

# Start the chat server
if __name__ == "__main__":
    start_server()
```


## Client.py

```

# Import necessary libraries
import socket  # For handling network connections
import threading  # For multi-threading support

# Get the user's chosen nickname as input
nickname = input("Choose your nickname: ")

# Create a socket for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the chat server with its IP address and port number
client.connect(('server ip', 55555))  # Replace 'server ip' with the actual server's IP address

# Function to receive and display messages from the server
def receive():
    while True:
        try:
            # Receive and decode incoming messages from the server
            message = client.recv(1024).decode('ascii')
            
            # Check if the server requested the client's nickname
            if message == 'NICK':
                # Send the chosen nickname to the server
                client.send(nickname.encode('ascii'))
            else:
                # Display the received message
                print(message)
        except:
            # Handle errors and close the client socket
            print("An error occurred!")
            client.close()
            break

# Function to send messages to the server
def write():
    while True:
        # Get user input and format it as "nickname: message"
        message = '{}: {}'.format(nickname, input(''))
        
        # Send the formatted message to the server
        client.send(message.encode('ascii'))

# Create a thread to receive messages from the server
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Create a thread to send messages to the server
write_thread = threading.Thread(target=write)
write_thread.start()

```


