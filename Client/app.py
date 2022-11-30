from kivy.app import App 
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import (StringProperty, ObjectProperty)
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

Window.size = (500, 500)
Window.icon = 'icon.png'

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
    label = ObjectProperty(None)

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
    