from tkinter import *
from tkinter import messagebox
import threading

class ClientGui:

    def __init__(self, client):
        self.ip = 'localhost'
        self.port = 8201
        self.username = ''
        self.client = client
        self.is_chatting = False
        self.is_connected = False

        self.t1 = threading.Thread(target=self.read_msg)

        self.window = Tk()
        self.window.title("My Chat Room")
        self.window.geometry('850x500')

        self.frame = Frame(self.window)
        self.frame.grid(row=0, column=0, sticky=W + E + N + S)

        self.__initialize()

        self.frame2 = Frame(self.window)
        self.frame3 = Frame(self.window)
        self.frame4 = Frame(self.window)
        self.frame2.grid(row=1, column=0, columnspan=3, sticky=W + N + S)
        self.frame3.grid(row=1, column=3, columnspan=1, sticky=E + N + S)
        self.frame4.grid(row=2, column=0, columnspan=4, sticky=W + E + N +S)

        self.chat_pane, \
        self.chat_scrollbar, \
        self.users_list, \
        self.users_list_scrollbar, \
        self.chat_entry, \
        self.chat_button,\
        self.contact = \
            None, None, None, None, None, None, None

        self.online_users = []

        self.var = IntVar()

        self.window.mainloop()

    def __initialize(self):
        self.lbl1 = Label(self.frame, text="Server IP")
        self.lbl2 = Label(self.frame, text="Server Port")
        self.lbl3 = Label(self.frame, text="Username")

        self.entry1 = Entry(self.frame)
        self.entry2 = Entry(self.frame)
        self.entry3 = Entry(self.frame)
        self.entry1.insert(0, self.ip)
        self.entry2.insert(0, self.port)

        self.button = Button(self.frame, text="Connect", command=self.connect, width=20)

        # self.lbl1.grid(row=0, column=0)
        # self.lbl2.grid(row=1, column=0)
        # self.lbl3.grid(row=2, column=0)
        # self.entry1.grid(row=0, column=1, columnspan=2)
        # self.entry2.grid(row=1, column=1, columnspan=2)
        # self.entry3.grid(row=2, column=1, columnspan=2)
        # self.button.grid(row=3, column=1)
        self.lbl1.grid(row=0, column=0)
        self.lbl2.grid(row=0, column=3)
        self.lbl3.grid(row=0, column=6)
        self.entry1.grid(row=0, column=1, columnspan=2)
        self.entry2.grid(row=0, column=4, columnspan=2)
        self.entry3.grid(row=0, column=7, columnspan=2)
        self.button.grid(row=0, column=9)

    def connect(self):
        self.is_connected = not self.is_connected
        if self.is_connected:
            self.ip = self.entry1.get()
            self.port = int(self.entry2.get())
            self.username = self.entry3.get()
            # print(self.ip, self.port, self.username)
            if self.ip and self.port and self.username:
                enter_msg = self.client.connect_to_server(self.ip, self.port, self.username)
                messagebox.showinfo("Welcome", enter_msg)
                self.button.configure(text="disconnect", bg="red", fg="white")

                # set up chat pane
                self.chat_pane = Text(self.frame2)
                self.chat_pane.pack(side="left", expand=1, fill="both")
                self.chat_scrollbar = Scrollbar(self.frame2, orient="vertical")
                self.chat_scrollbar.config(command=self.chat_pane.yview)
                self.chat_scrollbar.pack(side="left", fill="both")
                self.chat_pane.config(yscrollcommand=self.chat_scrollbar.set)

                # set up users list
                self.users_list = Listbox(self.frame3)
                self.users_list.pack(side="left", expand=1, fill="both")
                self.users_list_scrollbar = Scrollbar(self.frame3, orient="vertical")
                self.users_list_scrollbar.config(command=self.users_list.yview)
                self.users_list_scrollbar.pack(side="left", fill="both")
                self.users_list.config(yscrollcommand=self.users_list_scrollbar.set)

                # set up entry for inputs
                self.entrytext = StringVar()
                self.chat_entry = Entry(self.frame4, width=100, textvariable=self.entrytext)
                self.chat_entry.grid(row=0, column=0, columnspan=4)
                self.chat_button = Button(self.frame4, text="send", command=self.send_msg)
                self.chat_button.grid(row=0, column=4)

                self.online_users = self.client.receive_users()
                for index in range(len(self.online_users)):
                    online_user = self.online_users[index]
                    radio = Radiobutton(self.users_list, text=online_user, value=index, variable=self.var)
                    radio.grid(row=index, column=0)
                self.btn = Button(self.users_list, text="Start", bg='green', command=self.start_chat)
                # btn.bind('<Button-1>', 'start_chat')
                self.btn.grid(column=0)
            else:
                self.client.send_msg('#exit')
                self.window.exit()

    def start_chat(self):
        self.is_chatting = not self.is_chatting
        if self.is_chatting:
            self.btn.configure(text="END", bg='blue', fg='white')
            self.contact = self.online_users[self.var.get()]
            previous_messages = self.client.start_chat(self.contact, self.username)
            for previous_message in previous_messages:
                self.chat_pane.insert(END, previous_message)
                self.chat_pane.insert(END, '\n')
            self.t1.start()
        else:
            self.client.send_msg('#finish')

    def send_msg(self):
        if self.is_chatting:
            message = self.chat_entry.get()
            self.chat_pane.insert(END, self.username + '->' + self.contact + ': ' + message)
            self.chat_pane.insert(END, '\n')
            self.client.send_msg(self.username + '->' + message)
        self.entrytext.set('')

    def read_msg(self):
        while True:
            read_message = self.client.read_message().split('->')
            sender = read_message[0]
            message = read_message[1]
            self.chat_pane.insert(END, sender + '->' + self.username + ': ' + message)





