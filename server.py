import socket
import os

def send_file(client_socket, file_path):
    # Get file name and size
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    # Send file name and size information
    file_info = f"{file_name},{file_size}"
    client_socket.send(file_info.encode())

    # Wait for acknowledgment from the client
    acknowledgment = client_socket.recv(1024).decode()

    if acknowledgment.lower() == 'ok':
        # Send the file data in chunks
        with open(file_path, 'rb') as file:
            for chunk in iter(lambda: file.read(1024), b''):
                client_socket.send(chunk)

        print(f"File '{file_name}' sent to the client. Size: {file_size} bytes")
    else:
        print("Client did not acknowledge. File transfer aborted.")

def handle_client(client_socket, client_number, clients):
    file_path = "/home/satvik/Pictures/top.png"  # Replace with the path to your binary file

    send_file(client_socket, file_path)

    # Receive client's decision to forward the file
    forward_decision = client_socket.recv(1024).decode()
    
    if forward_decision.lower() == 'yes':
        # Send acknowledgment to the client
        client_socket.send('OK'.encode())

        # Send the list of available clients
        client_socket.send(','.join(clients).encode())

        # Receive the selected client number
        selected_client = client_socket.recv(1024).decode()

        if selected_client in clients:
            send_file(clients[selected_client], file_path)
        else:
            print("Invalid client number. File forwarding aborted.")
    
    client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8080))
server.listen(5)

print("Server listening on port 8080")

clients = {}

# Accept multiple clients
for i in range(1, 5):
    client, address = server.accept()
    print(f"Connection from {address} has been established for client {i}.")
    clients[str(i)] = client

    handle_client(client, i, clients)
