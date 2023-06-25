import vk
import vk_api
from plugins.config import access_token
import json

session = vk.Session(access_token=access_token)
vkapi = vk.API(session)
vk = vk_api.VkApi(token=access_token)
owner_id = -198776140
quotationskubsu_id = -114875319

wall_posts = vkapi.wall.get(owner_id=owner_id, count = 24, v = 5.95)

def quots(count):
    quotations = vkapi.wall.get(owner_id=-114875319, count=count, v=5.95)
    for quots in quotations['items']:
        post = quots
    return post

def getUser(peer_id):
    user = vkapi.users.get(user_ids=peer_id, v = 5.131, lang=0, fields="photo_200")
    return user

def getUsername(peer_id):
    user = getUser(peer_id)
    username = user[0]['first_name'] + ' ' + user[0]['last_name']
    return username

def last_post(count: int):
    wall_posts = vkapi.wall.get(owner_id=owner_id, count=count, v=5.95)
    for ids in wall_posts['items']:
        return ids['id']
    #return wall_posts

def getNews(message):
    wall = ''
    text = "Последняя запись"
    if message == 'осо':
        group = -61559790
        text+=" ОСО"
    if message == 'профком':
        group = -940543
        text += " Профкома"
    if message == 'студ':
        group = -198776140
        text += " Студа"
    if message == 'профбюро':
        group = -91150385
        text += " Профбюро"
    if message == 'ксн':
        group = -171487716
        text += " КСН"
    if message == 'сно':
        group = -89992372
        text += " СНО"
    wall = -group
    flag = 0
    post = vkapi.wall.get(owner_id=group, count=2, v=5.95)

    for ids in post['items']:
        try:
            if ids['is_pinned'] == 1:
                flag = 1
        except:
            pass
    for ids in post['items']:
        if flag == 1:
            post = ids['id']
        else:
            return ids['id'], wall, text
    return post, wall, text

def getUploadUrl(group_id):
    return vkapi.docs.getUploadServer(group_id=group_id)