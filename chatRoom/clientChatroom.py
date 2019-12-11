import socket
import re
from clientgui import ClientGui


class Client:
    def __init__(self):
        self.gui = ClientGui(self)
        self.client_socket = None
        self.isChosen = False

    def connect_to_server(self, ip, port, username):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip, port))
        self.client_socket.send(bytes(username, 'utf-8'))

        message = self.client_socket.recv(1024).decode('utf-8')
        return message

    def receive_users(self):
        msg = self.__recv_message()
        users = msg.split('*')
        return users

    def __recv_message(self):
        message = self.client_socket.recv(2048)
        return message.decode('utf-8')

    def start_chat(self, user, username):
        msg = '#' + username + '->' + user
        self.client_socket.send(bytes(msg, 'utf-8'))
        previous_data = self.client_socket.recv(4096)
        if previous_data:
            previous_data = previous_data.decode('utf-8').split('##')
        return previous_data

    def send_msg(self, msg):
        # regex
        x = re.findall("^#", msg)
        y = re.findall("\r", msg)
        if x:
            print("Your message should not contain #")
        elif y:
            print("Your message should not contain \\r")
        else:
            self.client_socket.send(bytes(msg, 'utf-8'))

    def read_message(self):
        message = self.client_socket.recv(1024).decode('utf-8')
        return message


if __name__ == '__main__':
    Client()