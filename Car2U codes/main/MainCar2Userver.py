# Import required modules
import socket
import threading

HOST = '127.0.0.1'
PORT = 1234 # You can use any port between 0 to 65535
LISTENER_LIMIT = 5
active_clients = [] # List of all currently connected users

# Function to send message to a single client
def send_message_to_client(client, message):
    client.sendall(message.encode())

# Function to send any new message to all the clients that
# are currently connected to this server
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

# Function to handle client
def client_handler(client):
    
    # Server will listen for client message that will
    # Contain the username
    while 1:
        username = client.recv(2048).decode('utf-8')
        
        username = str(username)

        if username != '':
            if username not in active_clients:
                active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} added to the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

# Main function
def main():
    # Creating the socket class object
    # AF_INET: we are going to use IPv4 addresses
    # SOCK_STREAM: we are using TCP packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Creating a try catch block
    try:
        # Provide the server with an address in the form of
        # host IP and port
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    # Set server limit
    server.listen(LISTENER_LIMIT)

    # This while loop will keep listening to client connections
    while 1:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()

# Function to send a direct message to a chosen user
def send_direct_message(username,target_username, message):
    for user in active_clients:
        if user[0] == username:
            send_message_to_client(user[1], message)
        if user[0] == target_username:
            send_message_to_client(user[1], message)
    print(f"User {target_username} not found or not connected.")
    return

# Modified listen_for_messages function to handle direct messages
def listen_for_messages(client, username):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            if message.startswith("@"):  # If message starts with '@', treat it as a direct message
                try:
                    # Example message format: "@target_username message"
                    target_username, msg_content = message[1:].split(' ', 1)
                    final_msg = f"{username} (direct)~{msg_content}"
                    send_direct_message(username,target_username, final_msg)
                except ValueError:
                    error_msg = "SERVER~Invalid direct message format. Use '@username message'."
                    send_message_to_client(client, error_msg)
            else:
                # Handle as a broadcast message if no '@' prefix
                final_msg = username + '~' + message
                send_messages_to_all(final_msg)
        else:
            print(f"The message sent from client {username} is empty")

if __name__ == '__main__':
    main()