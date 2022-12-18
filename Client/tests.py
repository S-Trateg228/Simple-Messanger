import unittest
from cryptography.fernet import Fernet
from network import Session
from app import Chat, Message, is_valid_time_format
from os.path import isfile

f = open("server_address.txt")
IP, PORT = f.readline().split(':')
f.close()

DEBUGGING_USER = "DEBUGGER"

class SessionTest(unittest.TestCase):
    
    def test_connect(self):
        new_session = Session("localhost", "0")
        expected_result = False
        self.assertEqual(new_session.connect("any1", "any1", 1), expected_result)
        self.assertEqual(new_session.connect("any2", "any2", 0), expected_result)
        self.assertEqual(new_session.connect("debug", "debug", 0), expected_result)
        
        new_session = Session(IP, PORT)
        new_session.connect("debug", "debug", 1)
        if new_session.ping():
            self.assertEqual(new_session.connect("debug", "debug", 1), False)
            self.assertEqual(new_session.connect("debug", "debug", 0), True)
    
    def test_send_key(self):
        new_session = Session(IP, PORT)
        new_session.login = "debug"
        new_session.password = "debug"
        connected = new_session.connect("debug", "debug", 0)
        if connected:
            if not isfile("keys/DEBUGGER.txt"):
                result = new_session.send_key(DEBUGGING_USER)
                self.assertEqual(result, True)
                with open("keys/DEBUGGER.txt", 'rb') as f:
                    self.assertIsInstance(f.read(), bytes)
    
    def test_get_all_chats(self):
        new_session = Session(IP, PORT)
        new_session.login = "debug"
        new_session.password = "debug"
        connected = new_session.connect("debug", "debug", 0)
        new_session.send_message(DEBUGGING_USER, "some text", "11.11.1111 11:11")
        if connected:
            success, chat_names = new_session.get_all_chats()
            if success:
                [self.assertIsInstance(chat_name, str) for chat_name in chat_names]
                self.assertIn(DEBUGGING_USER, chat_names)
            else:
                self.assertListEqual(chat_names, [])
            
    def test_send_message(self):
        new_session = Session(IP, PORT)
        new_session.login = "debug"
        new_session.password = "debug"
        connected = new_session.connect("debug", "debug", 0)
        if connected:
            result = new_session.send_message(DEBUGGING_USER, "some text", "11.11.1111 11:11")
            self.assertEqual(result, True)
            result = new_session.send_message(DEBUGGING_USER, "some text", "33.02.1111 11:11") #invalid Time Format
            self.assertEqual(result, False)
            result = new_session.send_message(DEBUGGING_USER, "some text", "11:11 11.11.1111") #invalid Time Format
            self.assertEqual(result, False)
        
    def test_find_chats(self):
        new_session = Session(IP, PORT)
        new_session.login = "debug"
        new_session.password = "debug"
        connected = new_session.connect("debug", "debug", 0)
        if connected:
            success, chat_names = new_session.find_chats("debug")
            if success:
                self.assertIn("debug", chat_names)
            else:
                self.assertListEqual(chat_names, [])
        
    def test_get_all_chats(self):
        new_session = Session(IP, PORT)
        new_session.login = "debug"
        new_session.password = "debug"
        connected = new_session.connect("debug", "debug", 0)
        if connected:
            new_session.send_message(DEBUGGING_USER, "some text", "11.11.1111 11:11")
            success, chat_names = new_session.get_all_chats()
            if success:
                self.assertIn(DEBUGGING_USER, chat_names)
            else:
                self.assertListEqual(chat_names, [])
                               
    def test_get_new_messages(self):
        new_session = Session(IP, PORT)
        new_session.login = "debug"
        new_session.password = "debug"
        connected = new_session.connect("debug", "debug", 0)
        if connected:
            new_session.send_message(DEBUGGING_USER, "some text", "11.11.1111 11:11")
            success, messages = new_session.get_new_messages(DEBUGGING_USER, 0)
            print(success, ' success')
            if success:
                texts = [text for idx, text, sender, time in messages]
                self.assertIn("some text", texts)
            else:
                self.assertListEqual(messages, [])
   
class AppTest(unittest.TestCase):
    
    def test_chat_init(self):
        self.assertRaises(ValueError, Chat, "some name", "abcd")
        
    def test_message_init(self):
        self.assertRaises(TypeError, Message, text=1)
        self.assertRaises(TypeError, Message, time=1)
        self.assertRaises(TypeError, Message, text=1)
        self.assertRaises(TypeError, Message, index='1')
        self.assertRaises(TypeError, Message, sender=1)
        self.assertRaises(ValueError, Message, text='1'*300)
        self.assertRaises(ValueError, Message, time='11.11.1111 60:60')
        
    def test_time_format(self):
        self.assertEqual(is_valid_time_format("11.11.1111 11:11"), True)
        self.assertEqual(is_valid_time_format("28.02.1111 23:59"), True)
        self.assertEqual(is_valid_time_format("29.02.2000 11:11"), True)
        self.assertEqual(is_valid_time_format("01.11.1111 00:00"), True)
        self.assertEqual(is_valid_time_format("29.02.2001 11:11"), False)
        self.assertEqual(is_valid_time_format("01.11.1111"), False)
        self.assertEqual(is_valid_time_format("11:11 01.11.1111"), False)
        self.assertEqual(is_valid_time_format("11.11.1111 24:11"), False)
    
if __name__ == "__main__":
    unittest.main()