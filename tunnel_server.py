import socket
import threading

def handle_client(client_socket):
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_socket.connect(("localhost", 25565))  # Connect to your Minecraft server

    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        target_socket.sendall(data)

        response = target_socket.recv(4096)
        if not response:
            break
        client_socket.sendall(response)

    client_socket.close()
    target_socket.close()

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"[*] Listening on port {port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

# Start the tunnel server on port 8080 (or any other port you choose)
if __name__ == "__main__":
    start_server(8080)
