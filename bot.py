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

def importOrReload(module_name, *names):
    import sys

    if module_name in sys.modules:
        reload(sys.modules[module_name])
    else:
        __import__(module_name, fromlist=names)
    for name in names:
        globals()[name] = getattr(sys.modules[module_name], name)

importOrReload("plugins", "languages")


vk, longpoll, longpollGroup = system.session()

# text = register(event.obj.from_id)

def vkup(image):
    upload = VkUpload(vk)
    upload_image = upload.photo_messages(photos=image)[0]
    return upload_image

def sender(peer_id, message, attachment=None,keyboard=None, template=None):
    vk.messages.send(
        peer_id=peer_id,
        message=message,
        attachment=attachment,
        random_id=get_random_id(),
        keyboard=keyboard,
        template=template
    )


def filter_text(text):
    text = [c for c in text if c in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя- /abcdefghijklmnopqrstuvwxyz']
    text = ''.join(text)
    return text


class RpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection()
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body.decode()

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='VK_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(n))
        while self.response is None:
            self.connection.process_data_events()

        from urllib.parse import unquote
        answer = str(self.response)
        return answer

    def callReportTG(self, n):
        self.channel.exchange_declare(exchange='vk_report', exchange_type='fanout')
        self.channel.basic_publish(
            exchange='vk_report',
            routing_key='',
            body=str(n)
        )
        return str('Спасибо за репорт. В скором времени администратор рассмотрит вашу проблему.')


class User:
    def __init__(self, id, mode):
        self.id = id
        self.mode = mode


users = []


def change_lang(lang, peer_id, conversation):
    # Тут функция для изменения в базе данных
    function.setLang(user_id=peer_id,lang=lang)
    arrLang = languages.arrLang[f'{lang}']

    last_id = vk.messages.edit(
        peer_id=peer_id,
        message=(arrLang['settings-save'] if function.checkAgree(user_id=peer_id) else arrLang['conf-choose-lang']),
        conversation_message_id=conversation,
        keyboard=(keyboards.new_start(lang).get_keyboard() if function.checkAgree(user_id=peer_id) else keyboards.agreement(lang).get_keyboard())
    )








def bot():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            from_id = event.object.message['from_id']  # id пользователя, который отправил сообщение
            peer_id = event.object.message['peer_id']  # peer_id беседы или ЛС, откуда пришло сообщение
            message = event.object.message['text'].lower()
            msg = event.object.message['text']
            start_msg = message

            if message=='!reload':
                importOrReload("plugins", "languages")

            # Если сообщение поступило
            # if message == '!start':
            if start_msg in config.hello_msg:
                base = vk_parsing.getUser(from_id)
                fullname = base[0]['first_name'] + ' ' + base[0]['last_name']
                status, situation = function.checkUser(peer_id, fullname)
                if status:
                    lang = function.checkLang(user_id=peer_id)
                    arrLang = languages.arrLang[lang]
                    if situation == 1: # Новый
                        kbrd_lang = keyboards.lang()
                        sender(peer_id, arrLang['choose-lang'], keyboard=kbrd_lang.get_keyboard())
                    elif situation == 2: # Бывалый
                        kbrd = keyboards.main_menu(lang)
                        sender(peer_id, arrLang['main-menu-info'], keyboard=kbrd.get_keyboard())



                # Если беседа
                if function.checkGroup(peer_id=peer_id):
                    # if function.checkReg(peer_id=peer_id):
                    #     lang = function.checkLang(user_id=from_id)
                    #     arrLangLang = arrLang[lang]
                    #     sender(peer_id, arrLangLang['sorry-allchat'])
                    # else:
                    #     lang = 'en-GB'
                    #     arrLangLang = arrLang[lang]
                    #     sender(peer_id, arrLangLang['sorry-allchat'])
                    pass



            if message == 'пупипупи':
                sender(peer_id, 'ПУПИПИДУП ПУП ПУП ПИДУП ПУП ПУПУП ПУУУУУУПИПУПИ 🤪🤪🤪')

            from plugins import profiledb
            base = vk_parsing.getUser(from_id)
            fullname = base[0]['first_name'] + ' ' + base[0]['last_name']
            photo = base[0]['photo_200']
            if message in ['!reg', '!рег']:
                if profiledb.checkUser(uid=from_id) == False:

                    if profiledb.register(uid=from_id, name=fullname, status='Ожидается'):
                        sender(peer_id, 'Успешная регистрация')
                else:
                    sender(peer_id, 'Вы уже зарегистрированы')

            if message.partition(' ') in ['!edit']:
                if profiledb.editName(uid=from_id, name=fullname):
                    sender(peer_id, 'имя успешно изменено')
                if profiledb.editPhoto(uid=from_id, photo=photo):
                    sender(peer_id, 'фото успешно обновлено')
            if message in ['test']:
                profiledb.getData(uid=from_id)


            if message in ['!profile', '!профиль']:
                from plugins import profiledb
                if profiledb.checkUser(uid=from_id):
                    import generateProfile

                    data = profiledb.getData(uid=from_id)

                    sender(peer_id, 'Пожалуйста, подождите')

                    if (generateProfile.create_image(data=data)):
                        image = "F:/Dev/Python/Projects/VKbot/data/profile.jpg"
                        upload = VkUpload(vk)
                        upload_image = upload.photo_messages(photos=image)[0]
                        att = []
                        att.append('photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))
                        sender(peer_id=peer_id, message="", attachment=','.join(att))
                else:
                    sender(peer_id, 'Вы не зарегистрированы')

        elif event.type == VkBotEventType.MESSAGE_EVENT:

            lang = function.checkLang(user_id=event.obj.peer_id)
            back = ''
            try:
                back = event.object.payload.get('back-menu')
                arrLang = languages.arrLang[lang]
            except:
                arrLang = languages.arrLang['en-GB']

            CALLBACK_TYPES = ('show_snackbar', 'open_link', 'open_app')
            f_toggle: bool = False

            if event.object.payload.get('type') in CALLBACK_TYPES:
                r = vk.messages.sendMessageEventAnswer(
                    event_id=event.object.event_id,
                    user_id=event.object.user_id,
                    peer_id=event.object.peer_id,
                    event_data=json.dumps(event.object.payload))

            elif event.object.payload.get('type') in ['lang_rus', 'lang_eng','lang_it','lang_am', 'lang_kz']:
                lang_choose = event.object.payload.get('type')
                lang = 'en-GB'
                if lang_choose == 'lang_rus':
                    lang = 'ru-RU'
                elif lang_choose == 'lang_it':
                    lang = 'it-IT'
                elif lang_choose == 'lang_am':
                    lang = 'hy-AM'
                elif lang_choose == 'lang_kz':
                    lang = 'kk-KZ'
                    sender(event.obj.peer_id, '«...Я просто совру, сказал что здесь был выбор...»')
                elif lang_choose == 'lang_ua':
                    lang = 'uk-UA'
                change_lang(lang, event.obj.peer_id, event.obj.conversation_message_id)

            elif event.object.payload.get('type') in ['agr_yes', 'agr_no']:
                if event.object.payload.get('type') == 'agr_yes':
                    new_start = keyboards.new_start(lang)
                    function.setAgree(user_id=event.obj.peer_id, status=1)
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=arrLang['accept-agreement'],
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=new_start.get_keyboard())

                elif event.object.payload.get('type') == 'agr_no':
                    function.setAgree(user_id=event.obj.peer_id, status=0)
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=arrLang['deny-agreement'],
                        conversation_message_id=event.obj.conversation_message_id)

            # Обработчик главного меню
            elif event.object.payload.get('type') == 'main-menu_list':
                main_menu = keyboards.main_menu(lang)
                last_id = vk.messages.edit(
                    peer_id=event.obj.peer_id,
                    message=arrLang['main-menu-info'],
                    conversation_message_id=event.obj.conversation_message_id,
                    keyboard=main_menu.get_keyboard())

            elif event.object.payload.get('type') in ['app-menu', 'blanks', 'wifi']:
                arrLang = arrLang['app-menu']
                if event.object.payload.get('type') == 'app-menu':
                    menu_app = keyboards.app(lang, 'main-menu_list')
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=arrLang['info'],
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=menu_app.get_keyboard()
                    )

                elif event.object.payload.get('type') == 'blanks':
                    backKbr = keyboards.backKbr(lang, 'app-menu')
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=arrLang['blanks'],
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=backKbr.get_keyboard()
                    )
                elif event.object.payload.get('type') == 'wifi':
                    backKbr = keyboards.backKbr(lang, 'app-menu')
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=arrLang['wifi'],
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=backKbr.get_keyboard()
                    )
            # Обработчик меню Вуза
            elif event.object.payload.get('type') in ['university', 'info-kubsu', 'input-kubsu', 'univ-live', 'spam', 'univ-live-struct', 'univ-live-clubs']:
                arrLang = arrLang['univ-menu']
                if event.object.payload.get('type') == 'university':
                    menu_univ = keyboards.univ(lang, 'main-menu_list')
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=arrLang['start'],
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=menu_univ.get_keyboard()
                    )

                # Меню Вуза
                elif event.object.payload.get('type') == 'info-kubsu':
                    kbrd = keyboards.backKbr(lang, 'university')
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=arrLang['info'],
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=kbrd.get_keyboard()
                    )
                elif event.object.payload.get('type') == 'input-kubsu':
                    kbrd = keyboards.inputkubsu(lang, 'university')
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=arrLang['input'],
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=kbrd.get_keyboard()
                    )
                elif event.object.payload.get('type') == 'univ-live':
                    univLife_menu = keyboards.univLife(lang, 'university')
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=arrLang['life']['info'],
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=univLife_menu.get_keyboard()
                    )
                elif event.object.payload.get('type') == 'spam':
                    kbrd = keyboards.backKbr(lang, 'university')
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=arrLang['spam'],
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=kbrd.get_keyboard()
                    )

                # Меню Унив. Жизни
                elif event.object.payload.get('type') == 'univ-live-news':
                    back = keyboards.backKbr(lang, 'univ-live')
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=arrLang['life']['news'],
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=back.get_keyboard()
                    )
                elif event.object.payload.get('type') == 'univ-live-plans':
                    back = keyboards.backKbr(lang, 'univ-live')
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=arrLang['life']['mer'],
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=back.get_keyboard()
                    )
                elif event.object.payload.get('type') == 'univ-live-struct':
                    back = keyboards.backKbr(lang, 'univ-live')
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=arrLang['life']['struct'],
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=back.get_keyboard()
                    )
                elif event.object.payload.get('type') == 'univ-live-clubs':
                    back = keyboards.clubsMenu(lang, 'univ-live')
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=arrLang['life']['clubs']['info'],
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=back.get_keyboard()
                    )
                elif event.object.payload.get('type') == 'univ-life-opportunities':
                    back = keyboards.backKbr(lang, 'univ-live')
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=arrLang['life']['opportunities'],
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=back.get_keyboard()
                    )
                elif event.object.payload.get('type') == 'univ-life-museum':
                    back = keyboards.backKbr(lang, 'univ-live')
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=arrLang['life']['museum'],
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=back.get_keyboard()
                    )

            # Обработчик клубов
            elif event.object.payload.get('type') in ['presscenter','imperial', 'greencubik', 'gamedesign', 'patriotvosp', 'debatclub', 'clubnastav', 'studotryad', 'nackult']:
                type = event.object.payload.get('type')
                arrLang = arrLang['univ-menu']['life']['clubs']
                back = keyboards.backKbr(lang, 'univ-live-clubs')

                last_id = vk.messages.edit(
                    peer_id=event.obj.peer_id,
                    message=arrLang[type],
                    conversation_message_id=event.obj.conversation_message_id,
                    keyboard=back.get_keyboard()
                )

            # Обработчик общего меню факультетов
            elif event.object.payload.get('type') in ['faculties', 'fac1', 'fac2', 'fac3', 'fac4']:
                if event.object.payload.get('type') == 'faculties':
                    kbrd = keyboards.facults_menu(lang, 'main-menu_list')
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=arrLang['faculties-info'],
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=kbrd.get_keyboard()
                    )
                elif event.object.payload.get('type') == 'fac1':
                        kbrd = keyboards.facults_menu1(lang, 'main-menu_list')
                        last_id = vk.messages.edit(
                            peer_id=event.obj.peer_id,
                            message='Page: 1',
                            conversation_message_id=event.obj.conversation_message_id,
                            keyboard=kbrd.get_keyboard()
                        )
                elif event.object.payload.get('type') == 'fac2':
                    kbrd = keyboards.facults_menu2(lang, 'main-menu_list')
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message='Page: 2',
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=kbrd.get_keyboard()
                    )
                elif event.object.payload.get('type') == 'fac3':
                    kbrd = keyboards.facults_menu3(lang, 'main-menu_list')
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message='Page: 3',
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=kbrd.get_keyboard()
                    )
                elif event.object.payload.get('type') == 'fac4':
                    kbrd = keyboards.facults_menu4(lang, 'main-menu_list')
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message='Page: 4',
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=kbrd.get_keyboard()
                    )

            elif event.object.payload.get('type') in ['biofacult', 'iggts', 'fad', 'jurfuck', 'fismo', 'fktpm', 'matfak', 'fppk', 'rgf', 'fup', 'fhivt', 'ftf', 'filfac', 'hudgraf', 'econom', 'urfak', 'inspo']:

                kbrd = keyboards.fac_menu(lang, 'main-menu_list', event.obj.payload.get('type'))
                last_id = vk.messages.edit(
                    peer_id=event.obj.peer_id,
                    message=arrLang['faculties-info'],
                    conversation_message_id=event.obj.conversation_message_id,
                    keyboard=kbrd.get_keyboard()
                )

            elif event.object.payload.get('type') == 'fac':
                button = event.object.payload.get('button')
                fac = event.object.payload.get('fac')
                arrFac = languages.faculties[fac]
                kbrd = keyboards.backKbr(lang, fac)
                info = json.loads(function.getFacInfo(fac))
                info = info[lang][0][button]
                last_id = vk.messages.edit(
                    peer_id=event.obj.peer_id,
                    message=info,
                    conversation_message_id=event.obj.conversation_message_id,
                    keyboard=kbrd.get_keyboard()
                )
            # Обработчик меню навигации
            elif event.object.payload.get('type') in ['menu-nav', '1-nav', '2-nav', '3-nav', '4-nav']:
                if event.object.payload.get('type') == 'menu-nav':
                    menu_nav = keyboards.nav_menu(lang, back)
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=arrLang['navigation-menu-info'],
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=menu_nav.get_keyboard()
                    )

            # Обработчик меню настроек
            elif event.object.payload.get('type') in ['settings-menu', 'set-change_lang', 'other-lang', 'about-app']:
                if event.object.payload.get('type') == 'settings-menu':
                    settings_kbrd = keyboards.setting_menu(lang, 'main-menu_list')
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=arrLang['settings-menu-info'],
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=settings_kbrd.get_keyboard()
                    )
                    # sender(event.obj.peer_id, arrLang['settings-menu-info'], keyboard=settings_kbrd.get_keyboard())

                elif event.object.payload.get('type') == 'set-change_lang':
                    kbrd_lang = keyboards.lang()
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=arrLang['choose-lang'],
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=kbrd_lang.get_keyboard()
                    )
                elif event.object.payload.get('type') == 'other-lang':
                    other_lang = keyboards.other_lang()
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=arrLang['choose-lang'],
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=other_lang.get_keyboard()
                    )

                elif event.object.payload.get('type') == 'about-app':
                    kbrd = keyboards.backKbr(lang, back)
                    last_id = vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=arrLang['about-app'],
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=kbrd.get_keyboard()
                    )

            elif event.object.payload.get('type') == 'panorama':
                kbrd = keyboards.backKbr(lang, 'main-menu_list')
                last_id = vk.messages.edit(
                    peer_id=event.obj.peer_id,
                    message='Кто же нас создал?!'
                            '\nНикто не знает.'
                            '\nМы самый главный секрет человечества...'
                            '\n\nСоздатель: [id1|Павел Дуров]'
                            '\nМы в ВК: [panorama_kubsu|ИА «Панорама КубГУ»]',
                    conversation_message_id=event.obj.conversation_message_id,
                    keyboard=kbrd.get_keyboard()
                )
            print(event.obj.payload)


















