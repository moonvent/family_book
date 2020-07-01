from kivy.uix.stacklayout import StackLayout
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
        self.manager.add_widget(Screen(name='info'))

    def change_screen(self, screen):
        """
            Функция для смены экрана + отключение анимации, ибо по проекту она не нужна.
        """
        self.manager.current = screen
        self.manager.transition.stop()

    def info_ancestors(self, instance):
        """
            Вывод подробной инфы о предке
        """
        self.manager.get_screen('info').clear_widgets()
        sl = GridLayout(**find_gl)

        data = self.family_tree.find_full(instance.id)
        print(data)
        if data[1]:
            sl.add_widget(Image(source='static\\' + data[1][0],
                                # size_hint=size_hint_pic
                                size_hint_y=data[2]))
        for info in data[0].values():
            if isinstance(info, str):
                sl.add_widget(Button(**button_in_detail(info, data[2])))
            elif info is None:
                sl.add_widget(Widget(size_hint_y=data[2]))
            else:
                gl = GridLayout(**nearest_gl)
                gl.add_widget(Button(**nearest_family))
                for near in info:
                    gl.add_widget(Button(**button_in_find(near.get('rel') + ': ' + near.get('fullname'),
                                                          self.info_ancestors,
                                                          near.get('id'))))
                sl.add_widget(gl)

        self.manager.get_screen('info').add_widget(sl)
        self.change_screen(info_screen)

    def output_finded(self, name, gl):
        """
            Вывод найденных персон в лайаут поиска
        """
        list_of_finded_ancestors = self.family_tree.find(name)

        while len(gl.children) != 1:                # производим полное удаление старых данных поиска
            if gl.children[0].id != 'search':
                gl.remove_widget(gl.children[0])

        for ancestor in list_of_finded_ancestors:
            if len(gl.children) < max_of_finded_people:
                gl.add_widget(Button(**button_in_find(ancestor.get('fullname'),
                                                      self.info_ancestors,
                                                      ancestor.get('id'))))
        else:
            for i in range(46 - len(gl.children)):
                gl.add_widget(Widget(size_hint=(0, 0)))

    def find_screen(self):
        """
            Экран поиска
        """
        screen = Screen(name=find_screen)
        gl = GridLayout(**find_gl)

        def checker(instance):
            if len(instance.text) > 2:
                self.output_finded(instance.text, gl)
                instance.hint_text_color = neutral
                instance.hint_text = 'Введите ФИО'
                instance.text = ''
            else:
                instance.hint_text_color = red
                instance.hint_text = 'Введите не менее трёх символов'
                instance.text = ''

        gl.add_widget(TextInput(on_text_validate=checker,
                                **find_input))
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
