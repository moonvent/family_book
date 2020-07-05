from kivy.uix.label import Label
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
        sl = BoxLayout(orientation=horizontal,
                       padding=padding_in_find)

        sl.add_widget(Widget())

        data, image = self.family_tree.find_full(instance.id)

        st = StackLayout(size_hint_y=1)
        sl.add_widget(st)
        st.add_widget(Label(text='Личная карточка',
                            **unpress_label(50),
                            size_hint_y=.1,))
        st.add_widget(Label(text='Родители' if len(data.get('parents')) > 0 else '',
                            **unpress_label(25),
                            size_hint=(1, .05),
                            ))

        # print(data)

        for parent in data.get('parents'):
            st.add_widget(Button(**button_for_parents(parent.get('fullname').replace(' ', '\n'),
                                                      parent.get('id'),
                                                      self.info_ancestors,
                                                      (.5, .1),
                                                      25,)))

        if data.get('second_half') and len(data.get('second_half')) > 0:
            second_half = data.get('second_half')[0]
            mini_bl = BoxLayout(orientation=vertical,
                                size_hint=(.33, .5))
            mini_bl.add_widget(Label(text=second_half.get('rel'),
                                     **unpress_label(25)))
            mini_bl.add_widget(Button(**button_for_parents(second_half.get('fullname').replace(' ', '\n'),
                                                           second_half.get('id'),
                                                           self.info_ancestors,
                                                           (1, 1),
                                                           25),))
            mini_bl.add_widget(Widget())
            st.add_widget(mini_bl)
        else:
            st.add_widget(Label(text='',
                                **unpress_label(25),
                                size_hint=(.33, .5),))

        if image:
            st.add_widget(Image(source='static\\' + image[0],
                                size_hint=(.33, .5)))
        else:
            st.add_widget(Label(text='',
                                **unpress_label(30),
                                size_hint=(.33, .5)))

        if data.get('bro_and_sis'):
            label = 'Братья и сестры'
            mini_bl = BoxLayout(orientation=vertical,
                                size_hint=(.33, .5))

            mini_bl.add_widget(Label(text=label,
                                     **unpress_label(25),
                                     size_hint=(1, .3),
                                     ))
            for bro_or_sis in data.get('bro_and_sis')[:2]:
                mini_bl.add_widget(Button(**button_for_parents(bro_or_sis.get('fullname').replace(' ', '\n'),
                                                               bro_or_sis.get('id'),
                                                               self.info_ancestors,
                                                               (1, .3),
                                                               25)))
            st.add_widget(mini_bl)
        else:
            st.add_widget(Label(text='',
                                **unpress_label(25),
                                size_hint=(.33, .5)))

        st.add_widget(Label(text=data.get('fullname') + ('\n' + data.get('bdate') if data.get('bdate') else ''),
                            **unpress_label(25),
                            size_hint_y=.1,
                            halign='center'))
        # print(data)

        st.add_widget(Label(text=data.get('comment') if data.get('comment') else '',
                            **unpress_label(25),
                            size_hint_y=.2,
                            halign='center'))

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
        Window.add_widget(Image(source=picture_in_main))
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
