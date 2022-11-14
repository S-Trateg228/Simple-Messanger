from kivy.app import App 
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.image import Image

Window.size = (500, 500)
Window.icon = 'icon.png'

class ClientApp(App):
    
    def __init__(self):
        super().__init__()
        self.icon = "icon.png"
        self.title = "Messanger"
        self.login = TextInput()
        self.password = TextInput(password=True)

    def sign_in(self, instance):
        print("Logined with %s and password %s" % (self.login.text, self.password.text))

    def build(self):
        
        root = GridLayout(rows=3, padding=(50,200))

        login = GridLayout(cols=2)
        login.add_widget(Label(text='Login:'))
        login.add_widget(self.login)
        root.add_widget(login)

        password = GridLayout(cols=2)
        password.add_widget(Label(text='Password:'))
        password.add_widget(self.password)
        root.add_widget(password)

        root.add_widget(Button(text="Submit!", on_press=self.sign_in))

        return root

if __name__ == '__main__':
    ClientApp().run()