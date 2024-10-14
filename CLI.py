import argparse
from time import sleep
from random import choice

from Core.Config import check_config, change_config
from Core.Run import start_async_attacks
from Core.Attack.Services import urls
from Core.Attack.Feedback_Services import feedback_urls
from Core.TBanner import banner


class OutsideBomberCLI:
    def __init__(self):
        self.color = check_config()['color']

    def start_attack(self, number, rounds, attack_type, feedback):
        """Запуск атаки через CLI"""
        if check_config()['attack'] == 'True':
            print("Слишком много атак. Подождите!")
            return

        print(f"\nЗапуск атаки на номер: {number}")
        print(f"Тип атаки: {attack_type}")
        print(f"Круги: {rounds}")
        print(f"Сервисы обратной связи: {'Включены' if feedback else 'Отключены'}\n")
        print("Атака началась...\n")

        # Обновляем конфиг для атаки
        change_config('attack', 'True')
        change_config('type_attack', attack_type)
        change_config('feedback', str(feedback))

        # Запуск асинхронной атаки
        start_async_attacks(number, rounds)

        # Завершение атаки
        change_config('attack', 'False')
        print("Атака завершена!\n")

    def information(self):
        """Информация о сервисах"""
        services_count = len(urls("12345"))
        feedback_count = len(feedback_urls("12345"))

        print(f"\nВсего сервисов: {services_count}")
        print(f"Сервисов в России: {sum(1 for i in urls('12345') if i['info']['country'] == 'RU')}")
        print(f"Сервисов обратной связи: {feedback_count}\n")


def main():
    # Создание CLI интерфейса
    parser = argparse.ArgumentParser(description="OUTSIDE Bomber CLI")

    parser.add_argument("-n", "--number", type=str, required=True,
                        help="Номер телефона без знака '+'")
    parser.add_argument("-r", "--rounds", type=int, default=1,
                        help="Количество кругов (по умолчанию 1)")
    parser.add_argument("-t", "--type", type=str, choices=["MIX", "SMS", "CALL"], default="MIX",
                        help="Тип атаки (MIX, SMS, CALL)")
    parser.add_argument("-f", "--feedback", action="store_true",
                        help="Использовать сервисы обратной связи")
    parser.add_argument("-i", "--info", action="store_true",
                        help="Показать информацию о сервисах")

    args = parser.parse_args()

    bomber = OutsideBomberCLI()

    if args.info:
        bomber.information()
    else:
        bomber.start_attack(args.number, args.rounds, args.type, args.feedback)


if __name__ == "__main__":
    main()
