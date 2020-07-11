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
        self.page, self.cursor = [], 0
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

    def search_on_first_page(self, first_page_bl):
        """
            Создание поиска на первой странице
        :param first_page_bl:
        :return:
        """
        first_page_bl.clear_widgets()

        def searching(name):
            list_of_finded_ancestors = self.family_tree.find(name)
            first_page_bl.clear_widgets()
            first_page_bl.add_widget(TextInput(on_text_validate=checker,
                                               **find_input))

            for ancestor in list_of_finded_ancestors:
                if len(first_page_bl.children) < max_of_finded_people:
                    first_page_bl.add_widget(Button(**button_in_find(ancestor.get('fullname'),
                                                                     self.info_ancestors,
                                                                     ancestor.get('id'))))
            else:
                if 22 - len(first_page_bl.children) > 0:
                    first_page_bl.add_widget(Widget())

        def checker(instance):
            if len(instance.text) > 2:
                searching(instance.text)
                instance.hint_text_color = neutral
                instance.hint_text = 'Введите ФИО'
                instance.text = ''
            else:
                instance.hint_text_color = red
                instance.hint_text = 'Введите не менее трёх символов'
                instance.text = ''

        first_page_bl.add_widget(TextInput(on_text_validate=checker,
                                           **find_input))
        first_page_bl.add_widget(Widget())

    def output_on_first_page(self, first_page_bl, data):
        """
            Вывод информации на первой странице
        :return:
        """
        first_page_bl.clear_widgets()
        for one_person in data:
            first_page_bl.add_widget(Button(**button_for_parents(one_person.get('fullname'),
                                                                 one_person.get('id'),
                                                                 self.info_ancestors,
                                                                 (1, None),
                                                                 font_in_pr_page),
                                            # text_size=font_in_pr_page,
                                            height=35))
        first_page_bl.add_widget(Widget())
        first_page_bl.add_widget(Button(text='Вернутся к поиску',
                                        on_press=lambda x: self.search_on_first_page(first_page_bl),
                                        size_hint_y=None,
                                        height=35,
                                        **unpress_label(font_in_pr_page),
                                        background_color=invisible_background_color))

    def info_ancestors(self, instance):
        """
            Вывод подробной инфы о предке
        """
        self.manager.get_screen('info').clear_widgets()
        sl = BoxLayout(orientation=horizontal,
                       padding=padding_in_find)
        first_page_bl = BoxLayout(orientation=vertical)
        self.search_on_first_page(first_page_bl)
        sl.add_widget(first_page_bl)

        # print(instance.id)
        data, image = self.family_tree.find_full(instance.id)

        # if not self.page:
        #     self.cursor += 1

        if instance.text == 'Вперед':
            if self.cursor != len(self.page) - 1:
                self.cursor += 1
        elif instance.text == 'Назад':
            if self.cursor != 0:
                self.cursor -= 1
        else:
            if len(self.page) >= 1:
                self.cursor += 1
                del self.page[self.cursor:]

            self.page.append(instance.id)

        st = StackLayout(size_hint_y=1)
        sl.add_widget(st)
        st.add_widget(Label(text='Личная карточка',
                            **unpress_label(50),
                            size_hint_y=.1,))
        st.add_widget(Label(text='Родители' if len(data.get('parents')) > 0 else '',
                            **unpress_label(font_in_pr_page),
                            size_hint=(1, .05),
                            ))

        # print(data)

        for parent in data.get('parents'):
            st.add_widget(Button(**button_for_parents(parent.get('fullname').replace(' ', '\n'),
                                                      parent.get('id'),
                                                      self.info_ancestors,
                                                      (.5, .1),
                                                      font_in_pr_page,)))

        if data.get('second_half') and len(data.get('second_half')) > 0:
            if len(data.get('second_half')) > 1:
                st.add_widget(Button(text='Супруги',
                                     on_press=lambda x: self.output_on_first_page(first_page_bl, data.get('second_half')),
                                     **for_more_objects,
                                     **unpress_label(font_in_pr_page)
                                     ))
            else:
                second_half = data.get('second_half')[0]
                mini_bl = BoxLayout(orientation=vertical,
                                    size_hint=(.33,  .35),
                                    )
                mini_bl.add_widget(Label(text=second_half.get('rel'),
                                         **unpress_label(font_in_pr_page)))
                mini_bl.add_widget(Button(**button_for_parents(second_half.get('fullname').replace(' ', '\n'),
                                                               second_half.get('id'),
                                                               self.info_ancestors,
                                                               (1, 1),
                                                               font_in_pr_page),))
                mini_bl.add_widget(Widget())
                st.add_widget(mini_bl)
        else:
            st.add_widget(Label(text='',
                                **unpress_label(font_in_pr_page),
                                size_hint=(.33,  .35),))

        if image:
            st.add_widget(Image(source='static\\' + image[0],
                                size_hint=(.33,  .35)))
        else:
            st.add_widget(Label(text='',
                                **unpress_label(30),
                                size_hint=(.33,  .35)))

        if data.get('bro_and_sis'):
            if len(data.get('bro_and_sis')) > 1:
                st.add_widget(Button(text='Братья и сестры',
                                     on_press=lambda x: self.output_on_first_page(first_page_bl, data.get('bro_and_sis')),
                                     **for_more_objects,
                                     **unpress_label(font_in_pr_page)
                                     ))
            else:
                mini_bl = BoxLayout(orientation=vertical,
                                    size_hint=(.33, .35))

                mini_bl.add_widget(Label(text='Братья и сестры',
                                         **unpress_label(25),
                                         size_hint=(1, .3),
                                         ))
                mini_bl.add_widget(Button(**button_for_parents(data.get('bro_and_sis')[0].get('fullname').replace(' ', '\n'),
                                                               data.get('bro_and_sis')[0].get('fullname').get('id'),
                                                               self.info_ancestors,
                                                               (1, .3),
                                                               25)))
                st.add_widget(mini_bl)
        else:
            st.add_widget(Label(text='',
                                **unpress_label(font_in_pr_page),
                                size_hint=(.33, .35)))

        st.add_widget(Label(text=data.get('fullname') + ('\n' + data.get('bdate') if data.get('bdate') else ''),
                            **unpress_label(font_in_pr_page),
                            size_hint_y=.05,
                            halign='center'))
        # print(data)

        temp_data = ''
        if data.get('comment'):
            news_str = data.get('comment').split()
            for part in range(6, len(news_str), 6):
                news_str[part] += '\n'
            data['comment'] = ' '.join(news_str)
            if len(data.get('comment')) > 400:
                temp_data = data.get('comment')[:400]
                temp_data = temp_data[:temp_data.rfind(' ')] + '...'
            else:
                temp_data = data.get('comment')

        st.add_widget(Button(text=temp_data if data.get('comment') else '',
                             **unpress_label(font_in_pr_page),
                             size_hint_y=.33,
                             halign='center',
                             background_color=invisible_background_color
                             ))

        navigation_bl = BoxLayout(orientation='horizontal',
                                  size_hint_y=.1,)
        st.add_widget(navigation_bl)
        if self.cursor != 0 and len(self.page) >= 2:
            navigation_bl.add_widget(Button(**navigation_buttons('Назад', str(self.page[self.cursor - 1]), self.info_ancestors)))
        if self.cursor < len(self.page) - 1 and len(self.page) >= 2:
            navigation_bl.add_widget(Button(**navigation_buttons('Вперед', str(self.page[self.cursor + 1]), self.info_ancestors)))

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
