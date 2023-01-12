from tkinter import *
from client import ChatClient, MessageData
import json
import time
from utils import time_to_message_format


class ChatView:
    def __init__(self):
        self.name = ""
        EnterNameView(self)

        self._init_window()
        self.client = ChatClient(self)
        self.client.initialize_connection()
        self.root.mainloop()

    def display_message(self, message_data):
        displaying_time = time_to_message_format(message_data.time)
        displaying_string = f"({displaying_time}) {message_data.name}: {message_data.message}"

        self.messages_listbox.insert(END, displaying_string)

    def set_name(self, name):
        self.name = name

    def _send_message(self, event=None):
        message_data = MessageData(time.time(), self.name, self.message_var.get())
        self.client.send_message_data(message_data)
        self.message_var.set("")
        self.display_message(message_data)

    def _on_closed(self):
        self.client.close_connection()
        self.root.quit()

    def _init_window(self):
        self.root = Tk()
        self.root.title("Chat")

        self.chat_frame = Frame(self.root)
        self.message_var = StringVar()
        self.scrollbar = Scrollbar(self.chat_frame)
        self.messages_listbox = Listbox(self.chat_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.messages_listbox.pack(side=LEFT, fill=BOTH)
        self.messages_listbox.pack()
        self.chat_frame.pack()

        self.entry_field = Entry(self.root, textvariable=self.message_var)
        self.entry_field.pack()
        self.send_button = Button(self.root, text="Send", command=self._send_message)
        self.send_button.pack()

        self.root.protocol("WM_DELETE_WINDOW", self._on_closed)


class EnterNameView:
    def __init__(self, chat_view):
        self.chat_view = chat_view
        self._init_window()
        self.root.mainloop()

    def _on_name_entered(self):
        self.chat_view.set_name(self.name_entry.get())
        self.root.destroy()

    def _on_canceled(self):
        self.root.quit()

    def _init_window(self):
        self.root = Tk()
        self.name_label = Label(self.root, text="Enter your name:")
        self.name_entry = Entry(self.root)
        self.enter_button = Button(self.root, text="OK", command=self._on_name_entered)
        self.cancel_button = Button(self.root, text="Cancel", command=self._on_canceled)

        self.name_label.grid(row=0, column=0)
        self.name_entry.grid(row=0, column=1)
        self.enter_button.grid(row=1, column=1)
        self.cancel_button.grid(row=1, column=0)


if __name__ == "__main__":
    application = ChatView()
