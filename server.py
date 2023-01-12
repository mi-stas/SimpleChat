import socket as s
from threading import Thread

HOST = ""
PORT = 12400
MESSAGE_MAX_SIZE = 1024


class ChatServer:
    def __init__(self):
        self.server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(100)
        self.client_sockets = []
        self.server_listening_thread = Thread(target=self._listen_for_connections)
        self.server_listening_thread.start()

    def _listen_for_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(MESSAGE_MAX_SIZE).decode()
                if message:
                    self._broadcast_message(message, client_socket)
                else:
                    self._remove_client_connection(client_socket)
            except Exception:
                self._remove_client_connection(client_socket)

    def _broadcast_message(self, message, sending_socket):
        for client_socket in self.client_sockets:
            if client_socket == sending_socket:
                continue

            try:
                client_socket.send(message.encode())
            except Exception:
                self._remove_client_connection(client_socket)

    def _remove_client_connection(self, client_socket):
        if client_socket in self.client_sockets:
            self.client_sockets.remove(client_socket)
        client_socket.close()

    def _listen_for_connections(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.client_sockets.append(client_socket)
            listening_thread = Thread(target=self._listen_for_client, args=(client_socket,))
            listening_thread.daemon = True
            listening_thread.start()


if __name__ == "__main__":
    server = ChatServer()