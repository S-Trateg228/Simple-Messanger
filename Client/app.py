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

from functools import partial

Window.size = (500, 500)
Window.icon = 'icon.png'
OOO = 0
class Chat(Widget):
    chat_icon: Image = ObjectProperty(None)
    chat_name: Label = ObjectProperty(None)
    enter_chat: Button = ObjectProperty(None)
    
    def __init__(self):
        super().__init__()
        self.chat_icon.source = "icon.png"
        self.chat_name.text = f"Chat {OOO}"
        self.enter_chat.width = Window.width
        
    def abc(self):
        print(f"{self.chat_name.text} is Pressed!!!!!!!!!")

class LoginScreen(Screen):
    login_label = ObjectProperty(None)
    login = ObjectProperty(None)
    password = ObjectProperty(None)
    password_label = ObjectProperty(None)
    button = ObjectProperty(None)

    def sign_in(self):
        print("Logined with %s and password %s" % (self.login.text, self.password.text))
        if self.login.text == 'abc' and self.password.text == '1':
            global LOGIN
            global PASSWORD
            LOGIN = self.login.text
            PASSWORD = hash(self.password.text)
            self.manager.current = "main_menu"


class MainMenuScreen(Screen):
    scroll = ObjectProperty(None)
    def __init__(self):
        super().__init__()
        total_height = 100*20 + 99*40
        self.scroll.width = Window.width
        self.scroll.children[0].height = total_height
        for i in range(100):
            a = Chat()
            self.scroll.children[0].add_widget(a)
            global OOO
            OOO += 1

class ClientApp(App):
    title = StringProperty("Messanger")
    def __init__(self):
        super().__init__()
        self.icon = "icon.png"

    def build(self):
        root = ScreenManager()
        root.add_widget(LoginScreen())
        root.add_widget(MainMenuScreen())
        return root

if __name__ == "__main__":
    ClientApp().run()
    