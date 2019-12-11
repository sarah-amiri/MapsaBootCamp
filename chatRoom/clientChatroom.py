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
'''
isChosen = False


def send_message():
    while True:
        global isChosen
        msg = input()
        if msg:
            if not isChosen:
                msg = '#' + username + '->' + msg
                isChosen = True
            elif msg == 'finish':
                msg = '#finish'
            elif msg == 'exit':
                msg = '#exit'
            else:
                msg = username + "->" + msg
            client_socket.send(bytes(msg, 'utf-8'))


def first_setup():
    mess = client_socket.recv(2048)
    print(mess.decode('utf-8'))
    client_socket.setblocking(0)


t1 = threading.Thread(target=send_message)
t1.start()


first_setup()
while True:
    # #    message = client_socket.recv(1024)
    # #    print(message.decode('utf-8'))
    # msg = input('{}-> '.format(username))
    # if msg:
    #     client_socket.send(bytes(username + "->" + msg, 'utf-8'))

    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                print("Connection Closed!")
                sys.exit()
            message = message.decode('utf-8')
            if message == '#OK':
                print("Now you can start messaging")
                print("If you want to close this private chat enter finish")
                isChosen = True
            elif message == '#busy':
                print('Username you chose was busy')
                isChosen = False
            elif message == '#disconnected':
                print('Username you chose was disconnected')
                isChosen = False
            elif message == '#exist':
                print('Username does not exist')
                isChosen = False
            elif message == '#you':
                print('You cannot chat with yourself')
                isChosen = False
            elif message[:7] == '#finish':
                print('finish')
                print(message[7:])
                isChosen = False
            else:
                print(message)

    except IOError as e:
        pass

#    time.sleep(5)
'''