from server import Server
from scheduleBot import ScheduledBot
from plugins.config import token, group_id

server = Server(token, group_id, "Mentor.Online")

def start():
    try:
        server.start()
    except Exception as e:
        print(e)
        print('Произошла ошибка!')
        start()

if __name__ == '__main__':
    start()

scheduleBot = ScheduledBot()