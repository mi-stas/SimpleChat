import socket
from threading import Thread
import json
from dataclasses import dataclass

HOST = "127.0.0.1"
PORT = 12400
MESSAGE_MAX_SIZE = 1024


@dataclass
class MessageData:
    time: float
    name: str
    message: str

    def encoded(self):
        data_dict = {"time": self.time, "name": self.name, "message": self.message}
        return json.dumps(data_dict)


def decode_message_data(message_dict_string):
    try:
        message_data = json.loads(message_dict_string)
        return MessageData(message_data["time"], message_data["name"], message_data["message"])
    except Exception:
        return None


class ChatClient:
    def __init__(self, application):
        self.application = application
        self.listening_thread = None
        self.is_connected = False
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def initialize_connection(self):
        if self.is_connected:
            return

        self.is_connected = True
        self.client_socket.connect((HOST, PORT))
        self.listening_thread = Thread(target=self.listen_for_messages)
        self.listening_thread.daemon = True
        self.listening_thread.start()

    def listen_for_messages(self):
        while self.is_connected:
            try:
                message_data_string = self.client_socket.recv(MESSAGE_MAX_SIZE).decode()
                message_data = decode_message_data(message_data_string)
                self.application.display_message(message_data)
            except Exception:
                continue

    def send_message_data(self, message_data):
        message_data_string = message_data.encoded()
        self.client_socket.send(message_data_string.encode())

    def close_connection(self):
        if not self.is_connected:
            return

        self.is_connected = False
        self.client_socket.close()
