import vk
from plugins.config import access_token
import json
import bot

session = vk.Session(access_token=access_token)
vkapi = vk.API(session)
owner_id = -198776140
quotationskubsu_id = -114875319

wall_posts = vkapi.wall.get(owner_id=owner_id, count = 24, v = 5.95)

def info():
    last_like = vkapi.wall.get(owner_id=owner_id, v=5.95, count=3)
    for ids in last_like['items']:
        post_id= ids['id']
        try:
            last_comment = vkapi.wall.getComments(owner_id=owner_id, post_id=post_id, v=5.95)
            for ids in last_comment['items']:
                id_person = ids['from_id']
                text_person = ids['text']
                bot.sender(id_person,'Спасибо за комментарий')
                bot.sender(2000000001, f'Пользователь @id{id_person} оставил комментарий под последним постом: {text_person}')
        except:
            pass
        last_repost = vkapi.wall.getReposts(owner_id=owner_id, post_id=post_id, v=5.95)

def quots(count):
    quotations = vkapi.wall.get(owner_id=-114875319, count=count, v=5.95)
    for quots in quotations['items']:
        post = quots
    return post

def getUser(peer_id):
    user = vkapi.users.get(user_ids=peer_id, v = 5.95, lang=0)
    return user



def last_post(count: int):
    wall_posts = vkapi.wall.get(owner_id=owner_id, count=count, v=5.95)
    for ids in wall_posts['items']:
        return ids['id']
    #return wall_posts
