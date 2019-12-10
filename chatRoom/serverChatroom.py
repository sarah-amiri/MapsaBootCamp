import socket
import datetime
import select
from dbConnection import DBConnection

IP = 'localhost'
PORT = 8201

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((IP, PORT))

server_socket.listen(10)
print("server up!")

socket_list = [server_socket]

#establish the database
db = DBConnection()
conn = db.connect_to_db('chatroom.db')
cursor = conn.cursor()
#cursor.execute('drop table if exists users')
#cursor.execute('drop table if exists chats')
db.create_table(cursor, 'users',
                'username TEXT PRIMARY KEY',
                'busy BOOLEAN',
                'online BOOLEAN',
                'chatTo string',
                'FOREIGN KEY (chatTo) REFERENCES users (username) ON UPDATE SET NULL ON DELETE SET NULL')
db.create_table(cursor, 'chats',
                'sender string',
                'receiver string',
                'message TEXT',
                'time TIMESTAMP',
                'FOREIGN KEY (sender) REFERENCES users (username) ON UPDATE SET NULL ON DELETE SET NULL',
                'FOREIGN KEY (receiver) REFERENCES users (username) ON UPDATE SET NULL ON DELETE SET NULL')

def print_chats():
    query3 = db.db_query(cursor, 'SELECT * FROM chats')
    if query3:
        chats_list = cursor.fetchall()
        for ch in chats_list:
            print(ch)


cursor.execute("update users set busy=0, online=0, chatTo=''")
conn.commit()
clients = {}
usernames = []

def print_db():
    query_2 = db.db_query(cursor, 'SELECT * FROM users')
    if query_2:
        users_list = cursor.fetchall()
    for usrr in users_list:
        print(usrr)

while True:
    read_socket, write_socket, exception_socket = select.select(
        socket_list, [], socket_list)
    for s in read_socket:
        if s == server_socket:
            client_socket, address = server_socket.accept()
            if client_socket:
                username = client_socket.recv(1024).decode('utf-8')
                search_query = db.search(cursor, 'username', 'users')
                for x in search_query:
                    usernames.append(x[0])
                if username in usernames:
                    client_socket.send(bytes("Welcome back {}!\n".format(username), 'utf-8'))
                    db.update(cursor, 'users', 'online=1', 'WHERE username="{}"'.format(username))
                else:
                    query = "INSERT INTO users(username, busy, online, chatTo) VALUES(?, ?, ?, ?)"
                    db_query = db.add_query(cursor, query, [(username, False, True, None)])
                    if db_query:
                        conn.commit()
                    client_socket.send(bytes("welcome to this chatroom!\n", 'utf-8'))
                client_socket.send(bytes("If you want to exit enter exit\n",'utf-8'))
                socket_list.append(client_socket)
                clients[client_socket] = username
                print("Connection Established from {}".format(address))
                client_socket.send(bytes("Who do you want to chat to?", 'utf-8'))
                for client_sockets in clients:
                    if client_sockets != client_socket:
                        client_sockets.send(
                            bytes("{} joined Group with address {}".format(username, address), 'utf-8'))

        else:
            message = s.recv(1024).decode('utf-8')
            if not message:
                socket_list.remove(s)
                del clients[s]
                continue
            if message[0] == '#':
                if message == '#finish':
                    sender = clients[s]
                    receiver = db.search(cursor, 'chatTo', 'users', "WHERE username='{}'".format(sender))[0][0]
                    for client in clients:
                        if clients[client] == receiver:
                            u2 = client
                            break
                    db.update(cursor, 'users', "busy=0, chatTo=''", "WHERE username='{}' OR username='{}'".format(sender,receiver))
                    finished_message = bytes('#finishPrivate chat is finished\nNow you can choose another user',
                                             'utf-8')
                    s.send(finished_message)
                    u2.send(finished_message)
                    print('A chat is finished between {} and {}'.format(sender, receiver))
                elif message == '#exit':
                    username_exit = clients[s]
                    who_exit = db.search(cursor, 'busy, chatTo', 'users', 'WHERE username="{}"'.format(username_exit))
                    print(who_exit)
                    busy_status = who_exit[0][0]
                    db.update(cursor, 'users', 'busy=0,online=0,chatTo=""', 'WHERE username="{}"'.format(username_exit))
                    if busy_status:
                        db.update(cursor,'users', 'busy=0, chatTo=""', 'WHERE username="{}"'.format(who_exit[0][1]))
                        for client in clients:
                            if clients[client] == who_exit[0][1]:
                                client.send(bytes('#finishPrivate chat is finished\nNow you can choose another user',
                                             'utf-8'))
                    conn.commit()
                    s.send(bytes("bye {}".format(username_exit),'utf-8'))
                    socket_list.remove(s)
                    del clients[s]
                else:
                    message = message[1:].split('->')
                    sender_user = message[0]
                    receiver_user = message[1]
                    if sender_user == receiver_user:
                        s.send(bytes("#you", 'utf-8'))
                    else:
                        search_query = db.search(cursor, 'busy, online', 'users',
                                                 "WHERE username = '{}'".format(receiver_user))
                        if search_query:
                            if search_query[0][0]:
                                s.send(bytes("#busy", 'utf-8'))
                            elif not search_query[0][1]:
                                s.send(bytes("#disconnected", 'utf-8'))
                            else:
                                update_query = db.update(cursor,
                                                         "users",
                                                         "busy=1, chatTo='{}'".format(sender_user),
                                                         "WHERE username = '{}'".format(receiver_user))
                                if update_query:
                                    conn.commit()
                                update_query = db.update(cursor,
                                                         "users",
                                                         "busy=1, chatTo='{}'".format(receiver_user),
                                                         "WHERE username = '{}'".format(sender_user))
                                if update_query:
                                    conn.commit()
                                s.send(bytes("#OK", 'utf-8'))
                                for client in clients:
                                    if clients[client] == receiver_user:
                                        client_socket = client
                                        break
                                client_socket.send(bytes("#OK", 'utf-8'))
                                print('A chat is established between {} and {}'.format(sender_user,
                                                                                       receiver_user))
                                chat_messages = db.search(cursor,
                                                     'sender, receiver, message, time',
                                                     'chats',
                                                     'WHERE sender="{}" AND receiver="{}"'.format(sender_user, receiver_user))
                                for mss in chat_messages:
                                    previous_chat = "{}**  {}->{}: {}".format(mss[3], mss[0], mss[1], mss[2])
                                    s.send(bytes(previous_chat,'utf-8'))
                                    client_socket.send(bytes(previous_chat,'utf-8'))
                        else:
                            s.send(bytes('#exist', 'utf-8'))
            else:
                sender_username = clients[s]
                receiver_username = db.search(cursor, 'chatTo', 'users', 'WHERE username="{}"'.format(sender_username))
                if receiver_username:
                    receiver_username = receiver_username[0][0]
                for client in clients:
                    if clients[client] == receiver_username:
                        receiver_socket = client
                        break
                add_query = db.add_query(cursor,
                             "INSERT INTO chats(sender, receiver, message, time) VALUES(?,?,?,?)"
                             ,[(sender_username, receiver_username, message.split('->')[1], datetime.datetime.now())])
                if add_query:
                    conn.commit()
                receiver_socket.send(bytes(message,'utf-8'))
    for s in exception_socket:
        socket_list.remove(s)
        del clients[s]
    # print(socket_list)
# server_socket.close()
