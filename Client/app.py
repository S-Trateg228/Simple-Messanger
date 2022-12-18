from kivy.app import App 
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import (StringProperty, ObjectProperty)
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.clock import mainthread
from network import Session
import threading
from time import sleep, strptime
from datetime import datetime as dt
from network import Session

Window.size = (500, 500)
Window.icon = 'icon.png'
TIME_FORMAT = "%d.%m.%Y %H:%M"

def is_valid_time_format(time: str) -> bool:
    """Проверяет совпадает ли формат времени со следующим DD.MM.YYYY hh:mm.

        :param time: время для проверки
        :type time: str

        :returns: True - формат совпадает
        :rtype: bool
    """
    try:
        strptime(time, TIME_FORMAT)
        return True
    except ValueError:
        return False

class ChatFinderScreen(Screen):
    "Окно, отвечающее за нахождение пользователей по имени."
    scroll: ScrollView = ObjectProperty(None)
    back_button: Button = ObjectProperty(None)
    input_field: TextInput = ObjectProperty(None)
    find_chat_button: Button = ObjectProperty(None)
    
    def return_back(self):
        "Нажатие кнопки возвращает обратно в главное меню."
        ClientApp.SM.transition.direction = "up"
        ClientApp.SM.current = "main_menu"
    
    @mainthread
    def add_chats_to_scroll(self, chat_names: list[str]):
        """Добавление чата в двигающееся меню.

        :param chat_names: список чатов для добавления
        :type chat_names: list[str]
        """
        for chat_name in chat_names:
            self.scroll.children[0].add_widget(Chat(chat_name, 'add'))
    
    def find_chat(self):
        "Получает с сервера список чатов по имени."
        def threaded_find_chat():    
            success, chat_names = ClientApp.session.find_chats(self.input_field.text)
            if success:
                self.add_chats_to_scroll(chat_names)
        threading.Thread(target=threaded_find_chat).start()

class Message(Widget):
    "Виджет-сообщение. Имеет 3 строки: текст сообщения, отправитель, время отправки."
    message_text: Label = ObjectProperty(None)
    message_time: Label = ObjectProperty(None)
    message_sender: Label = ObjectProperty(None)
    
    def __init__(self, text: str='', sender: str='', time: str='', index: int=0, **kwargs):
        """Инициализация сообщения.

        :param text: текст сообщения (содержит максимум 200 символов)
        :type text: str
        
        :param sender: отправитель
        :type sender: str
        
        :param time: время отправки формата DD.MM.YYYY hh:mm
        :type time: str
        
        :param index: индекс сообщения
        :type index: int
        """
        super().__init__(**kwargs)
        if not isinstance(text, str):
            raise TypeError("Argument text in message must be str.")
        if len(text) > 200:
            raise ValueError("Argument text in message can't contain more than 200 chars.")
        if not isinstance(sender, str):
            raise TypeError("Argument sender in message must be str.")
        if not isinstance(index, int):
            raise TypeError("Argument index in message must be int.")
        if not isinstance(time, str):
            raise TypeError("Argument time in message must be str.")
        if not is_valid_time_format(time):
            raise ValueError("Invalid time format.")
         
        if text == '':
            self.message_text.text = "Some text"
        else:
            self.message_text.text = text
        if sender:
            self.message_sender.text = sender
        else:
            self.message_sender.text = "Some sender"
        self.message_time.text = time
        self.index = index
        self.resize()
            
    def resize(self):
        "Подгоняет размер сообщения под размер окна приложения."
        self.message_text.text_size[0] = Window.width - 20
        self.message_text.texture_update()
        self.height = self.message_text.height + 40

