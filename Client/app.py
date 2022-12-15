from kivy.app import App 
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import (StringProperty, ObjectProperty)
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.clock import mainthread
from network import Session
from kivy.graphics import Color, Rectangle
import threading
from time import sleep
from network import Session

Window.size = (500, 500)
Window.icon = 'icon.png'

class ChatFinderScreen(Screen):
    scroll: ScrollView = ObjectProperty(None)
    back_button: Button = ObjectProperty(None)
    input_field: TextInput = ObjectProperty(None)
    find_chat_button: Button = ObjectProperty(None)
    
    def return_back(self):
        ClientApp.SM.transition.direction = "up"
        ClientApp.SM.current = "main_menu"
    
    @mainthread
    def add_chats_to_scroll(self, chat_names):
        for chat_name in chat_names:
            self.scroll.children[0].add_widget(Chat(chat_name, 'add'))
    
    def find_chat(self):
        def threaded_find_chat():    
            chat_names = ClientApp.session.find_chats(self.input_field.text)
            self.add_chats_to_scroll(chat_names)
        threading.Thread(target=threaded_find_chat).start()
        

class Message(Widget):
    message_text: Label = ObjectProperty(None)
    message_time: Label = ObjectProperty(None)
    message_sender: Label = ObjectProperty(None)
    
    def __init__(self, text='', sender='', index=0, **kwargs):
        super().__init__(**kwargs)
        if not isinstance(text, str):
            raise TypeError("Argument text in message must be str.")
        if len(text) > 200:
            raise Exception("Argument text in message can't contain more than 200 chars.") 
        if text == '':
            self.message_text.text = "Some text"
        else:
            self.message_text.text = text
        if sender:
            self.message_sender.text = sender
        else:
            self.message_sender.text = "Some sender"
        self.index = index
        self.resize()
            
    def resize(self):
        self.message_text.text_size[0] = Window.width - 20
        self.message_text.texture_update()
        self.height = self.message_text.height + 40

class ChatScreen(Screen):
    scroll: ScrollView = ObjectProperty(None)
    back_button: Button = ObjectProperty(None)
    chat_name: Label = ObjectProperty(None)
    input_field: TextInput = ObjectProperty(None)
    send_button: Button = ObjectProperty(None)
    def __init__(self, *messages, **kwargs):
        super().__init__(**kwargs)
        self.chat_name.text = kwargs["name"]
        self.scroll.width = Window.width
        Window.bind(on_resize=self.on_window_resize_messages)
        
    
    @mainthread        
    def add_message(self, text='', sender='', index=0):
        self.scroll.children[0].add_widget(Message(text=text, sender=sender, index=index))
    
    def on_window_resize_messages(self, window, width, height):
        if ClientApp.SM.current == self.chat_name.text:
            for message in self.scroll.children[0].children:
                message.resize()
                
    def on_enter(self, *args):
        threading.Thread(target=self.update_messages).start()
    
    def on_leave(self, *args):
        self.updating = False
    
    def update_messages(self):
        self.updating = True
        while True:
            print('update')
            if not self.updating:
                break
            current_messages = self.scroll.children[0].children
            idx = 0 if len(current_messages) == 0 else current_messages[0].index
            news = ClientApp.session.get_new_messages(self.chat_name.text.split(maxsplit=1)[1], idx)
            for new_idx, message_text, sender, time in news:
                print(new_idx, message_text, sender, time)
                self.add_message(text=message_text, sender=sender, index=new_idx)
            sleep(2)

    def resize_messages(self):
        for message in self.scroll.children[0].children:
            message.resize()

    def return_back(self):
        ClientApp.SM.transition.direction = "right"
        ClientApp.SM.current = "main_menu"
        
    def send(self):
        message_text = self.input_field.text
        self.input_field.text = ""
        
        def threaded_send(text):
            ClientApp.session.send_message(self.chat_name.text.split(maxsplit=1)[1], text, 'xxx')
        
        if len(message_text) % 200 == 0 and message_text:
            times = len(message_text)//200
        else:
            times = len(message_text)//200 + 1
        for i in range(times):
            sample = message_text[i*200:(i+1)*200]
            threading.Thread(target=threaded_send, args=[sample]).start()        
        
