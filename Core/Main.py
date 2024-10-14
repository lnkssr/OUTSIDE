from flet import *
from time import sleep
from random import choice

from Core.Config import *
from Core.Run import start_async_attacks
from Core.Attack.Services import urls
from Core.Attack.Feedback_Services import feedback_urls
from Core.TBanner import banner


class OutsideBomberApp:
    def __init__(self, page: Page):
        '''Инициализация окна бомбера'''
        self.page = page
        self.color = check_config()['color']
        self.page_setup()

        self.number = self.create_textfield(label='Введите номер без знака "+"', width=275)
        self.replay = self.create_textfield(label='Круги', width=131, value='1')

        self.type_attack = self.create_dropdown(label='Тип атаки', options=['MIX', 'SMS', 'CALL'], value=check_config()['type_attack'], on_change=self.type_attack_change)
        self.feedback = self.create_switch(label='Сервисы обратной связи (?)', value=check_config()['feedback'] == 'True', on_change=self.feedback_change)

        self.attack_button = self.create_button('Атака', self.checking_values, width=190, height=60)

        self.banner = self.create_banner()
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

    def create_textfield(self, label, width, value='', on_change=None):
        '''Создание текстового поля'''
        return TextField(label=label, width=width, text_align='center', border_radius=40,
                         border_color=self.color, cursor_color=self.color, focused_border_color=self.color,
                         selection_color=self.color, value=value, label_style=TextStyle(color=self.color))

    def create_dropdown(self, label, options, value, on_change):
        '''Создание выпадающего списка'''
        return Dropdown(label=label, hint_text='Выберите тип атаки',
                        options=[dropdown.Option(opt) for opt in options],
                        width=131, border_radius=40, value=value,
                        alignment=alignment.bottom_center,
                        border_color=self.color, label_style=TextStyle(color=self.color),
                        on_change=on_change)

    def create_switch(self, label, value, on_change):
        '''Создание переключателя'''
        return Switch(label=label, value=value, width=280, active_color=self.color,
                      on_change=on_change, tooltip='Сервисы, которые оставляют заявки...')

    def create_button(self, text, on_click, width=100, height=40):
        '''Создание кнопки'''
        return ElevatedButton(content=Text(text, size=25), on_click=on_click, width=width, height=height, color=self.color)

    def create_banner(self):
        '''Создание баннера'''
        return Stack([
            Text(spans=[TextSpan('OUTSIDE', TextStyle(size=95, foreground=Paint(color=self.color, stroke_width=9, stroke_join='round', style='stroke')))], font_family='Consolas'),
            Text(spans=[TextSpan('OUTSIDE', TextStyle(size=95, color=self.color))], font_family='Consolas')
        ])

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
            Row([
                IconButton(icon='info', icon_size=48, tooltip='Информация', icon_color=self.color, on_click=self.information),
                IconButton(icon='color_lens_sharp', icon_size=48, tooltip='Цвет (рандом)', icon_color=self.color, on_click=self.color_change),
                IconButton(icon='mode_night', icon_size=48, tooltip='Тема', on_click=self.theme_change, icon_color=self.color)
            ], alignment='CENTER')  # Добавляем все иконки в один Row
        )

    def type_attack_change(self, e):
        '''Изменение типа атаки'''
        change_config('type_attack', f'{self.type_attack.value}')

    def feedback_change(self, e):
        '''Изменение состояния сервисов обратной связи'''
        change_config('feedback', f'{self.feedback.value}')

    def theme_change(self, e):
        '''Смена темы'''
        self.page.theme_mode = 'dark' if self.page.theme_mode == 'light' else 'light'
        self.page.update()
        change_config('theme', f'{self.page.theme_mode}')

    def color_change(self, e):
        '''Смена цвета'''
        colors = ['red', 'pink', 'white', 'black', 'purple', 'indigo', 'blue', 'cyan', 'teal', 'green', 'lime', 'yellow', 'amber', 'orange', 'brown', 'bluegrey', 'grey']
        self.color = choice(colors)
        self.update_banner()
        self.update_all_elements_color()  # Обновляем цвет всех элементов
        change_config('color', self.color)

    def update_banner(self):
        '''Обновление баннера и цвета элементов'''
        self.banner.controls = [
            Text(spans=[TextSpan('OUTSIDE', TextStyle(size=95, foreground=Paint(color=self.color, stroke_width=9, stroke_join='round', style='stroke')))], font_family='Consolas'),
            Text(spans=[TextSpan('OUTSIDE', TextStyle(size=95, color=self.color))], font_family='Consolas')
        ]
    
    def update_all_elements_color(self):
        '''Обновление цвета всех элементов интерфейса'''
        # Обновляем все основные элементы
        self.number.border_color = self.color
        self.number.cursor_color = self.color
        self.number.focused_border_color = self.color
        self.number.selection_color = self.color
        self.number.label_style = TextStyle(color=self.color)

        self.replay.border_color = self.color
        self.replay.cursor_color = self.color
        self.replay.focused_border_color = self.color
        self.replay.selection_color = self.color
        self.replay.label_style = TextStyle(color=self.color)

        self.type_attack.border_color = self.color
        self.type_attack.label_style = TextStyle(color=self.color)

        self.feedback.active_color = self.color

    # Обновляем цвет кнопки "АТАКА"
        self.attack_button.color = self.color
        self.attack_button.content = Text('Атака', size=25, color=self.color)  # Обновляем цвет текста кнопки

    # Обновляем иконки
        for element in self.page.controls:
            if isinstance(element, Row):
                for icon_button in element.controls:
                    if isinstance(icon_button, IconButton):
                        icon_button.icon_color = self.color

        # Очищаем и перерисовываем страницу с обновлёнными элементами
        self.page.clean()
        self.add_elements()


    def error(self, message, reason='Ошибка'):
        '''Показ окна с ошибкой'''
        def close_error(e):
            self.page.dialog.open = False
            self.page.update()

        error_dialog = AlertDialog(
            title=Text(reason, color=self.color, size=30, text_align='center', font_family='Consolas'),
            content=Text(message, font_family='Consolas'),
            actions=[TextButton('ОКЕЙ', on_click=close_error, style=ButtonStyle(color=self.color))],
            actions_alignment='end'
        )
        self.page.dialog = error_dialog
        error_dialog.open = True
        self.page.update()

    def checking_values(self, e):
        '''Проверка введённых данных перед атакой'''
        if not self.number.value or not self.number.value.isdigit():
            self.error('Введите корректный номер!')
            self.number.focus()
            return

        if not self.replay.value or not self.replay.value.isdigit() or not (1 <= int(self.replay.value) <= 50):
            self.error('Введите количество кругов от 1 до 50!')
            self.replay.focus()
            return

        if check_config()['attack'] == 'False':
            self.confirmation()
        else:
            self.error('Слишком много атак, подождите!')

    def confirmation(self):
        '''Окно подтверждения атаки'''
        def cancel(e):
            self.page.dialog.open = False
            self.page.update()

        def confirm(e):
            self.page.dialog.open = False
            self.page.update()
            sleep(1)
            self.start_attack()

        confirmation_dialog = AlertDialog(
            title=Text('Внимание!', color=self.color, size=30, text_align='center'),
            content=Text('После запуска атаки и её отмены,\nона всё равно выполнится до конца!\n\nПродолжить?'),
            actions=[TextButton('НЕТ', on_click=cancel, style=ButtonStyle(color=self.color)),
                     TextButton('ДА', on_click=confirm, style=ButtonStyle(color=self.color))],
            actions_alignment='end'
        )
        self.page.dialog = confirmation_dialog
        confirmation_dialog.open = True
        self.page.update()

    def start_attack(self):
        '''Запуск атаки'''
        def close_attack(e):
            self.page.dialog.open = False
            self.page.update()

        attack_dialog = AlertDialog(
            modal=True,
            title=Text('Атака запущена...', color=self.color, size=30, text_align=TextAlign.CENTER),
            content=ProgressBar(width=325, color=self.color),
            actions=[TextButton('Закрыть', width=90, height=40, on_click=close_attack, style=ButtonStyle(color=self.color))],
            actions_alignment='end'
        )
        self.page.dialog = attack_dialog
        attack_dialog.open = True
        self.page.update()

        change_config('attack', 'True')
        start_async_attacks(self.number.value, self.replay.value)
        change_config('attack', 'False')

    def information(self, e):
        '''Информация о сервисах'''
        def close_info(e):
            self.page.dialog.open = False
            self.page.update()

        services_count = len(urls("12345"))
        feedback_count = len(feedback_urls("12345"))
        info_text = f'''Сервисов - {services_count}\nRU - {sum(1 for i in urls("12345") if i["info"]["country"] == "RU")}\nФидбек Сервисов - {feedback_count}'''

        info_dialog = AlertDialog(
            title=Text(f'OUTSIDE V{VERSION}', text_align='center', size=40, color=self.color, font_family='Consolas'),
            content=Text(info_text, text_align='center', size=17, font_family='Consolas'),
            actions=[TextButton('ОКЕЙ', width=110, height=50, on_click=close_info, style=ButtonStyle(color=self.color))],
            actions_alignment='end'
        )
        self.page.dialog = info_dialog
        info_dialog.open = True
        self.page.update()


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
