import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from commander import Commander


class Server:
    def __init__(self, api_token, group_id, server_name: str = "Empty"):
        self.server_name = server_name

        self.vk = vk_api.VkApi(token=api_token)

        self.long_poll = VkBotLongPoll(self.vk, group_id)

        self.vk_api = self.vk.get_api()

        self.users={}

    def sender(self, peer_id, message, keyboard=None, attachment=None, template=None):
        """
        Отправка сообщения методом messages.send
        :param peer_id:
        :param message:
        :return:
        """

        self.vk_api.messages.send(
            peer_id=peer_id,
            message=message,
            attachment=attachment,
            random_id=get_random_id(),
            keyboard=keyboard,
            template=template
        )

    def sender_edit(self, peer_id, conversation_message_id, message, keyboard=None):
        """
        Изменение предыдущего сообщения системы
        :param peer_id: пользователь
        :param message: сообщение
        :param conversation_message_id: предыдущее сообщение
        :param keyboard: клавиатура
        :return:
        """

        self.vk_api.messages.edit(
            peer_id=peer_id,
            message=message,
            conversation_message_id=conversation_message_id,
            keyboard=keyboard
        )

    def start(self):
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:

                from_id = event.object.message['from_id']  # id пользователя, который отправил сообщение
                peer_id = event.object.message['peer_id']  # peer_id беседы или ЛС, откуда пришло сообщение
                message = event.object.message['text'].lower()
                msg = event.object.message['text']
                start_msg = message

                if peer_id < 2000000000:
                    if event.object.from_id not in self.users:
                        self.users[from_id] = Commander(from_id)
                    if event.type == VkBotEventType.MESSAGE_NEW:
                        self.sender(from_id, *self.users[from_id].input(message))

            elif event.type == VkBotEventType.MESSAGE_EVENT:
                peer_id = event.obj.peer_id

                if event.object.from_id not in self.users:
                    self.users[peer_id] = Commander(peer_id)

                if event.type == VkBotEventType.MESSAGE_EVENT:
                    CALLBACK_TYPES = ('show_snackbar', 'open_link', 'open_app')
                    if event.object.payload.get('type') in CALLBACK_TYPES:
                        import json
                        self.vk_api.messages.sendMessageEventAnswer(
                            event_id=event.object.event_id,
                            user_id=event.object.user_id,
                            peer_id=event.object.peer_id,
                            event_data=json.dumps(event.object.payload)
                        )
                    elif event.object.payload.get('type') == 'personal-area':
                        self.sender(peer_id, event.obj.conversation_message_id,
                                    *self.users[peer_id].event(event.object.payload, peer_id)
                                    )
                    else:
                        self.sender_edit(peer_id, event.obj.conversation_message_id,
                                         *self.users[peer_id].event(event.object.payload, peer_id)
                                         )