class Chat(Widget):
    chat_icon: Image = ObjectProperty(None)
    chat_name: Label = ObjectProperty(None)
    chat_button: Button = ObjectProperty(None)
        
    def __init__(self, chat_name, b_type="enter"):
        super().__init__()
        self.chat_icon.source = "icon.png"
        self.chat_name.text = chat_name
        self.button_type = b_type
        self.chat_button.width = Window.width
        if b_type == "enter":
            screen = ChatScreen(name=f"Chat {self.chat_name.text}")
            ClientApp.SM.add_widget(screen)
    
    def activate(self):
        match self.button_type:
            case "enter":
                self.enter_chat()
            case "add":
                self.add_chat()
    
    def add_chat(self):
        if f"Chat {self.chat_name.text}" not in ClientApp.SM.screen_names:
            ClientApp.SM.get_screen("main_menu").scroll.children[0].add_widget(Chat(self.chat_name.text))
        
    def enter_chat(self):
        ClientApp.SM.transition.direction = "left"
        ClientApp.SM.current = f"Chat {self.chat_name.text}"
        ClientApp.SM.current_screen.resize_messages()

class LoginScreen(Screen):
    login_label: Label = ObjectProperty(None)
    login: TextInput = ObjectProperty(None)
    password: TextInput = ObjectProperty(None)
    password_label: Label = ObjectProperty(None)
    button: Button = ObjectProperty(None)

    @mainthread
    def to_main_menu_screen(self):
        self.manager.current = "main_menu"

    def sign_in(self):
        def threaded_sign_in():
            success = ClientApp.session.connect(self.login.text, self.password.text)
            if success:
                ClientApp.LOGIN = self.login.text
                ClientApp.PASSWORD = self.password.text
                ClientApp.session.login = ClientApp.LOGIN
                ClientApp.session.password = ClientApp.PASSWORD
                self.to_main_menu_screen()
        threading.Thread(target=threaded_sign_in).start()

class MainMenuScreen(Screen):
    scroll: ScrollView = ObjectProperty(None)
    finder_button: Button = ObjectProperty(None)

    def on_enter(self, *args):
        threading.Thread(target=self.update_chats).start()
        
    def on_leave(self, *args):
        self.updating = False
    
    def update_chats(self):
        self.updating = True
        while True:
            if not self.updating:
                break
            chat_names = ClientApp.session.get_all_chats()
            self.add_chats_to_scroll(chat_names)
            sleep(5)
    
    @mainthread
    def add_chats_to_scroll(self, chat_names):
        for chat_name in chat_names:
            if f"Chat {chat_name}" not in ClientApp.SM.screen_names:
                self.scroll.children[0].add_widget(Chat(chat_name, 'enter'))
            
    def to_find_chat_screen(self):
        ClientApp.SM.transition.direction = "down"
        ClientApp.SM.current = "chat_finder"

class ClientApp(App):
    title = StringProperty("Messanger")
    SM: ScreenManager = ObjectProperty(None)
    LOGIN: str = ''
    PASSWORD: str = ''
    
    def __init__(self, ip, port):
        super().__init__()
        self.icon = "icon.png"
        ClientApp.session = Session(ip, port)

    def on_stop(self):
        for screen in ClientApp.SM.screens:
            screen.updating = False

    def build(self):
        root = ScreenManager()
        ClientApp.SM = root        
        root.add_widget(LoginScreen())
        root.add_widget(MainMenuScreen())
        root.add_widget(ChatFinderScreen())
        return root

if __name__ == "__main__":
    a = ClientApp('25.19.117.26', '8080').run()
    