class ChatScreen(Screen):
    "Окно конкретного чата."
    scroll: ScrollView = ObjectProperty(None)
    back_button: Button = ObjectProperty(None)
    chat_name: Label = ObjectProperty(None)
    input_field: TextInput = ObjectProperty(None)
    send_button: Button = ObjectProperty(None)
    is_file_check_box: CheckBox = ObjectProperty(None)
    def __init__(self, **kwargs):
        "Инициализация окна чата."
        super().__init__(**kwargs)
        self.chat_name.text = kwargs["name"]
        self.scroll.width = Window.width
        Window.bind(on_resize=self.on_window_resize_messages)
    
    @mainthread        
    def add_message(self, text: str='', sender: str='', time: str='', index: int=0):
        """Добавляет сообщение по заданному тексту, отправителю, 
        времени отправки, и индексу в прокручивающееся меню.

        :param text: текст сообщения
        :type text: str
        
        :param sender: отправитель
        :type sender: str
        
        :param time: время отправки формата DD.MM.YYYY hh:mm
        :type time: str
        
        :param index: индекс сообщения
        :type index: int
        """
        self.scroll.children[0].add_widget(Message(text=text, sender=sender, time=time, index=index))
    
    def on_window_resize_messages(self, *args):
        """Изменяет размер каждого сообщения в чате.
        Вызывается при изменении размера окна приложения."""
        if ClientApp.SM.current == self.chat_name.text:
            for message in self.scroll.children[0].children:
                message.resize()
                
    def on_enter(self, *args):
        "При входе в чат начинается обновление сообщений с сервера."
        threading.Thread(target=self.update_messages).start()
    
    def on_leave(self, *args):
        "При выходе из чата сообщения перестают обновлятся."
        self.updating = False
    
    def update_messages(self):
        "Обновление сообщений с сервера."
        self.updating = True
        while True:
            print('update')
            if not self.updating:
                break
            current_messages = self.scroll.children[0].children
            idx = 0 if len(current_messages) == 0 else current_messages[0].index
            success, news = ClientApp.session.get_new_messages(self.chat_name.text.split(maxsplit=1)[1], idx)
            if success:
                for new_idx, message_text, sender, time in news:
                    print(new_idx, message_text, sender, time)
                    self.add_message(text=message_text, sender=sender, index=new_idx, time=time)
            sleep(2)

    def resize_messages(self):
        "Изменяет размер каждого сообщения в чате."
        for message in self.scroll.children[0].children:
            message.resize()

    def return_back(self):
        "Возвращается в главное меню при нажатии кнопки."
        ClientApp.SM.transition.direction = "right"
        ClientApp.SM.current = "main_menu"
        
    def send(self):
        "Отправка сообщения на сервер."
        message_text = self.input_field.text
        self.input_field.text = ""
        
        def threaded_send(text):
            success = ClientApp.session.send_message(self.chat_name.text.split(maxsplit=1)[1], text, dt.now().strftime(TIME_FORMAT))
            if not success:
                print("Message has NOT be sent!")
        
        def threaded_send_file(filename):
            print('tryes to send file')
            success = ClientApp.session.send_file(self.chat_name.text.split(maxsplit=1)[1], filename, dt.now().strftime(TIME_FORMAT))
            if not success:
                print("Document has NOT been sent!")
        
        if self.is_file_check_box.active:
            threading.Thread(target=threaded_send_file, args=[message_text]).start()
            return
        
        if len(message_text) % 200 == 0 and message_text:
            times = len(message_text)//200
        else:
            times = len(message_text)//200 + 1
        for i in range(times):
            sample = message_text[i*200:(i+1)*200]
            threading.Thread(target=threaded_send, args=[sample]).start()        

