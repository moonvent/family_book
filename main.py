from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from constants import *
Config.set('graphics', 'width', width)
Config.set('graphics', 'height', height)
Config.set('graphics', 'borderless', True)
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class MyApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager = ScreenManager()
        self.manager.add_widget(self.main_screen())

    def main_screen(self):
        screen = Screen(name='main')
        bl = BoxLayout(orientation=bl_hor,
                       padding=padding_in_main,
                       spacing=spacing_in_main)
        bl.add_widget(Button(text='Книга', **main_buttons))
        bl.add_widget(Button(text='Поиск', **main_buttons))
        screen.add_widget(Image(source=picture_in_main))
        screen.add_widget(bl)
        return screen

    def build(self):
        return self.manager


if __name__ == '__main__':
    MyApp().run()
