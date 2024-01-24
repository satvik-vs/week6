import socket
import os

def receive_file(client_socket):
    # Receive file name and size information
    file_info = client_socket.recv(1024).decode().split(',')
    file_name, file_size = file_info[0], int(file_info[1])

    # Create a new file to write the received data
    with open(file_name, 'wb') as received_file:
        # Receive the file data in chunks
        remaining_size = file_size
        while remaining_size > 0:
            chunk_size = min(1024, remaining_size)
            file_data = client_socket.recv(chunk_size)
            received_file.write(file_data)
            remaining_size -= len(file_data)

    print(f"File '{file_name}' received and saved on the client. Size: {file_size} bytes")

def forward_file(client_socket):
    forward_decision = input("Do you want to forward the file to another client? (yes/no): ")
    client_socket.send(forward_decision.encode())

    if forward_decision.lower() == 'yes':
        # Receive the list of available clients
        client_list = client_socket.recv(1024).decode()
        print(f"Available clients: {client_list}")

        # Ask for the client number to forward the file to
        selected_client = input("Enter the client number to forward the file to: ")
        client_socket.send(selected_client.encode())
    else:
        client_socket.close()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8080))

receive_file(client)

forward_file(client)