class Chat(Widget):
    "Виджет-чат. Является отображением конкретного чата."
    chat_icon: Image = ObjectProperty(None)
    chat_name: Label = ObjectProperty(None)
    chat_button: Button = ObjectProperty(None)
        
    def __init__(self, chat_name: str, b_type: str="enter"):
        """Инициализация. 
        При b_type "enter" входит в чат при нажатии на виджет.
        При b_type "add" добавляет чат в главное меню при нажатии на виджет.

        :param chat_name: имя чата
        :type chat_name: str
        
        :param b_type: тип поведения
        :type sender: str
        """
        super().__init__()
        
        if b_type not in ("enter", "add"):
            raise ValueError("No such type of ChatWidget Button. It must be 'enter' or 'add'")
        
        self.chat_icon.source = "icon.png"
        self.chat_name.text = chat_name
        self.button_type = b_type
        self.chat_button.width = Window.width
        if b_type == "enter":
            screen = ChatScreen(name=f"Chat {self.chat_name.text}")
            ClientApp.SM.add_widget(screen)
    
    def activate(self):
        """При b_type "enter" входит в чат.
        При b_type "add" добавляет чат в главное меню."""
        match self.button_type:
            case "enter":
                self.enter_chat()
            case "add":
                self.add_chat()
    
    def add_chat(self):
        "Добавление чата в главное меню."
        if f"Chat {self.chat_name.text}" not in ClientApp.SM.screen_names:
            ClientApp.SM.get_screen("main_menu").scroll.children[0].add_widget(Chat(self.chat_name.text))
        
    def enter_chat(self):
        "Вход в чат."
        ClientApp.SM.transition.direction = "left"
        ClientApp.SM.current = f"Chat {self.chat_name.text}"
        ClientApp.SM.current_screen.resize_messages()

class LoginScreen(Screen):
    "Начальное окно. Отвечает за авторизацию и регистрацию пользователя."
    login: TextInput = ObjectProperty(None)
    password: TextInput = ObjectProperty(None)
    button: Button = ObjectProperty(None)
    check_box: CheckBox = ObjectProperty(None)

    @mainthread
    def to_main_menu_screen(self):
        "Переход в главное меню."
        self.manager.current = "main_menu"

    def sign_in(self):
        """Авторизуется или регистрируется на сервере.
        При успехе входит в главное меню."""
        def threaded_sign_in():
            success = ClientApp.session.connect(self.login.text, self.password.text, self.check_box.active)
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
        "Начинает обновлять все свои чаты при входе в главное меню."
        threading.Thread(target=self.update_chats).start()
        
    def on_leave(self, *args):
        "Прекращает обновлять чаты при выходе из главного меню."
        self.updating = False
    
    def update_chats(self):
        "Обновление списка чатов."
        self.updating = True
        while True:
            if not self.updating:
                break
            success, chat_names = ClientApp.session.get_all_chats()
            if success:
                self.add_chats_to_scroll(chat_names)
            sleep(5)
    
    @mainthread
    def add_chats_to_scroll(self, chat_names: list[str]):
        """Добавление чатов в прокручивающийся список по имени.
        
        :param chat_names: имена чатов
        :type chat_names: list[str]
        """
        for chat_name in chat_names:
            if f"Chat {chat_name}" not in ClientApp.SM.screen_names:
                self.scroll.children[0].add_widget(Chat(chat_name, 'enter'))
            
    def to_find_chat_screen(self):
        "Переход в меню поиска чатов."
        ClientApp.SM.transition.direction = "down"
        ClientApp.SM.current = "chat_finder"

class ClientApp(App):
    "Главное приложение."
    title = StringProperty("Messanger")
    SM: ScreenManager = ObjectProperty(None)
    LOGIN: str = ''
    PASSWORD: str = ''
    
    def __init__(self, ip: str, port: str):
        """Инициализация приложения.
        
        :param ip: ip-адрес сервера для подключения
        :type ip: str
        
        :param port: port сервера для подключения
        :type port: str"""
        
        super().__init__()
        self.icon = "icon.png"
        ClientApp.session = Session(ip, port)

    def on_stop(self):
        "Останавливает обновление чатов и сообщений при закрытии приложения."
        for screen in ClientApp.SM.screens:
            screen.updating = False

    def build(self):
        "Формирование окон приложения."
        root = ScreenManager()
        ClientApp.SM = root        
        root.add_widget(LoginScreen())
        root.add_widget(MainMenuScreen())
        root.add_widget(ChatFinderScreen())
        return root

if __name__ == "__main__":
    ClientApp('25.19.117.26', '8080').run()
