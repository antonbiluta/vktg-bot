import datetime
import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random  # генератор случайных чисел
import schedule  # выполнение отложенных задач
import time  # работа с датой и временем (используется только для логов)

from server import Server
from plugins import function, weather
from plugins.config import token, group_id


class ScheduledBot(Server):
    """
    Бот по расписанию
    """


    def __init__(self):

        super().__init__(token, group_id, "Mentor.Online")

        self.create_schedule()
        self.today()
        while True:
            schedule.run_pending()

    def today(self):
        status = weather.getStatus()
        speed = weather.getSpeed()
        humidity = weather.getHumidity()
        temperature = weather.getTemp()
        rain = weather.getRain()

        current_datetime = datetime.datetime.now().date()
        time = datetime.datetime.now().strftime("%H:%M") # "%H:%M:%S"
        week = datetime.date(2021, 12, 20).strftime("%V")
        if int(week)%2 != 0:
            week = 'Четная'
        else:
            week = 'Нечетная'

        rasp = function.getNews()

        last_news = '\n'.join(
             [f'{str(title)}\n\n{str(text)}\n\n{str(footer)}\n{str(comments)}' for
             title, text, footer, comments in rasp])
        date = datetime.datetime.now().strftime("%d/%m/%Y")
        message = f'📅 Дата: {date}' \
               f'\n⏰ Время: {time}' \
               f'\n⌛ Неделя: {week}'
        if last_news:
            message = message + f'\n━━━━━━━━━━━━━━━━' \
                                f'\n📰 Последние новости' \
                                f'\n━━━━━━━━━━━━━━━━' \
                                f'\n{last_news}'
        message = message + f'\n━━━━━━━━━━━━━━━━' \
                            f'\n🌞 Погода в Краснодаре.' \
                            f'\n━━━━━━━━━━━━━━━━' \
                            f'\n☀ Статус: {status}' \
                            f'\n💨 Скорость ветра: {speed}м/c' \
                            f'\n💧 Влажность воздуха: {humidity}%' \
                            f'\n🌡️ Температура: {temperature}°С'
        try:
            arrayUser = function.getListUser('news')
            for id in arrayUser:
                self.sender(id, message)
        except:
            pass

    def news(self):
        message = 'Вы получили это сообщение, т.к. подписаны на рассылку.'
        try:
            arrayUser = function.getListUser('news')
            for id in arrayUser:
                self.sender(id, message)
        except:
            pass


    def wish_good_morning(self):
        """
        Отправка случайного пожелания доброго утра
        Сообщение будет отправлено пользователю с default_user_id (можно изменить при вызове функци отправки сообщения)
        """
        message = 'Вы получили это сообщение, т.к. подписаны на рассылку.'
        try:
            arrayUser = function.getListUser('news')
            for id in arrayUser:
                self.sender(id, message)
        except:
            pass

    def talk_about_lunch(self):
        """
        Отправка случайного сообщения про обед
        Сообщение будет отправлено пользователю с default_user_id (можно изменить при вызове функци отправки сообщения)
        """
        pet_name = self.pet_names[random.randint(0, len(self.pet_names) - 1)]
        phrases = [
            "угадай, чем я сегодня обедала, {}".format(pet_name),
            "приятного аппетита, {}!".format(pet_name),
            "а что ты любишь кушать, {}?".format(pet_name),
            "Что ты ел сегодня, {}?".format(pet_name),
        ]
        message = phrases[random.randint(0, len(phrases) - 1)]
        self.send_message(message_text=message)

    def ask_how_the_day_was(self):
        """
        Отправка случайного вопроса про то, как у собеседника идут дела
        Сообщение будет отправлено пользователю с default_user_id (можно изменить при вызове функци отправки сообщения)
        """
        pet_name = self.pet_names[random.randint(0, len(self.pet_names) - 1)]
        phrases = [
            "как твой день проходит, {}?".format(pet_name),
            "чем занимался сегодня, {}?".format(pet_name),
            "Признавайся, что делал весь день, {}?".format(pet_name),
            "чего успел натворить за сегодня, {}?".format(pet_name)
        ]
        message = phrases[random.randint(0, len(phrases) - 1)]
        self.send_message(message_text=message)

    def wish_good_night(self):
        """
        Отправка случайного пожелания на ночь
        Сообщение будет отправлено пользователю с default_user_id (можно изменить при вызове функци отправки сообщения)
        """
        pet_name = self.pet_names[random.randint(0, len(self.pet_names) - 1)]
        phrases = [
            "Доброй ночи, {}!".format(pet_name),
            "Сладких снов, {})".format(pet_name),
            "спи крепко, {}".format(pet_name),
            "спокнойно ночи тебе, {}, завтра продолжим".format(pet_name)
        ]
        message = phrases[random.randint(0, len(phrases) - 1)]
        self.send_message(message_text=message)

    def create_schedule(self):
        """
        Создание расписания отправки сообщений со случайным временем в заданном промежутке
        Используется время сервера
        Документация библиотеки schedule: https://schedule.readthedocs.io/en/stable/index.html
        """

        news = "10:00"
        schedule.every().day.at(news).do(self.news)

        # отправка сообщения в обеденное время в случайный момент
        lunch_time = str(random.randint(11, 13)) + ":" + str(random.randint(10, 59))
        schedule.every().day.at(lunch_time).do(self.talk_about_lunch)

        # отправка сообщения в вечернее время в случайный момент
        evening_time = str(random.randint(18, 20)) + ":" + str(random.randint(10, 59))
        schedule.every().day.at(evening_time).do(self.ask_how_the_day_was)

        # отправка сообщения поздним вечером в случайный момент
        night_time = str(random.randint(22, 23)) + ":" + str(random.randint(10, 59))
        schedule.every().day.at(night_time).do(self.wish_good_night)

        # перезапуск формирования случайного расписания ровно в полночь
        schedule.every().day.at("00:00").do(self.restart_schedule)

        # вывод созданного расписания
        print(f"Расписание на {time.strftime('%d.%m.%Y')}:"
              f"\n{news}\n{lunch_time}\n{evening_time}\n{night_time}\n")

    def restart_schedule(self):
        """
        Перезапуск расписания для обновления случайного времени отправки сообщений
        """
        schedule.clear()
        self.create_schedule()