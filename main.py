from constants import *
from kivy.config import Config
from work_with_file import FamilyTree
Config.set('graphics', 'width', width)
Config.set('graphics', 'height', height)
Config.set('graphics', 'borderless', True)
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class MyApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.add_widget(Image(source=picture_in_main))
        self.family_tree = FamilyTree()
        self.manager = ScreenManager()
        self.manager.add_widget(self.main_screen())
        self.manager.add_widget(self.find_screen())

    def change_screen(self, screen):
        """
            Функция для смены экрана + отключение анимации, ибо по проекту она не нужна.
        """
        self.manager.current = screen
        self.manager.transition.stop()

    def output_finded(self, name, gl):
        list_of_finded_ancestors = self.family_tree.find(name)

        while len(gl.children) != 1:                # производим полное удаление старых данных поиска
            if gl.children[0].id != 'search':
                gl.remove_widget(gl.children[0])

        for ancestor in list_of_finded_ancestors:
            if len(gl.children) < max_of_finded_people:
                gl.add_widget(Button(text=ancestor[0],
                                     on_press=lambda x: print('valid'),
                                     **row_size))
        else:
            gl.add_widget(Widget())
            if len(gl.children) % 2 == 0:
                gl.add_widget(Widget())

    def find_screen(self):
        """
            Экран поиска
        """
        screen = Screen(name=find_screen)
        gl = GridLayout(**find_gl)
        gl.add_widget(TextInput(hint_text='Введите ФИО',
                                multiline=False,
                                on_text_validate=lambda x: self.output_finded(x.text, gl),
                                id='search',
                                **row_size))
        gl.add_widget(Widget())
        gl.add_widget(Widget())
        screen.add_widget(gl)
        return screen

    def main_screen(self):
        """
            Создание главного меню, которое отображается при входе
        """
        screen = Screen(name=main_screen)
        bl = BoxLayout(**main_bl_props)
        bl.add_widget(Button(text='Книга',
                             **main_buttons))
        bl.add_widget(Button(text='Поиск',
                             on_press=lambda x: self.change_screen('find'),
                             **main_buttons))
        screen.add_widget(bl)
        return screen

    def build(self):
        return self.manager


if __name__ == '__main__':
    MyApp().run()
