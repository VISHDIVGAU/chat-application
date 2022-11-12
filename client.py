import threading
from tkinter import *
from tkinter import messagebox
import grpc
import chat_pb2 as chat
import chat_pb2_grpc as rpc
import pymongo
address = 'localhost'
port = 50051
client = pymongo.MongoClient("127.0.0.1", 27017)
db= client['ChatApplication']
coll= db['UserChats']

class Client:
    def __init__(self, u, chat_id):
        self.root= Tk()
        self.window = Frame(self.root, width=300, height=300)
        self.window.pack()
        index= u.find('@')
        self.username = u[0:index]
        self.root.title(self.username)
        self.chat_id= chat_id
        self.channel = grpc.insecure_channel(address + ':' + str(port), options=(('grpc.enable_http_proxy', 0),))
        self.conn = rpc.ChatServiceStub(self.channel)
        self.__setup_ui()
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
    

    def __listen_for_messages(self):
        c= chat.ChatId()
        c.chat_id= str(self.chat_id)
        for note in self.conn.ChatStream(c):
            print("R[{}] {}".format(note.name, note.message))
            self.chat_list.insert(END, "[{}] {}\n".format(note.name, note.message))

    def send_message(self, event):
        message = self.entry_message.get()
        if message is not '':
            n = chat.Note()
            n.name = self.username
            n.message = message
            n.chat_id= str(self.chat_id)
            print("S[{}] {}".format(n.name, n.message))
            self.conn.SendNote(n)


    def __setup_ui(self):

        self.chat_list = Text(self.window)
        self.chat_list.pack(side=TOP)
        self.lbl_username = Label(self.window, text=self.username)
        self.lbl_username.pack(side=LEFT)
        self.entry_message = Entry(self.window, bd=5)
        self.entry_message.bind('<Return>', self.send_message)
        self.entry_message.focus()
        self.entry_message.pack(side=BOTTOM)
