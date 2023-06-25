from importlib import reload
import bot
from vk_api import VkUpload
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from datetime import datetime, timedelta
from docs import docWriter
from multiprocessing import Process

import vk_parsing, weather, json, requests, nltk, pika, uuid
from plugins import config, system, function, gaming_func, templates, SpyGame, keyboards

from importlib import reload
# импорты из дб
from plugins.db import init_db
init_db()

from bot import VkBot

def sender(peer_id, message, attachment=None,keyboard=None, template=None):
    vk.messages.send(
        peer_id=peer_id,
        message=message,
        attachment=attachment,
        random_id=get_random_id(),
        keyboard=keyboard,
        template=template
    )

bot = VkBot()
vk, longpoll, longpollGroup = system.session()
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        sender(bot.USER_ID, bot.get_command(event.object.message['text'].lower()))

print('Test is ready')
