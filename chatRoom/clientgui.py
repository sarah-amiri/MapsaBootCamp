from tkinter import *


class ClientGui:
    def __init__(self):
        self.window = Tk()
        self.window.title("My Chat Room")
        self.window.geometry('750x300')

        self.frame = Frame(self.window)
        self.frame.grid(row=3, column=0, sticky=W + E + N + S)

        self.__initialize()
        self.window.mainloop()

    def __initialize(self):
        self.lbl1 = Label(self.frame, text="Server IP")
        self.lbl2 = Label(self.frame, text="Server Port")
        self.lbl3 = Label(self.frame, text="Username")

        self.entry1 = Entry(self.frame)
        self.entry2 = Entry(self.frame)
        self.entry3 = Entry(self.frame)
        self.entry1.insert(0, 'localhost')
        self.entry2.insert(0, 8301)

        self.button = Button(self.frame, text="Connect", command=self.connect, width=20)

        self.lbl1.grid(row=0, column=0)
        self.lbl2.grid(row=0, column=3)
        self.lbl3.grid(row=0, column=6)
        self.entry1.grid(row=0, column=1, columnspan=2)
        self.entry2.grid(row=0, column=4, columnspan=2)
        self.entry3.grid(row=0, column=7, columnspan=2)
        self.button.grid(row=0, column=9)

    def connect(self):
        print(self.entry1.get())
        print(self.entry2.get())
        print(self.entry3.get())


client = ClientGui()