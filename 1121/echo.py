import socket
import threading

def send_msg(sock, msg):
    total_sent_len = 0
    total_msg_len = len(msg)
    while total_sent_len < total_msg_len:
        sent_len = sock.send(msg[total_sent_len:])
        if sent_len == 0:
            raise RuntimeError("Socket connection broken")
        total_sent_len += sent_len

def recv_msg(sock, chunk_len=1024):
    while True:
        received_chunk = sock.recv(chunk_len)
        if len(received_chunk) == 0:
            break
        yield received_chunk

def handle_client(client_socket, client_address):
    print(f"Accepted from {client_address}")

    for received_msg in recv_msg(client_socket):
        send_msg(client_socket, received_msg)
        print(f"Echo to {client_address}: {received_msg}")

    print(f"Connection with {client_address} closed.")
    client_socket.close()

def main():
    ip_address = input("Enter the IP address: ")
    port = int(input("Enter the port number: "))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((ip_address, port))
    server_socket.listen()
    print("Starting server ...")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    main()


