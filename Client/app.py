from kivy.app import App 
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import (StringProperty, ObjectProperty, NumericProperty)
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.layout import Layout
from kivy.input.providers.mouse import MouseMotionEvent
from kivy.clock import Clock, mainthread
from network import Session
from functools import partial
from kivy.graphics import Color, Rectangle
import asyncio
import threading
from time import sleep

Window.size = (500, 500)
Window.icon = 'icon.png'
OOO = 0

class Message(Widget):
    message_text: Label = ObjectProperty(None)
    message_time: Label = ObjectProperty(None)
    message_sender: Label = ObjectProperty(None)
    
    def __init__(self, text='', **kwargs):
        super().__init__(**kwargs)
        if not isinstance(text, str):
            raise TypeError("Argument text in message must be str.")
        if len(text) > 200:
            raise Exception("Argument text in message can't contain more than 200 chars.") 
        if text == '':
            self.message_text.text = "Some text"
        else:
            self.message_text.text = text
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
        for i in range(2):
            a = Message()
            self.scroll.children[0].add_widget(a)
            a.resize()
    
    def on_window_resize_messages(self, window, width, height):
        if ClientApp.SM.current == self.chat_name.text:
            for message in self.scroll.children[0].children:
                message.resize()
    
    def resize_messages(self):
        for message in self.scroll.children[0].children:
            message.resize()
            
    def return_back(self):
        ClientApp.SM.transition.direction = "right"
        ClientApp.SM.current = "main_menu"
        
    def send(self):
        message_text = self.input_field.text
        self.input_field.text = ""
        if len(message_text) % 200 == 0 and message_text:
            times = len(message_text)//200
        else:
            times = len(message_text)//200 + 1
        for i in range(times):
            sample = message_text[i*200:(i+1)*200]
            print(sample)
            message = Message(text=sample)
            self.scroll.children[0].add_widget(message)
        
class Chat(Widget):
    chat_icon: Image = ObjectProperty(None)
    chat_name: Label = ObjectProperty(None)
    chat_button: Button = ObjectProperty(None)
        
    def __init__(self):
        super().__init__()
        self.chat_icon.source = "icon.png"
        self.chat_name.text = f"Chat {OOO}"
        self.chat_button.width = Window.width
        self.screen = ChatScreen([1]*10, name=self.chat_name.text)
        ClientApp.SM.add_widget(self.screen)
        
    def enter_chat(self):
        ClientApp.SM.transition.direction = "left"
        ClientApp.SM.current = self.chat_name.text
        ClientApp.SM.current_screen.resize_messages()

class LoginScreen(Screen):
    login_label = ObjectProperty(None)
    login = ObjectProperty(None)
    password = ObjectProperty(None)
    password_label = ObjectProperty(None)
    button = ObjectProperty(None)

    def sign_in(self):
        print("Logined with %s and password %s" % (self.login.text, self.password.text))
        if self.login.text == 'abc' and self.password.text == '1' or self.login.text == '':
            global LOGIN
            global PASSWORD
            LOGIN = self.login.text
            PASSWORD = hash(self.password.text)
            self.manager.current = "main_menu"

class MainMenuScreen(Screen):
    scroll = ObjectProperty(None)
    def __init__(self):
        super().__init__()
        for i in range(10):
            a = Chat()
            self.scroll.children[0].add_widget(a)
            global OOO
            OOO += 1

class ClientApp(App):
    title = StringProperty("Messanger")
    SM: ScreenManager = ObjectProperty(None)
    
    def __init__(self, IP, PORT):
        super().__init__()
        self.icon = "icon.png"

    def build(self):
        root = ScreenManager()
        ClientApp.SM = root        
        root.add_widget(LoginScreen())
        root.add_widget(MainMenuScreen())
        return root
    
if __name__ == "__main__":
    ClientApp('localhost', '8080').run()
    