def loop_a():
    def getName():
        # Получаем имена
        try:
            request = vk.messages.getConversationsById(peer_ids=peer_id)
            for response in request['items']:
                chat_settings = response['chat_settings']
                title = chat_settings['title']
            base = vk_parsing.getUser(from_id)
            fullname = base[0]['first_name'] + ' ' + base[0]['last_name']

            group_podgroup = title.partition(' ')[0]
            group = group_podgroup.partition('/')[0]
            podgroup = group_podgroup[group_podgroup.find("/") + 1:]
            if podgroup == '':
                podgroup = None
        except:
            base = vk_parsing.getUser(from_id)
            fullname = base[0]['first_name'] + ' ' + base[0]['last_name']
            group = 0
            podgroup = 0
            group_podgroup = 0
            title = fullname
        return [group_podgroup, fullname, group, podgroup, title]
    try:
        user = 0
        chat = 0
        new_status = ''
        for event in longpoll.listen():
            #Если сообщение
            if event.type == VkBotEventType.MESSAGE_NEW:

                from_id = event.object.message['from_id']  # id пользователя, который отправил сообщение
                peer_id = event.object.message['peer_id']  # peer_id беседы или ЛС, откуда пришло сообщение

                [group_podgroup, fullname, group, podgroup, title] = getName()

                message = event.object.message['text'].lower()
                Message = event.object.message['text']

                # if message.partition(' ')[0] == 'бот':
                #     num = message[message.find(' ')+1:]
                #     rpc = RpcClient()
                #     try:
                #         sender(peer_id, rpc.call(num))
                #     except:
                #         print(rpc.call(num))

                function.checkName(peer_id=peer_id, title=title)

                #Если бота добавили или кого-то в беседу
                try:
                    action = event.object.message['action']
                    for x in action:
                        if x == 'type':
                            action_new = action[x]
                    if action_new == 'chat_invite_user':
                        if function.checkReg(peer_id=peer_id) == False:
                            keyboard = VkKeyboard(inline=True)
                            keyboard.add_callback_button(label='Зарегистрировать группу', color=VkKeyboardColor.POSITIVE,
                                                         payload={"type": "my_own_100500_type_edit"})
                            test = keyboard.get_keyboard()
                            text = '📝 Для активации всех функций бота дайте ему администратора, после чего введите "/reg" или нажмите на кнопку "зарегистрировать группу".' \
                                   '\n📜 Для справки введите "/help".'
                            sender(peer_id=peer_id, message=text, keyboard=test)
                except:
                     pass


                #SuperAdmin
                if function.check_adm(peer_id=from_id, lvl=1000) == True:

                    if message.partition(' ')[0] == 'delete':

                        num = message[7:]
                        msg = vk.messages.getHistory(count=int(num), peer_id=peer_id)
                        for x in msg['items']:
                            id=x['id']
                            vk.messages.delete(delete_for_all=1, message_ids=id)
                        #id_list = []
                        #id = event.object.message['id']
                        #id_list.append(str(id))
                        #for i in range(int(num)-1):
                            #id_list.append(str(id-1))
                        #ids = ','.join(id_list)
                        #vk.messages.delete(delete_for_all=1, message_ids=ids)

                    if message in ['осо', 'профком', 'студ', 'профбюро', 'ксн', 'сно']:
                        news, wals, text = vk_parsing.getNews(message)
                        attach = []
                        attach.append('wall-{}_{}'.format(wals, news))
                        sender(peer_id=peer_id, message=text, attachment=attach)

                #Admin
                if function.check_adm(peer_id=peer_id, lvl=100) == True:

                    if message == '/admin':
                        vk.messages.send(
                            keyboard=admin_board.get_keyboard(),
                            key=(''),  # ВСТАВИТЬ ПАРАМЕТРЫ
                            server=(''),
                            ts=(''),
                            random_id=get_random_id(),
                            message='Добро пожаловать в админ панель.',
                            peer_id=peer_id
                        )

                    if '/send' in Message:
                        text = Message[6:]
                        if text[:5] == 'group':
                            perm = function.getMassiv(char='>')
                            text = text[6:]
                        elif text[:6] == 'people':
                            perm = function.getMassiv(char='<')
                            text = text[7:]
                        else:
                            char1 = '['
                            char2 = ']'
                            save = Message
                            id = Message[Message.find(char1) + 1: Message.find(char2)]
                            group = id.split(', ')
                            perm = group
                            text = save[save.find(char2)+2:]

                        carousel = templates.comp()
                        for x in perm:
                            vk.messages.send(
                                peer_id=x,
                                random_id=get_random_id(),
                                message='Не забывай, что у твоего любимого факультета есть группы, на которые стоит подписаться!',
                                template=carousel
                            )

                    if '/add' in Message:
                        text = Message[5:]
                        char1 = '['
                        char2 = ']'
                        save = Message
                        id = Message[Message.find(char1) + 1: Message.find(char2)]
                        group = id.split(', ')
                        perm = group
                        money = save[save.find(char2) + 2:]
                        for x in perm:
                            gaming_func.addBalance(peer_id=x, balance_new=int(money))
                            text = f'На ваш счёт была добавлена сумма в размере {money} sc'
                            sender(x, text)

                    if 'наградить' in message:
                        text = message[13:]
                        import re
                        re.split(' ', text)
                        print(text)

                    if '/msg' in Message:
                        text = Message[5:]
                        if text[:5] == 'group':
                            perm = function.getMassiv(char='>')
                            text = text[6:]
                        elif text[:6] == 'people':
                            perm = function.getMassiv(char='<')
                            text = text[7:]
                        elif text[:3] == 'all':
                            perm = function.getMassiv()
                            text = text[4:]
                        else:
                            char1 = '['
                            char2 = ']'
                            save = Message
                            id = Message[Message.find(char1) + 1: Message.find(char2)]
                            group = id.split(', ')
                            perm = group
                            text = save[save.find(char2) + 2:]

                        attach = event.object.message['attachments']
                        attachments = []
                        lol = ''
                        for block in attach:
                            att_type = block['type']
                            block_t = block[att_type]
                            try:
                                try:
                                    attachments.append('{}{}_{}_{}'.format(block['type'], block_t['owner_id'], block_t['id'], block_t['access_key']))
                                except:
                                    attachments.append(
                                        '{}{}_{}'.format(block['type'], block_t['owner_id'], block_t['id']))
                            except:
                                pass
                            lol = ','.join(attachments)
                        for x in perm:
                            try:
                                sender(peer_id=x, attachment=lol, message=text)
                            except:
                                sender(2000000009, f'Пользователь @id{x} не разрешил отправку сообщений')

                    if message in ['/ids']:
                        ids = function.getIds()

                        text = '\n'.join(
                            [f'{str(uid)} ⇨ {str(uname)}' for uid, uname in ids])

                        sender(peer_id, text)

                    if message == 'тест':
                        keyboard = VkKeyboard(inline=True)
                        keyboard.add_callback_button(label='Зарегистрировать группу', color=VkKeyboardColor.PRIMARY,
                                                        payload={"type": "my_own_100500_type_edit"})
                        test = keyboard.get_keyboard()
                        text = '📝 Для активации всех функций бота дайте ему администратора и введите "/reg".' \
                                '\n📜 Для справки введите "/help".'
                        vk.messages.send(
                            peer_id=peer_id,
                            random_id=get_random_id(),
                            message=text,
                            keyboard=test
                        )

                    if message == 'тест2':
                        keyboard = VkKeyboard(inline=True)
                        keyboard.add_callback_button(label='Покажи pop-up сообщение', color=VkKeyboardColor.SECONDARY,
                                                        payload={"type": "show_snackbar",
                                                                "text": "Это исчезающее сообщение"})
                        test = keyboard.get_keyboard()
                        text = 'Всплывашка'
                        vk.messages.send(
                            peer_id=peer_id,
                            random_id=get_random_id(),
                            message=text,
                            keyboard=test
                        ),

                #Зареганым пользователям
                if message.partition(' ')[0] in ['баланс', 'профиль', 'магазин', 'награждение', 'студкоин', 'студкоины', '/статус']:
                    if function.check_adm(peer_id=from_id, lvl=0) == True:
                        #Личные данные
                        if message.partition(' ')[0] in ['баланс', 'профиль']:
                            if message == 'баланс':
                                try:
                                    balance = gaming_func.check_balance(peer_id=from_id)
                                    ruble = float(balance) * 0.25
                                    sender(peer_id, f'💳 Cчет: {balance} СтудКоинов'
                                                    f'\n\n💰 1 СтудКоин = 0.25 ₽'
                                                    f'\n💱 Баланс {ruble} ₽')
                                except:
                                    sender(2000000009, f'Ошибка в "Баланс" вызвана @id{from_id}')

                            if message.partition(' ')[0] == 'профиль':
                                not_cmd = message[message.find(" ") + 1:]
                                who = message[message.find(" ") + 1:]
                                who_id = 0
                                name = ''
                                if message.partition(' ')[0] != who:
                                    try:
                                        import re

                                        whoId0 = who
                                        whoId1 = whoId0.split('|')[0]
                                        who_id = re.findall(r'id(.*)', whoId1)[0]
                                    except:
                                        msg_to = who
                                else:
                                    who_id = from_id

                                base = vk_parsing.getUser(who_id)
                                name = base[0]['first_name'] + ' ' + base[0]['last_name']

                                invList = gaming_func.getInv(peer_id=who_id)
                                [skills] = gaming_func.getSkills(peer_id=who_id)
                                inv = ','.join([f' {item}' for (item,) in invList])
                                import re
                                if re.search(r'\w+', inv) is None:
                                    invent = ''
                                else:
                                    invent = '💼 Инвентарь:\n' + inv

                                status = function.check_lvl_user(peer_id=who_id)
                                text = f'👨‍💻 Профиль @id{who_id}({name})' \
                                       '\n' \
                                       f'\n💫 Статус: {status}' \
                                       '\n' \
                                       '\nХарактеристики' \
                                       f'\n❤ Здоровье: {skills[0]}' \
                                       f'\n🧠 Интеллект: {skills[1]}' \
                                       f'\n🌿 Ловкость: {skills[2]}' \
                                       f'\n👨‍🏫 Мудрость: {skills[3]}' \
                                       f'\n🍀 Удача: {skills[4]}%' \
                                       f'\n' \
                                       f'\n{invent}'
                                sender(peer_id, text)

                        if message.partition(' ')[0] in ['/статус']:
                            new_status = Message[8:]

                            admin_tool = VkKeyboard(inline=True)
                            admin_tool.add_callback_button(label='Отклонить', color=VkKeyboardColor.NEGATIVE,
                                                     payload={"type": "status_denied"})
                            admin_tool.add_callback_button(label='Принять', color=VkKeyboardColor.POSITIVE,
                                                     payload={"type": "status_access"})
                            admin = admin_tool.get_keyboard()

                            user = from_id
                            chat = peer_id
                            sender(271870028, f'Пользователь @id{from_id}({fullname}) желает получить статус: {new_status}', admin)
                            sender(peer_id, 'Администратор получил вашу зявку. Она будет рассмотрена в ближайшее время. '
                                            'Спасибо за проявленное терпение!')



                        # Магазин
                        if message in ['магазин']:

                            if message in ['магазин']:

                                balance = gaming_func.check_balance(peer_id=from_id)
                                shop = VkKeyboard(inline=True)
                                if balance < 250:
                                    shop.add_callback_button(label='Препод - 250 СК', color=VkKeyboardColor.NEGATIVE,
                                                             payload={"type": "shop_byer_prepod"})
                                else:
                                    shop.add_callback_button(label='Препод - 250 СК', color=VkKeyboardColor.POSITIVE,
                                                             payload={"type": "shop_byer_prepod"})
                                    shop.add_line()

                                if balance < 56:
                                    shop.add_callback_button(label='Тетрадь 56 СК', color=VkKeyboardColor.NEGATIVE,
                                                             payload={"type": "shop_byer_notebook"})
                                else:
                                    shop.add_callback_button(label='Тетрадь 56 СК', color=VkKeyboardColor.POSITIVE,
                                                             payload={"type": "shop_byer_notebook"})
                                shop.add_line()

                                if balance < 14:
                                    shop.add_callback_button(label='Дошик - 14 СК', color=VkKeyboardColor.NEGATIVE,
                                                             payload={"type": "shop_byer_doshik"})
                                else:
                                    shop.add_callback_button(label='Дошик - 14 СК', color=VkKeyboardColor.POSITIVE,
                                                             payload={"type": "shop_byer_doshik"})
                                    shop.add_line()

                                if balance < 9999999:
                                    shop.add_callback_button(label='Мозг - 99999 СК', color=VkKeyboardColor.NEGATIVE,
                                                             payload={"type": "shop_byer_brain"})
                                else:
                                    shop.add_callback_button(label='Мозг - 9999999 СК', color=VkKeyboardColor.POSITIVE,
                                                             payload={"type": "shop_byer_brain"})

                                shoper = shop.get_keyboard()
                                text = '📝 Добро пожаловать в магазин.' \
                                       '\nЧто желаете приобрести?.'
                                vk.messages.send(
                                    peer_id=peer_id,
                                    random_id=get_random_id(),
                                    message=text,
                                    keyboard=shoper
                                )
                    else:
                        sender(peer_id, 'Пожалуйста, зарегистрируйтесь по команде /reg')

                # Только в беседах (ну и для пользователей в лс)   ---- Сделать определитель беседы
                if function.check_adm(peer_id=peer_id, lvl=0) == True:
                    # Если беседа
                    if function.checkGroup(peer_id=peer_id) == True:
                        if message in ['пн', 'вт', 'ср', 'чт', 'пт', 'сб']:
                            try:
                                current_datetime = datetime.now().date()
                                week = function.getWeek(new_date=current_datetime)
                                rasp = function.getAllRasp(group=group, pod_group=podgroup, day=message, week=week)

                                text = '\n'.join(
                                    [f'{str(message_Num)}. {str(message_timeline)} - {str(message_text)}. Ауд: {str(message_audit)}'
                                     for
                                     message_Num, message_timeline, message_text, message_audit in rasp])

                                sender(peer_id,
                                       f'Расписание {str(group)}/{str(podgroup)} на {str(message)} ({str(week)}):\n\n{str(text)}')
                            except:
                                sender(2000000009, f'Ошибка вызвана при попытке узнать расписание на день @id{from_id}')

                        if message in ['имя беседы']:
                            try:
                                sender(peer_id, "Общее - " + group_podgroup + "\nГруппа - " + group + "\nПодгруппа - " + podgroup)
                            except:
                                sender(2000000009, f'Ошибка распознавания имени беседы @id{from_id}')

                    # Задачи
                    try:
                        if message.partition(' ')[0] in ['/task','/deltask','/editask','/comtask','/uncomtask','/alltask']:
                            if message == '/alltask':
                                function.updateTask(id_chat=peer_id)
                                try:
                                    task_list = function.getTasks(id_chat=peer_id)
                                    text = '\n'.join([f'{status} ♯{num}. {str(task)}' for (num, task, status) in task_list])
                                    if text !='':
                                        sender(peer_id, f'Ваши задачи: '
                                                    f'\n\n{text}')
                                    else:
                                        sender(peer_id, 'Ваш список задач пуст 😔')
                                except:
                                    sender(peer_id, 'У вас еще нет задач.')

                            if message.partition(' ')[0] == '/task':
                                new_task = Message[Message.find(' ') + 1:]
                                function.setTask(id_chat=peer_id, task=new_task)

                            if message.partition(' ')[0] == '/deltask':
                                numbers = message[message.find(' ') + 1:]
                                while numbers!="":
                                    number_task = numbers.partition(' ')[0]
                                    function.delTask(id_chat=peer_id, num=number_task)
                                    if numbers == numbers[numbers.find(' ')+1:]:
                                        numbers =""
                                    numbers = numbers[numbers.find(' ')+1:]
                                function.updateTask(id_chat=peer_id)

                            if message.partition(' ')[0] == '/editask':
                                not_cmd = Message[Message.find(' ') + 1:]
                                num = not_cmd.partition(' ')[0]
                                new_text = not_cmd[not_cmd.find(' ') + 1:]

                                function.editTask(id_chat=peer_id, num=num, new_task=new_text)
                                sender(peer_id, 'Успешно.')

                            if message.partition(' ')[0] == '/comtask':
                                numbers = message[message.find(' ') + 1:]
                                while numbers!="":
                                    number_task = numbers.partition(' ')[0]
                                    function.comTask(id_chat=peer_id, num=number_task)
                                    if numbers == numbers[numbers.find(' ')+1:]:
                                        numbers =""
                                    numbers = numbers[numbers.find(' ')+1:]

                            if message.partition(' ')[0] == '/uncomtask':
                                numbers = message[message.find(' ') + 1:]
                                while numbers!="":
                                    number_task = numbers.partition(' ')[0]
                                    function.uncomTask(id_chat=peer_id, num=number_task)
                                    if numbers == numbers[numbers.find(' ')+1:]:
                                        numbers =""
                                    numbers = numbers[numbers.find(' ')+1:]
                    except:
                        pass

                    # Напоминания
                    try:
                        if message.partition(' ')[0] in ['напомни', 'напомнить']:
                            what = Message[Message.find(' ')+1:]
                            sec = 0
                            min = 0
                            hour = 0
                            day = 0
                            week = 0
                            import locale
                            locale.setlocale(locale.LC_TIME, 'ru_RU')

                            if 'через' in what:
                                timeline = what[what.find('через')+6:]
                                if ('секунд' or 'cекунду') in timeline:
                                    if 'секунду' == timeline:
                                        sec = 1
                                    else:
                                        sec = timeline.partition(' ')[0]
                                if ('минут' or 'минуты' or 'минуту') in timeline:
                                    if 'минуту' == timeline:
                                        min = 1
                                    else:
                                        min = timeline.partition(' ')[0]
                                if ('час' or 'часов' or 'часа') in timeline:
                                    if 'час' == timeline:
                                        hour = 1
                                    else:
                                        hour = timeline.partition(' ')[0]
                                if 'неделю' in timeline:
                                    hour = 168
                                if 'месяц' in timeline:
                                    week = 4
                                if ('дней' or 'дня' or 'день') in timeline:
                                    if 'день' in timeline:
                                        day = 2
                                    else:
                                        day = timeline.partition(' ')[0]
                                notic_time = datetime.now() + timedelta(seconds=int(sec), minutes=int(min), hours=int(hour),
                                                                    days=int(day), weeks=int(week))

                                sender(peer_id, f'Хорошо, ждите меня в {notic_time.strftime("%A, %d %B в %H:%M:%S")}')
                                text = what[:what.find('через')]

                                function.setNotice(id_chat=peer_id, timeline=notic_time.strftime("%y-%m-%d %H:%M:%S"), notic=text)

                            elif 'завтра' in what:
                                notic_time = datetime.now() + timedelta(days=1)
                                sender(peer_id, f'Хорошо, ждите меня завтра в {notic_time.strftime("%H:%M:%S")}')

                                text = what[:what.find('завтра')]
                                function.setNotice(id_chat=peer_id, timeline=notic_time.strftime("%y-%m-%d %H:%M:%S"), notic=text)

                            elif 'послезавтра' in what:
                                notic_time = datetime.now() + timedelta(days=2)
                                sender(peer_id, f'Хорошо, ждите меня послезавтра в {notic_time.strftime("%H:%M:%S")}')

                                text = what[:what.find('послезавтра')]
                                function.setNotice(id_chat=peer_id, timeline=notic_time.strftime("%y-%m-%d %H:%M:%S"), notic=text)

                            else:
                                time = what[what.find(':')-2:what.find(':')+3]
                                hour = time.partition(':')[0]
                                min = time[time.find(':')+1:]
                                notic_time = timedelta(hours=int(hour), minutes=int(min))
                                when = datetime.now() - notic_time
                                sender(peer_id, f'Хорошо, ждите меня через {when.strftime("%M")} минут, ровно в {notic_time}')
                                function.setNotice(id_chat=peer_id, timeline=notic_time, notic=text)
                    except:
                        pass

                    # Игры
                    if message.partition(' ')[0] in ['шпионстарт', 'шпионвойти', 'шпионарест', 'шпионконец', 'шпионинфо']:
                        try:
                            try:
                                command = message.partition(' ')[0]
                                count = message[message.find(" ") + 1:]
                            except:
                                print("ошибка")
                            base = vk_parsing.getUser(from_id)
                            fullname = base[0]['first_name'] + ' ' + base[0]['last_name']

                            const_minute = datetime.now().minute

                            global need_person
                            if count == command:
                                count = 4

                            if command == 'шпионстарт':
                                try:
                                    if int(count) < 3:
                                        sender(peer_id, 'У вас нет друзей?')
                                        continue
                                    need_person = count
                                    need_person = SpyGame.start(count_player=need_person, id_game=peer_id, status="chat",
                                                                id_player=000)
                                    need_person = int(need_person) + 1
                                    sender(peer_id, f'Игра Шпион начата. '
                                                    f'\nЧтобы войти в игру, введите "шпионвойти".'
                                                    f'\nНужно кол-во игроков: {need_person} '
                                                    f'\nИгра автоматически будет остановлена через 20 минут.')
                                except:
                                    print('Ошибка в "шпионстарт"')

                            if command == 'шпионвойти':
                                try:
                                    if need_person == 1:
                                        need_person = SpyGame.start(count_player=need_person, id_game=peer_id,
                                                                    id_player=from_id, status="person")
                                        sender(peer_id, f'Вы вошли в игру. Игра началась. Используйте голосовые')
                                        SpyGame.random(id_game=peer_id)
                                        location = SpyGame.location()
                                        person = SpyGame.getPerson(id_game=peer_id)
                                        spy = SpyGame.getSpy(id_game=peer_id)
                                        for x in person:
                                            sender(x, f'Локация: {location}'
                                                      f'\n\nСреди нас шпион! Его нужно найти. Быстрее возвращайся в беседу и '
                                                      f'начни задавать вопросы. Только так ты сможешь выяснить, кто чужак')

                                        for x in spy:
                                            sender(x, f'Тенденция какая, отец. Ты шпион и тебе нужно выяснить где ты. Удачи)')
                                    elif need_person < 1:
                                        sender(peer_id, f'Игра уже началась.')
                                    else:
                                        check = need_person
                                        need_person = SpyGame.start(count_player=need_person, id_game=peer_id,
                                                                    id_player=from_id, status="person")
                                        if check != need_person:
                                            sender(peer_id, f'Вы вошли в игру. Осталось: {need_person}')
                                        else:
                                            sender(peer_id, 'Вы уже в игре. Ожидайте игроков.')
                                except:
                                    print('Ошибка в "шпионвойти"')

                            if command == 'шпионарест':
                                import re

                                try:
                                    kickId0 = message[11:]
                                    kickId1 = kickId0.split('|')[0]
                                    kick_id = re.findall(r'id(.*)', kickId1)[0]
                                    voices = SpyGame.getVoice(id_game=peer_id, id_player=kick_id)
                                    need_person_const = SpyGame.getCount(id_game=peer_id)
                                    if need_person_const / voices < 2:
                                        SpyGame.kick(id_game=peer_id, id_player=kick_id)
                                        sender(peer_id, f'Игрок @id{kick_id} кикнут из игры. Был ли он шпионом?')
                                        spy_count = SpyGame.checkSpy(id_game=peer_id)

                                        if spy_count == 0:
                                            sender(peer_id, "Поздравляю! В игре не осталось ни одного шпиона! Вы победили")
                                            players = SpyGame.getPlayers(id_game=peer_id)
                                            SpyGame.finish(id_game=peer_id)
                                            for x in players:
                                                gaming_func.addBalance(peer_id=x, balance_new=50)
                                        else:
                                            sender(peer_id, f"В игре осталось шпионов: {spy_count}")
                                except:
                                    print('Ошибка в "шпионарест"')

                            try:
                                if command == 'шпионконец':
                                    SpyGame.finish(id_game=peer_id)
                                    sender(peer_id, 'Игра окончена успешно.')
                            except:
                                print("Ошибка в 'шпионконец'")

                            if command == 'шпионинфо':
                                text = '📜 Правила игры "Находка для шпиона".' \
                                       '\n\n🎯 Цель игры.' \
                                       '\nЦель шпиона: не раскрыть себя до окончания раунда или определить локацию, в которой все находятся.' \
                                       '\nЦель нешпионов: единогласно указать шпиона и, следовательно, разоблачить его.' \
                                       '\n\n🚧 Обзор игры.' \
                                       '\nИгровая партия состоит из последовательности коротких раундов. В каждом раунде игроки оказываются в какой-то локации, у каждого — свой статус. ' \
                                       'Один неизбежно оказывается шпионом, который не ' \
                                       'знает, где находится. Его задача — разговорить других игроков, определить локацию и не разоблачить ' \
                                       'себя. Каждый нешпион в свою очередь пытается ' \
                                       'обтекаемо дать понять «своим», что знает, где находится, и поэтому не является шпионом. Наблюдательность, собранность, выдержка, хитрость — ' \
                                       'в этой игре пригодится всё. Будьте начеку!' \
                                       '\n\n⛽ Ход игры.' \
                                       '\nРаздающий запускает таймер, после чего начинает игру. Он задаёт вопрос любому другому ' \
                                       'игроку, обращаясь к нему по имени: «А скажика мне, Рита...» Как правило, вопросы касаются ' \
                                       'указанной в карточке загадочной локации: это ' \
                                       'желательно, но не обязательно. Вопрос задаётся ' \
                                       'один раз и без уточнений. Ответ также может ' \
                                       'быть любым. Затем ответивший на вопрос задаёт ' \
                                       'вопрос любому другому игроку, кроме того, кто ' \
                                       'перед этим задал ему вопрос (т. е. нельзя спросить в ответ). Порядок опроса игроки выстроят ' \
                                       'сами — это будет зависеть от подозрений, основанных на вопросах и ответах. ' \
                                       '\n\n♨ Комманды.' \
                                       '\n"шпионстарт" - запустить игру с дефолтным параметром' \
                                       '\n"шпионстарт <число>" - запустить игру на <число> человек (<> - писать не нужно)' \
                                       '\n"шпионвойти" - присоединиться к игре.' \
                                       '\n"шпионарест <упоминание>" - отдать свой голос за изгнание <упоминание> игрока. ' \
                                       '\n"шпионконец" - принудительно завершает игру' \
                                       'Как только голосов больше половины участников, игрок вылетает из игры (<> - писать не нужно)' \
                                       '\n\nЗадавайте друг другу вопросы через голосовые сообщения, чтобы получать особое удовольствие.' \
                                       '\nКак только все шпионы будут выгнаны из игры, игра завершается. ' \
                                       'По окончанию всем игрокам начисляется 50 СтудКоинов' \
                                       'Игра будет дорабатываться. На данный момент, если шпион угадывает локацию, то нужно прописать "шпионконец".'
                                sender(peer_id, text)
                        except:
                            sender(2000000009, 'Ошибка в блоке "шпион"')

                    if message.partition(' ')[0] in ['расписание', 'распфото']:
                        [group_podgroup, fullname, group, podgroup, title] = getName()

                        if message[message.find(' ') + 1:] != message.partition(' ')[0]:
                            group_podgroup = message[message.find(' ') + 1:]
                            print(group_podgroup.find('/'))
                            if group_podgroup.find('/')!=(-1):
                                group = group_podgroup[:group_podgroup.find('/')]
                                podgroup = group_podgroup[group_podgroup.find('/') + 1:]
                            else:
                                group = group_podgroup
                                podgroup = None

                        if message.partition(' ')[0] == 'расписание':
                            try:
                                current_datetime = datetime.now().date()
                                week = function.getWeek(new_date=current_datetime)
                                moneday = function.getAllRasp(group=group, pod_group=podgroup, day="пн", week=week)
                                tuesday = function.getAllRasp(group=group, pod_group=podgroup, day="вт", week=week)
                                wednesday = function.getAllRasp(group=group, pod_group=podgroup, day="ср", week=week)
                                thursday = function.getAllRasp(group=group, pod_group=podgroup, day="чт", week=week)
                                friday = function.getAllRasp(group=group, pod_group=podgroup, day="пт", week=week)
                                saturday = function.getAllRasp(group=group, pod_group=podgroup, day="сб", week=week)

                                moneday_week = '\n'.join(
                                    [
                                        f'{str(message_Num)}. {str(message_timeline)} - {str(message_text)}. Ауд: {str(message_audit)}'
                                        for
                                        message_Num, message_timeline, message_text, message_audit in moneday])
                                tuesday_week = '\n'.join(
                                    [
                                        f'{str(message_Num)}. {str(message_timeline)} - {str(message_text)}. Ауд: {str(message_audit)}'
                                        for
                                        message_Num, message_timeline, message_text, message_audit in tuesday])
                                wednesday_week = '\n'.join(
                                    [
                                        f'{str(message_Num)}. {str(message_timeline)} - {str(message_text)}. Ауд: {str(message_audit)}'
                                        for
                                        message_Num, message_timeline, message_text, message_audit in wednesday])
                                thursday_week = '\n'.join(
                                    [
                                        f'{str(message_Num)}. {str(message_timeline)} - {str(message_text)}. Ауд: {str(message_audit)}'
                                        for
                                        message_Num, message_timeline, message_text, message_audit in thursday])
                                friday_week = '\n'.join(
                                    [
                                        f'{str(message_Num)}. {str(message_timeline)} - {str(message_text)}. Ауд: {str(message_audit)}'
                                        for
                                        message_Num, message_timeline, message_text, message_audit in friday])
                                saturday_week = '\n'.join(
                                    [
                                        f'{str(message_Num)}. {str(message_timeline)} - {str(message_text)}. Ауд: {str(message_audit)}'
                                        for
                                        message_Num, message_timeline, message_text, message_audit in saturday])

                                text = f'Расписание на неделю ({week}) для {group_podgroup}' \
                                       f'\n\n⁣       ПН' \
                                       f'\n{moneday_week}' \
                                       f'\n\n⁣       ВТ' \
                                       f'\n{tuesday_week}' \
                                       f'\n\n⁣       СР' \
                                       f'\n{wednesday_week}' \
                                       f'\n\n⁣       ЧТ' \
                                       f'\n{thursday_week}' \
                                       f'\n\n⁣       ПТ' \
                                       f'\n{friday_week}' \
                                       f'\n\n⁣       СБ' \
                                       f'\n{saturday_week}'

                                sender(peer_id, text)
                            except:
                                sender(2000000009, f'ошибка вызова "расписания" @id{from_id}')
                        elif message.partition(' ')[0] == 'распфото':
                            try:
                                sender(peer_id=peer_id, message='Немного подождите')
                                import shutil

                                shutil.copyfile("template.docx", "temp_template.docx")
                                file = "temp_template"
                                faculty = 'Факультет Компьютерных технологий и Прикладной математики'

                                current_datetime = datetime.now().date()
                                week = function.getWeek(new_date=current_datetime)

                                moneday = function.getAllRasp(group=group, pod_group=podgroup, day="пн", week=week)
                                tuesday = function.getAllRasp(group=group, pod_group=podgroup, day="вт", week=week)
                                wednesday = function.getAllRasp(group=group, pod_group=podgroup, day="ср", week=week)
                                thursday = function.getAllRasp(group=group, pod_group=podgroup, day="чт", week=week)
                                friday = function.getAllRasp(group=group, pod_group=podgroup, day="пт", week=week)
                                saturday = function.getAllRasp(group=group, pod_group=podgroup, day="сб", week=week)

                                docWriter.generateRasp(group, podgroup, faculty, week, moneday, tuesday, wednesday, thursday,
                                                       friday,
                                                       saturday, file)

                                # Отправить фото
                                attachments = []

                                check_file = file + '-final'
                                docWriter.docxPdf(check_file + '.docx')

                                docWriter.pdfImage(check_file + '.pdf')

                                pages = docWriter.pdfImage(check_file + '.pdf')
                                for page in pages:
                                    page.save('out.jpg', 'JPEG')

                                image = "out.jpg"
                                upload = VkUpload(vk)
                                upload_image = upload.photo_messages(photos=image)[0]
                                attachments.append('photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))

                                sender(peer_id=peer_id, message='Расписание появись!')

                                sender(peer_id=peer_id, message='Держите своё расписание!', attachment=','.join(attachments))
                                import os

                                path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'out.jpg')
                                os.remove(path)
                                path = os.path.join(os.path.abspath(os.path.dirname(__file__)), check_file + '.pdf')
                                os.remove(path)
                                path = os.path.join(os.path.abspath(os.path.dirname(__file__)), check_file + '.docx')
                                os.remove(path)
                                path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'temp_template.docx')
                                os.remove(path)
                            except:
                                sender(2000000009, f'Ошибка вызвана при попытке узнать "расписание фото" @id{from_id}')

                #Блок на любые команды
                # for sql_phrases in function.getComList():
                #     (phrases,) = sql_phrases
                #     list = phrases.split(',')
                #     for word in list:
                #         if nltk.edit_distance(word, filter_text(message)) / len(word) < 0.4:
                #             sender(peer_id, function.getCom(cmd=message, peer_id=peer_id))
                #             break

                #Для любого пользователя
                if message.partition(' ')[0] in config.keyword_phrases or '/' in message:

                    if message == 'костенко':
                        quotation = function.getQuotation()
                        text = '\n'.join(
                            [f'{str(text)}\n\n#{str(name_prepod)} {str(predmet)}\n#{str(faculty)}' for
                             text, name_prepod, predmet, faculty in quotation])
                        sender(peer_id, text)

                    if message.partition(' ')[0] == 'гороскоп':
                        text = message[9:]
                        info = function.getHoros(title=text)
                        horos = f'{info[0]}\n\n{info[1]}'

                        image = f'F:/Dev/Python/Projects/VKbot/horoscope/{info[2]}'
                        attachments = []
                        upload = VkUpload(vk)
                        upload_image = upload.photo_messages(photos=image)[0]
                        attachments.append('photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))

                        sender(peer_id, horos, ','.join(attachments))

                    if Message.partition(' ')[0] in ['/report']:
                        command = message.partition(' ')[0]
                        text = Message[message.find(" ") + 1:]

                        try:
                            request = vk.messages.getConversationsById(peer_ids=peer_id)
                            for response in request['items']:
                                chat_settings = response['chat_settings']
                                title = chat_settings['title']
                        except:
                            title = fullname
                        print(f'REPORT -> @id{from_id} ({title}): '
                              f'\n{text}')

                        report = RpcClient()
                        sender(2000000009, f'REPORT -> @id{from_id} ({title}): '
                                           f'\n{text}')
                        sender(peer_id, report.callReportTG(f'{title} -> {text}'))


                basa_roul = ['рулетка', 'пистолет', 'смерть', 'убейте']
                ford = message.split(' ')
                flag = False
                for word in basa_roul:
                    for mes in ford:
                        if nltk.edit_distance(word, filter_text(mes)) / len(word) < 0.4:
                            num = random.randint(1, 100)
                            base = vk_parsing.getUser(from_id)
                            first_name = base[0]['first_name']
                            text = f"{first_name} раскручивает барабан и подносит к виску" \
                                    f"\n..Спускает курок.."
                            msg_from = f'[id{from_id}|{first_name}]'
                            if num < 50:
                                text+=f"\n\nЩелчок! Похоже {msg_from} будет жить (В этот раз!)"
                            if num >= 50:
                                text+=f"\n\nЩелчок! Прощай {msg_from} ..."
                            sender(peer_id, text)
                            flag = True
                            break
                        if flag:
                            break

                #Дроп
                # if Message in ['LootBox']:
                #     if Message in ['LootBox']:
                #         balance = gaming_func.check_balance(peer_id=from_id)
                #
                #         loot = VkKeyboard(inline=True)
                #         loot.add_callback_button(label='LootBox за 100 sc', color=VkKeyboardColor.POSITIVE,
                #                                  payload={"type": "lootbox_100"})
                #         loot.add_line()
                #         loot.add_callback_button(label='LootBox за 5000 sc', color=VkKeyboardColor.POSITIVE,
                #                                  payload={"type": "lootbox_5000"})
                #
                #         casino = loot.get_keyboard()
                #         text = f'Откройте LootBox за 5тыс sc и получите одну из наград:' \
                #                f'\n1. От 600 до 35тыс СтудКоинов ' \
                #                f'\n2. Книга "ЭЛЕМЕНТЫ ДИСКРЕТНОЙ МАТЕМАТИКИ" К.И. Костенко' \
                #                f'\n3. Сорвать весь куш - джекпот' \
                #                f'\n4. Мозги Гения' \
                #                f'\n5. Акции компании "Ля Костя"' \
                #                f'\n6. Скидка 5% на место в очереди буфета' \
                #                f'\n\nJACKPOT: 10 000 SC' \
                #                f'\n\nВаш счёт: {balance}'
                #         vk.messages.send(
                #             peer_id=peer_id,
                #             random_id=get_random_id(),
                #             message=text,
                #             keyboard=casino
                #         )

                #РП
                if message.partition(' ')[0] in ['поцеловать', 'ушатать', 'шлепнуть', 'шлёпнуть', 'поздравляю', 'инфографик']:
                    command = message.partition(' ')[0]
                    not_cmd = message[message.find(" ") + 1:]
                    who = not_cmd[:not_cmd.find(" ")]
                    text = not_cmd[not_cmd.find(" ") + 1:]
                    if text == who+']':
                        text = ''

                    id_from = vk_parsing.getUser(from_id)
                    name_from = id_from[0]['first_name'] + ' ' + id_from[0]['last_name']
                    msg_from = f'[id{from_id}|{name_from}]'

                    try:
                        import re
                        whoId0 = who
                        whoId1 = whoId0.split('|')[0]
                        who_id = re.findall(r'id(.*)', whoId1)[0]
                        id_to = vk_parsing.getUser(who_id)
                        name_to = id_to[0]['first_name'] + ' ' + id_to[0]['last_name']
                        msg_to = f'[id{who_id}|{name_to}]'
                    except:
                        msg_to = who

                    if command == 'поцеловать':
                        if who_id == '271870028':
                            sender(peer_id, f'Я бы прокомментировал, да лень')
                        elif who_id == '219752733':
                            sender(peer_id, 'Теперь ты обязан на мне жениться')
                        else:
                            sender(peer_id, f'❤ {msg_from} 😘 поцеловал {msg_to}')

                    if command == 'ушатать':
                        if who_id == '271870028':
                            sender(peer_id, 'Ага, уже шатаюсь')
                        elif who_id == '219752733':
                            sender(peer_id, f'Жди, армянская мафия уже выехала за тобой')
                        else:
                            sender(peer_id, f'😎 {msg_from} 🤜🏻 ушатал {msg_to}')

                    if command in ['шлепнуть','шлёпнуть']:
                        if who_id == '271870028':
                            sender(peer_id, f'Отразил шлепок хуем тебе по лбу')
                        elif who_id == '219752733':
                            sender(peer_id, f'Жди, армянская мафия уже выехала за тобой')
                        else:
                            sender(peer_id, f'😏 {msg_from} ✋🏻 шлепнул {msg_to}')
                    if command == 'трахнуть':
                        if who_id == '271870028':
                            sender(peer_id, f'Он сам тебя сейчас трахнет за такие движения')
                        elif who_id == '219752733':
                            sender(peer_id, f'{msg_from}, твой джуджуль ещё не дорос для таких игр')
                        else:
                            sender(peer_id, f'😏 {msg_from} 🍆🍑 трахнул 💦{msg_to}')

                    if command == 'инфографик':
                        sender(peer_id, "", 'photo-198776140_457239393')

                    # Поздравлялка
                    # try:
                    #     if command in ['поздравляю']:
                    #         [group_podgroup, fullname, group, podgroup, title] = getName()
                    #         sender(peer_id=peer_id, message='Пожалуйста подождите')
                    #         import shutil
                    #
                    #         shutil.copyfile("mart8.docx", "mart8_template.docx")
                    #         file = "mart8_template"
                    #
                    #         base = vk_parsing.getUser(who_id)
                    #         name_to = base[0]['first_name']
                    #         base = vk_parsing.getUser(from_id)
                    #         name_from = base[0]['first_name'] + ' ' + base[0]['last_name']
                    #
                    #         docWriter.generate8mart(name_to, text, name_from, file)
                    #
                    #         # Отправить фото
                    #         attachments = []
                    #
                    #         check_file = file + '-final'
                    #
                    #         docWriter.docxPdf(check_file + '.docx')
                    #
                    #         docWriter.pdfImage(check_file + '.pdf')
                    #
                    #         pages = docWriter.pdfImage(check_file + '.pdf')
                    #         for page in pages:
                    #             page.save('8mart.jpg', 'JPEG')
                    #
                    #         image = "F:/Dev/Python/Projects/VKbot/8mart.jpg"
                    #         upload = VkUpload(vk)
                    #         upload_image = upload.photo_messages(photos=image)[0]
                    #         attachments.append('photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))
                    #         if peer_id == from_id:
                    #             id = who_id
                    #         else:
                    #             id = peer_id
                    #
                    #         vk.messages.send(
                    #             peer_id=id,
                    #             message=f'Тебе сюрприз от [id{from_id}|{name_from}] 😏',
                    #             random_id=get_random_id(),
                    #             attachment=','.join(attachments)
                    #         )
                    #         import os
                    #
                    #         path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '8mart.jpg')
                    #         os.remove(path)
                    #         path = os.path.join(os.path.abspath(os.path.dirname(__file__)), check_file + '.pdf')
                    #         os.remove(path)
                    #         path = os.path.join(os.path.abspath(os.path.dirname(__file__)), check_file + '.docx')
                    #         os.remove(path)
                    #         path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'mart8_template.docx')
                    #         os.remove(path)
                    # except:
                    #     sender(2000000009, f'Ошибка в поздравлении вызванная @id{from_id}')

                if message in ['здравствуйте!\nменя заинтересовал этот товар.']:
                    market = event.object.message['attachments']
                    ld = json.dumps(market)
                    market_att = json.loads(ld)
                    title = ''
                    price_rub = 0
                    price_sc = 0
                    for x in market_att:
                        title = x['market']['title']
                        price = x['market']['price']['amount']
                        price_rub = int(price)/100
                        price_sc = int(price)/10

                    chose_value = VkKeyboard(inline=True)
                    chose_value.add_callback_button(label='Рубли', color=VkKeyboardColor.NEGATIVE,
                                                 payload={"type": "Ruble"})
                    chose_value.add_callback_button(label='СтудКоины', color=VkKeyboardColor.POSITIVE,
                                                 payload={"type": "StudCoin"})

                    chose_key = chose_value.get_keyboard()

                    text = 'Выберите способ оплаты для '+title+'.\nВ рублях = '+str(price_rub)+\
                               '\nВ СтудКоинах = '+str(price_sc)
                    sender(peer_id, text, chose_key)

                #Любое другое сообщение
                else:
                    base = vk_parsing.getUser(from_id)
                    fullname = base[0]['first_name'] + ' ' + base[0]['last_name']
                    try:
                        if fullname == title:
                            text = f'{fullname}: {message}'
                        else:
                            text = f'{title} -> {fullname}: {message}'
                    except:
                        text = f'{fullname}: {message}'

                    import requests  # импортируем модуль
                    att = event.object.message['attachments']

                    rpc = RpcClient()
                    info = {
                        "peer_id": peer_id,
                        "from_id": from_id,
                        "message": message,
                        "attachments": event.object.message['attachments']
                    }

                    link = None
                    for x in att:
                        try:
                            link = x['audio_message']['link_mp3']
                        except:
                            pass

                    if link != None:
                        req = requests.get(link, stream=True)
                        with open('F:\Dev\Python\Projects\CoreBot\Audio.mp3', 'wb') as a:
                            a.write(req.content)
                        audio = {
                            'peer_id': peer_id,
                            'from_id': from_id,
                            'text': 'audio_message',
                            'fwd_messages':[],
                            'attachments':[]
                        }
                        answer = json.loads(rpc.call(audio))
                        if answer['text'] != 'No':

                            audiom = []
                            upload = VkUpload(vk)
                            audio_path = "F:\dev\python\projects\CoreBot\output.ogg"
                            upload_audio = upload.document(
                                    audio_path,
                                    doc_type='audio_message',
                                    message_peer_id=271870028,
                                    group_id=198776140,
                                    to_wall=False
                            )['audio_message']
                            audiom.append('doc{}_{}'.format(upload_audio['owner_id'], upload_audio['id']))
                            sender(peer_id, '', ','.join(audiom))
                    else:
                        answer = json.loads(rpc.call(event.object.message))
                        print(answer)
                        if answer['type'] in ['ai_lvl', 'any_cmd', 'answer']:
                            text = f"{answer['text']}"
                            sender(answer['peer_id'], text)

            #Если это не сообщение, а кнопка
            elif event.type == VkBotEventType.MESSAGE_EVENT:
                CALLBACK_TYPES = ('show_snackbar', 'open_link', 'open_app')
                try:
                    print(event.obj)
                    if event.object.payload.get('type') in CALLBACK_TYPES:
                        r = vk.messages.sendMessageEventAnswer(
                            event_id=event.object.event_id,
                            user_id=event.object.user_id,
                            peer_id=event.object.peer_id,
                            event_data=json.dumps(event.object.payload))


                    elif event.object.payload.get('type') == 'status_denied':
                        sender(user, 'Ваша заявка была отклонена(')
                        new_status = ''
                        user = 0
                        chat = 0

                    elif event.object.payload.get('type') == 'status_access':
                        function.add_status(peer_id=user, new_status=new_status)
                        sender(chat, 'Ваша заявка была одобрена! Напишите "Профиль", чтобы проверить!')

                    elif event.object.payload.get('type') == 'my_own_100500_type_edit':
                        request = vk.messages.getConversationsById(peer_ids=peer_id)
                        for response in request['items']:
                            chat_settings = response['chat_settings']
                            title = chat_settings['title']
                        answer = function.registerGroup(peer_id=event.obj.peer_id, uname=title)
                        if answer == True:
                            text = '✅ Ваша беседа была зарегистрирована.' \
                                   '\n📜 Справка: vk.com/@fktpm_ss-fktpm-bot' \
                                   '\n📢 Если понравится бот, подпишитесь пожалуйста на группу. Так вы сможете узнавать все новости первыми :)' \
                                   '\n⚠ Для того, чтобы узнать комманды пропишите "/help"'
                            last_id = vk.messages.edit(
                                peer_id=event.obj.peer_id,
                                message=text,
                                conversation_message_id=event.obj.conversation_message_id
                            )

                    elif event.object.payload.get('type') == 'shop_byer_prepod':
                        text = gaming_func.buy_item(peer_id=event.obj.user_id, need_money=250, item="Препод")
                        vk.messages.edit(
                            peer_id=event.obj.peer_id,
                            message=text,
                            conversation_message_id=event.obj.conversation_message_id
                        )
                    elif event.object.payload.get('type') == 'shop_byer_notebook':
                        text = gaming_func.buy_item(peer_id=event.obj.user_id, need_money=56, item="Тетрадь")
                        vk.messages.edit(
                            peer_id=event.obj.peer_id,
                            message=text,
                            conversation_message_id=event.obj.conversation_message_id
                        )
                    elif event.object.payload.get('type') == 'shop_byer_doshik':
                        text = gaming_func.buy_item(peer_id=event.obj.user_id, need_money=14, item="Доширак")
                        vk.messages.edit(
                            peer_id=event.obj.peer_id,
                            message=text,
                            conversation_message_id=event.obj.conversation_message_id
                        )
                    elif event.object.payload.get('type') == 'shop_byer_brain':
                        text = gaming_func.buy_item(peer_id=event.obj.user_id, need_money=9999999, item="Мозг")
                        vk.messages.edit(
                            peer_id=event.obj.peer_id,
                            message=text,
                            conversation_message_id=event.obj.conversation_message_id
                        )

                    elif event.object.payload.get('type') == 'lootbox_100':
                        text = gaming_func.lootGift(from_id=from_id, need_money=100)
                        vk.messages.edit(
                            peer_id=event.obj.peer_id,
                            message=text,
                            conversation_message_id=event.obj.conversation_message_id
                        )
                    elif event.object.payload.get('type') == 'lootbox_5000':
                        text = gaming_func.lootGift(from_id=from_id, need_money=5000)
                        vk.messages.edit(
                            peer_id=event.obj.peer_id,
                            message=text,
                            conversation_message_id=event.obj.conversation_message_id
                        )


                    elif event.object.payload.get('type') == 'Ruble':
                        sender(peer_id, 'С вас бабки')
                    elif event.object.payload.get('type') == 'StudCoin':
                        sender(peer_id, 'Хорошо!')
                except:
                    sender(2000000009, 'Ошибка при нажатии кнопок')
    #На случай падения серверов
    except (requests.exceptions.ConnectionError, TimeoutError, requests.exceptions.Timeout,
        requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
        def recon():
            print("\n----> Попытка повторного соединения <----\n")
            try:
                start()
                print("<---> Успешно! <--->")
            except:
                print("<---! Не удачно !--->")
                recon()
        print("\n----- Потеря соединения с серверами ВК -----\n")
        import time
        time.sleep(60)
        recon()


def callVK(ch, method, props, body):
    message = body.decode()
    sender(peer_id=2000000001, message=message)



def loop_b():
    while True:
        now = datetime.now().strftime("%y-%m-%d %H:%M:%S")
        try:
            (id_chat, ntc) = function.getNotice(timeline=now)
            #out = ''.join([f'{id_chat} - {notic}'] for id_chat, notic in text)
            sender(id_chat, f'🔔 Вы просили напомнить: {ntc}')
            function.delNotice(id_chat=id_chat, notice=ntc)
        except:
            pass

        try:
            connection = pika.BlockingConnection()
            channel = connection.channel()

            channel.exchange_declare(exchange='telegram_msg', exchange_type='fanout')

            result = channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue

            channel.queue_bind(exchange='telegram_msg', queue=queue_name)
            channel.basic_consume(
                queue=queue_name, on_message_callback=callVK, auto_ack=True)

            #channel.queue_declare(queue='VK_queue')
            #channel.basic_consume(queue='VK_queue', on_message_callback=callbackVK)

            channel.start_consuming()
        except:
            pass
        import time
        time.sleep(1)

# def listen(longpoll, admin, chat: str):
#     for e in longpoll.listen():
#         if e.type == VkBotEventType.MESSAGE_NEW:
#             spy_message = e.object.message['text']
#             sender(admin, spy_message)
#
#             if function.check_adm(peer_id=admin, lvl=100) == True:
#                 if spy_message == '/cancel':
#                     sender(chat, 'Администрация покинула ваш чат.')
#                     Process(target=listen).close()

def start():
    Process(target=loop_a).start()
    Process(target=loop_b).start()

if __name__ == '__main__':
    # Process(target=loop_a).start()
    # Process(target=loop_b).start()
    Process(target=bot).start()