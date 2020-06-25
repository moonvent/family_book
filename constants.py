from ctypes import windll


"""
############################################################
    Файл со всеми константами использующимися в программе
############################################################
"""

"""
############################################################
    Численные константы
############################################################
"""

spacing_in_main = 100  # отступ между элементами
width = windll.user32.GetSystemMetrics(0)  # ширина экрана
height = windll.user32.GetSystemMetrics(1)  # высота экрана
find_grid_cols = 2  # кол-во колонок в поиске
main_font_size = 60  # размер шрифта на главной странице
row_height = 34  # высота ряда
row_width = 525  # ширина ряда
max_of_finded_people = 46  # кол-во максимальных записей на страницах поиска

"""
############################################################
    Строковые константы
############################################################
"""

horizontal = 'horizontal'  # горизонтальный бокс лайаут
vertical = 'vertical'  # вертикальный бокс лайаут
find_screen = 'find'  # название экрана поиска
main_screen = 'main'  # название главного экрана
info_screen = 'info'  # название персональной карточки предка
top_to_bot = 'tb-rl'  # ориентация изображения предка

"""
############################################################
    Кортежные константы
############################################################
"""

invisible_background_color = (0,) * 4  # невидимый задний фон
padding_in_main = (200,) * 4  # падинги в мейне (чтоб тип на разных страницах)
black = (0, 0, 0, 1)  # черный цвет
padding_in_find = (200, 50) * 2
spacing_in_find = (100, 0)  # расстояние между столбцами в поиске
size_hint_info = (.45, .33)
size_hint_info_with_pic = (.45, .5)

"""
############################################################
    Статические файлы
############################################################
"""

picture_in_main = r'static\1.jpg'  # картинка в мейне
font = r'static\ofont.ru_a_BodoniNovaNr.ttf'  # шрифты
# font = r'static\18800.otf'  # шрифты

"""
############################################################
    Статические словари
############################################################
"""

main_buttons = {'background_color': invisible_background_color,
                'font_name': font,
                'color': black,
                'font_size': main_font_size}

main_bl_props = dict(orientation=horizontal,
                     padding=padding_in_main,
                     spacing=spacing_in_main)

find_gl = dict(cols=2,
               padding=padding_in_find,
               spacing=spacing_in_find,)

row_size = dict(size_hint=(None, None),
                height=row_height,
                width=row_width,
                background_color=invisible_background_color)

stack_layout = dict(orientation=top_to_bot,
                    padding=padding_in_find,
                    spacing=spacing_in_find)

find_input = dict(hint_text='Введите ФИО',
                  multiline=False,
                  id='search',
                  **row_size)



