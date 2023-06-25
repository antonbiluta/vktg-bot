import vk_api
from plugins.config import token, group_id, access_token
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.longpoll import VkEventType, VkLongPoll

def session():
    try:
        vk_session = vk_api.VkApi(token=token)
        vk = vk_session.get_api()
        longpoll = VkBotLongPoll(vk_session, group_id)
        longpollGroup = VkLongPoll(vk_session)
        return vk, longpoll, longpollGroup
    except:
        pass


