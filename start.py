import bot
import time
if __name__ == '__main__':
    try:
        bot.start()
    except:
        time.sleep(60)
        print('Попытка восстановить соединение')
