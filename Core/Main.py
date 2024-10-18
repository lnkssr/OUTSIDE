from flet import *
from time import sleep
from random import choice

from Core.Config import *
from Core.Run import start_async_attacks
from Core.Attack.Services import urls
from Core.Attack.Feedback_Services import feedback_urls
from Core.TBanner import banner

SIZE = 70

class OutsideBomberApp:
    def __init__(self, page: Page):
        '''Инициализация окна бомбера'''
        self.page = page
        self.color = check_config()['color']
        self.page_setup()
        self.create_ui_elements()
        self.add_elements()

    def page_setup(self):
        '''Настройка страницы'''
        self.page.window_center()
        self.page.title = 'OUTSIDE'
        self.page.scroll = 'adaptive'
        self.page.auto_scroll = True
        self.page.window_width = 450
        self.page.window_height = 720
        self.page.vertical_alignment = 'center'
        self.page.horizontal_alignment = 'center'
        self.page.theme_mode = check_config()['theme']
        self.page.window_maximizable = False
        self.page.window_resizable = False
        change_config('attack', 'False')

    def create_ui_elements(self):
        '''Создание элементов интерфейса'''
        self.number = self.create_textfield(label='Введите номер без знака "+"', width=275)
        self.replay = self.create_textfield(label='Круги', width=131, value='1')

        self.type_attack = self.create_dropdown(label='Тип атаки', 
                                                options=['MIX', 'SMS', 'CALL'], 
                                                value=check_config()['type_attack'], 
                                                on_change=self.update_config('type_attack'))
                                                
        self.feedback = self.create_switch(label='Сервисы обратной связи (?)', 
                                           value=check_config()['feedback'] == 'True', 
                                           on_change=self.update_config('feedback'),
                                           tooltip='Сервисы, которые оставляют заявки...')  # Tooltip для переключателя

        self.attack_button = self.create_button('Атака', self.checking_values, width=190, height=60)
        self.banner = self.create_banner()

        self.icon_buttons = self.create_icon_buttons()

    def create_textfield(self, label, width, value='', on_change=None):
        '''Создание текстового поля'''
        return TextField(
            label=label, width=width, text_align='center', value=value,
            border_radius=40, border_color=self.color, cursor_color=self.color, 
            focused_border_color=self.color, selection_color=self.color, 
            label_style=TextStyle(color=self.color))

    def create_dropdown(self, label, options, value, on_change):
        '''Создание выпадающего списка'''
        return Dropdown(
            label=label, hint_text='Выберите тип атаки',
            options=[dropdown.Option(opt) for opt in options],
            width=131, border_radius=40, value=value,
            alignment=alignment.bottom_center,
            border_color=self.color, label_style=TextStyle(color=self.color),
            on_change=on_change)

    def create_switch(self, label, value, on_change, tooltip=None):
        '''Создание переключателя с подсказкой'''
        switch = Switch(
            label=label, value=value, width=280, 
            active_color=self.color, on_change=on_change)

        # Если указана подсказка, добавляем её
        if tooltip:
            switch.tooltip = tooltip

        return switch

    def create_button(self, text, on_click, width=100, height=40):
        '''Создание кнопки'''
        return ElevatedButton(
            content=Text(text, size=25), 
            on_click=on_click, width=width, height=height, color=self.color)

    def create_banner(self):
        '''Создание баннера'''
        return Stack([
            Text(spans=[TextSpan('OUTSIDE', TextStyle(size=SIZE, 
                    foreground=Paint(color=self.color, stroke_width=9, 
                    stroke_join='round', style='stroke')))], font_family='Consolas'),
            Text(spans=[TextSpan('OUTSIDE', TextStyle(size=SIZE, color=self.color))], font_family='Consolas')
        ])

    def create_icon_buttons(self):
        '''Создание иконок кнопок'''
        icons = ['info', 'color_lens_sharp', 'mode_night']
        tooltips = ['Информация', 'Цвет (рандом)', 'Тема']
        functions = [self.information, self.color_change, self.theme_change]
        return Row([
            IconButton(icon=icons[i], icon_size=48, tooltip=tooltips[i], 
                       icon_color=self.color, on_click=functions[i])
            for i in range(3)], alignment='CENTER')

    def add_elements(self):
        '''Добавление всех элементов на страницу'''
        self.page.add(
            Text('\n', size=6),
            self.banner,
            Text('\n', size=12),
            self.number,
            Row([self.type_attack, self.replay], alignment='CENTER'),
            self.feedback,
            self.attack_button,
            Text('\n', size=12),
            self.icon_buttons
        )

    def update_config(self, key):
        '''Обновление конфигурации при изменении значения'''
        def wrapper(e):
            change_config(key, str(e.control.value))
        return wrapper

    def update_banner(self):
        '''Обновление баннера и цвета элементов'''
        self.banner.controls[0].spans[0].style.foreground.color = self.color
        self.banner.controls[1].spans[0].style.color = self.color

    def update_elements_color(self):
        '''Обновление цвета всех элементов интерфейса'''
        # Создаем список элементов, которые нуждаются в обновлении цвета
        elements_to_update = [self.number, self.replay, self.type_attack, self.feedback, self.attack_button]

        # Применяем цвет к каждому элементу
        for el in elements_to_update:
            el.border_color = self.color

            # Если элемент имеет особенные свойства для обновления, меняем их
            if isinstance(el, TextField) or isinstance(el, Dropdown):
                el.cursor_color = self.color
                el.focused_border_color = self.color
                el.label_style = TextStyle(color=self.color)

            if isinstance(el, Switch):
                el.active_color = self.color

            if isinstance(el, ElevatedButton):
                el.color = self.color
                el.content = Text(el.content.value, size=25, color=self.color)

        # Обновляем цвет иконок
        for icon_button in self.icon_buttons.controls:
            icon_button.icon_color = self.color

    def theme_change(self, e):
        '''Смена темы'''
        self.page.theme_mode = 'dark' if self.page.theme_mode == 'light' else 'light'
        self.page.update()
        change_config('theme', self.page.theme_mode)

    def color_change(self, e):
        '''Смена цвета'''
        colors = ['red', 'pink', 'white', 'black', 'purple', 'indigo', 'blue', 'cyan', 
                  'teal', 'green', 'lime', 'yellow', 'amber', 'orange', 'brown', 
                  'bluegrey', 'grey']
        self.color = choice(colors)
        self.update_banner()
        self.update_elements_color()
        self.page.update()
        change_config('color', self.color)

    def error(self, message, reason='Ошибка'):
        '''Показ окна с ошибкой'''
        self.show_dialog(reason, message, 'ОКЕЙ')

    def show_dialog(self, title, content, button_text, button_action=None):
        '''Универсальная функция для показа диалоговых окон'''
        def close_dialog(e):
            self.page.dialog.open = False
            self.page.update()

        dialog = AlertDialog(
            title=Text(title, color=self.color, size=30, text_align='center', font_family='Consolas'),
            content=Text(content, font_family='Consolas'),
            actions=[TextButton(button_text, on_click=button_action or close_dialog, style=ButtonStyle(color=self.color))],
            actions_alignment='end'
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def checking_values(self, e):
        '''Проверка введённых данных перед атакой'''
        if not self.number.value or not self.number.value.isdigit():
            self.error('Введите корректный номер!')
            return

        if not self.replay.value.isdigit() or not (1 <= int(self.replay.value) <= 50):
            self.error('Введите количество кругов от 1 до 50!')
            return

        if check_config()['attack'] == 'False':
            self.confirmation()
        else:
            self.error('Слишком много атак, подождите!')

    def confirmation(self):
        '''Окно подтверждения атаки'''
        self.show_dialog('Внимание!', 
            'После запуска атаки и её отмены, она всё равно выполнится до конца!\n\nПродолжить?', 
            'ДА', self.start_attack)

    def start_attack(self, e=None):
        '''Запуск атаки'''
        self.show_dialog('Атака запущена...', '', 'Закрыть')
        change_config('attack', 'True')
        start_async_attacks(self.number.value, self.replay.value)
        change_config('attack', 'False')

    def information(self, e):
        '''Информация о сервисах'''
        services_count = len(urls("12345"))
        feedback_count = len(feedback_urls("12345"))
        info_text = f'''Сервисов - {services_count}\nRU - {sum(1 for i in urls("12345") if i["info"]["country"] == "RU")}\nФидбек Сервисов - {feedback_count}'''
        self.show_dialog(f'OUTSIDE V{VERSION}', info_text, 'ОКЕЙ')

def main(page: Page):
    '''Запуск приложения'''
    app = OutsideBomberApp(page)

def Start(web=True):
    '''Стартовое окно'''
    if web:
        host, port = '127.0.0.1', 3030
        banner(host, port)
        app(main, view='web_browser', host=host, port=port)
    else:
        app(main)
