import json
from command_enum import Command
from mode_enum import Mode
from plugins import config, function, keyboards, languages, vk_parsing


class Commander:

    def __init__(self, user_id):

        self._USERID = user_id
        self._USERNAME = vk_parsing.getUsername(user_id)

        self.now_mode = Mode.default
        self.last_mode = Mode.default

        self.last_command = None

        self.last_ans = None


    def change_mode(self, to_mode):
        """
        Меняет режим приёма команд
        :param to_mode: Изменённый мод
        """

        self.last_mode = self.now_mode
        self.now_mode = to_mode

        self.last_ans = None

    def input(self, msg):
        """
        Функция принимающая сообщения пользователя
        :param msg: Сообщение
        :return: Ответ пользователю
        """

        if msg.startswith("/"):
            for mode in Mode:
                if msg[1::] in mode.value:
                    self.change_mode(mode)
                    return "Режим изменен на " + self.now_mode.value[0]
            return "Неизвестный мод " + msg[1::]

        if self.now_mode == Mode.default:

            if msg in config.hello_msg:
                status, situation = function.checkUser(self._USERID, self._USERNAME)
                if status:
                    lang = function.checkLang(user_id=self._USERID)
                    arrLang = languages.arrLang[lang]
                    arrBtn = languages.btn[lang]

                    if situation == 1:  # Новый
                        kbrd = keyboards.lang()
                        return arrLang['choose-lang'], kbrd.get_keyboard()
                    elif situation == 2:  # Бывалый
                        kbrd = keyboards.main_menu(lang)
                        return arrLang['main-menu-info'], kbrd.get_keyboard()

            if msg in ['f']:
                self.last_ans = msg
                self.now_mode = self.last_mode
                # Мод работы с клавиатурой

        if self.now_mode == Mode.default:
            # Мод обратной связи
            pass

        return 'Ошибка!'

    def event(self, payload, peer_id):

        lang = function.checkLang(user_id=peer_id)
        arrLang = languages.arrLang[lang]
        ARRVUZ = ['university', 'info-kubsu', 'input-kubsu', 'univ-live', 'spam',
                  'univ-live-struct', 'univ-live-clubs', 'univ-live-news', 'univ-live-plans',
                  'univ-live-opportunities', 'univ-live-museum']
        CLUBS = ['presscenter', 'imperial', 'greencubik', 'gamedesign', 'patriotvosp',
                 'debatclub', 'clubnastav', 'studotryad', 'nackult']
        ARRFAC = ['biofacult', 'iggts', 'fad', 'jurfuck', 'fismo',
                  'fktpm', 'matfak', 'fppk', 'rgf', 'fup', 'fhivt',
                  'ftf', 'filfac', 'hudgraf', 'econom', 'urfak', 'inspo']
        ARRFACLIST = ['biofacult', 'iggts', 'fad', 'jurfuck', 'fismo',
                  'fktpm', 'matfak', 'fppk', 'rgf', 'fup', 'fhivt',
                  'ftf', 'filfac', 'hudgraf', 'econom', 'urfak', 'inspo', 'faculties',
                      'fac', 'fac1', 'fac2', 'fac3', 'fac4']

        if payload.get('type') in ['lang_rus', 'lang_eng', 'lang_it', 'lang_am', 'lang_kz']:
            lang_choose = payload.get('type')
            lang = ('ru-RU' if lang_choose == 'lang_rus' else 'it-IT' if lang_choose == 'lang_it'
            else 'kk-KZ'if lang_choose == 'lang_kz' else 'uk-UA' if lang_choose == 'lang_ua'
            else 'en-GB'if lang_choose != 'lang_am' else 'hy-AM')
            # Тут функция для изменения в базе данных
            function.setLang(user_id=peer_id, lang=lang)
            arrLang = languages.arrLang[lang]

            return (arrLang['settings-save'] if function.checkAgree(user_id=peer_id) else arrLang['conf-choose-lang']),\
                   (keyboards.new_start(lang).get_keyboard() if function.checkAgree(user_id=peer_id)
                    else keyboards.agreement(lang).get_keyboard())

        elif payload.get('type') in ['agr_yes', 'agr_no']:
            if payload.get('type') == 'agr_yes':
                new_start = keyboards.new_start(lang)
                function.setAgree(user_id=peer_id, status=1)
                return arrLang['accept-agreement'], new_start.get_keyboard()

            elif payload.get('type') == 'agr_no':
                function.setAgree(user_id=peer_id, status=0)
                return arrLang['deny-agreement']

        # Обработчик главного меню
        elif payload.get('type') == 'main-menu_list':
            main_menu = keyboards.main_menu(lang)
            return arrLang['main-menu-info'], main_menu.get_keyboard()

        # Обработчик Вуза
        elif payload.get('type') in ARRVUZ:
            arrLang = arrLang['univ-menu']
            if payload.get('type') == 'university':
                menu_univ = keyboards.univ(lang, 'main-menu_list')
                return arrLang['start'], menu_univ.get_keyboard()

            # Меню Вуза
            elif payload.get('type') == 'info-kubsu':
                kbrd = keyboards.backKbr(lang, 'university')
                return arrLang['info'], kbrd.get_keyboard()
            elif payload.get('type') == 'input-kubsu':
                kbrd = keyboards.inputkubsu(lang, 'university')
                return arrLang['input'], kbrd.get_keyboard()
            elif payload.get('type') == 'univ-live':
                kbrd = keyboards.univLife(lang, 'university')
                return arrLang['life']['info'], kbrd.get_keyboard()
            elif payload.get('type') == 'spam':
                kbrd = keyboards.backKbr(lang, 'university')
                return arrLang['spam'], kbrd.get_keyboard()

            # Меню Унив. Жизни
            elif payload.get('type') == 'univ-live-news':
                kbrd = keyboards.backKbr(lang, 'univ-live')
                return arrLang['life']['news'], kbrd.get_keyboard()
            elif payload.get('type') == 'univ-live-plans':
                kbrd = keyboards.backKbr(lang, 'univ-live')
                return arrLang['life']['mer'], kbrd.get_keyboard()
            elif payload.get('type') == 'univ-live-struct':
                kbrd = keyboards.backKbr(lang, 'univ-live')
                return arrLang['life']['struct'], kbrd.get_keyboard()
            elif payload.get('type') == 'univ-live-clubs':
                kbrd = keyboards.clubsMenu(lang, 'univ-live')
                return arrLang['life']['clubs']['info'], kbrd.get_keyboard()
            elif payload.get('type') == 'univ-live-opportunities':
                kbrd = keyboards.backKbr(lang, 'univ-live')
                return arrLang['life']['opportunities'], kbrd.get_keyboard()
            elif payload.get('type') == 'univ-live-museum':
                kbrd = keyboards.backKbr(lang, 'univ-live')
                return arrLang['life']['museum'], kbrd.get_keyboard()

        # Обработчик Поступление
        elif payload.get('type') == 'bacmag':
            kbrd = keyboards.bacmag(lang, 'university')
            return 'Хочешь поступать в КубГУ? Супер! Выбирай нужный раздел и узнай всё.', kbrd.get_keyboard()
        elif payload.get('type') == 'aspir':
            pass

        # Обработчик Клубов
        elif payload.get('type') in CLUBS:
            club = payload.get('type')
            arrLang = arrLang['univ-menu']['life']['clubs']
            kbrd = keyboards.backKbr(lang, 'univ-live-clubs')
            return arrLang[club], kbrd.get_keyboard()

        # Обработчик общего меню факультетов
        elif payload.get('type') in ARRFACLIST:
            if payload.get('type') == 'faculties':
                kbrd = keyboards.facults_menu(lang, 'main-menu_list')
                return arrLang['faculties-info'], kbrd.get_keyboard()
            elif payload.get('type') == 'fac1':
                kbrd = keyboards.facults_menu1(lang, 'main-menu_list')
                return 'Page: 1', kbrd.get_keyboard()
            elif payload.get('type') == 'fac2':
                kbrd = keyboards.facults_menu2(lang, 'main-menu_list')
                return 'Page: 2', kbrd.get_keyboard()
            elif payload.get('type') == 'fac3':
                kbrd = keyboards.facults_menu3(lang, 'main-menu_list')
                return 'Page: 3', kbrd.get_keyboard()
            elif payload.get('type') == 'fac4':
                kbrd = keyboards.facults_menu4(lang, 'main-menu_list')
                return 'Page: 4', kbrd.get_keyboard()

            # Обработка конкретного факультета и его кнопок
            elif payload.get('type') == 'fac':
                button = payload.get('button')
                fac = payload.get('fac')
                kbrd = keyboards.backKbr(lang, fac)
                info = json.loads(function.getFacInfo(fac))
                info = info[lang][0][button]
                return info, kbrd.get_keyboard()
            # Информация о выбранном факультете
            elif payload.get('type') in ARRFAC:
                kbrd = keyboards.fac_menu(lang, 'main-menu_list', payload.get('type'))
                return arrLang['faculties-info'], kbrd.get_keyboard()

        # Обработчик меню навигации
        elif payload.get('type') in ['menu-nav', '1-nav', '2-nav', '3-nav', '4-nav']:
            if payload.get('type') == 'menu-nav':
                kbrd = keyboards.nav_menu(lang, 'main-menu_list')
                return arrLang['navigation-menu-info'], kbrd.get_keyboard()

        # Обработчик меню настроек
        elif payload.get('type') in ['settings-menu', 'set-change_lang', 'other-lang', 'about-app']:
            if payload.get('type') == 'settings-menu':
                kbrd = keyboards.setting_menu(lang, 'main-menu_list')
                return arrLang['settings-menu-info'], kbrd.get_keyboard()
            elif payload.get('type') == 'set-change_lang':
                kbrd = keyboards.lang()
                return arrLang['choose-lang'], kbrd.get_keyboard()
            elif payload.get('type') == 'other-lang':
                kbrd = keyboards.other_lang(lang)
                return arrLang['choose-lang'], kbrd.get_keyboard()
            elif payload.get('type') == 'about-app':
                kbrd = keyboards.backKbr(lang, 'settings-menu')
                return arrLang['about-app'], kbrd.get_keyboard()

        # Модули
        elif payload.get('type') in ['app-menu', 'blanks', 'wifi', 'panorama']:
            arrLang = arrLang['app-menu']
            if payload.get('type') == 'app-menu':
                kbrd = keyboards.app(lang, 'main-menu_list')
                return arrLang['info'], kbrd.get_keyboard()
            elif payload.get('type') == 'blanks':
                kbrd = keyboards.backKbr(lang, 'app-menu')
                return arrLang['blanks'], kbrd.get_keyboard()
            elif payload.get('type') == 'wifi':
                kbrd = keyboards.backKbr(lang, 'app-menu')
                return arrLang['wifi'], kbrd.get_keyboard()
            elif payload.get('type') == 'panorama':
                kbrd = keyboards.backKbr(lang, 'settings-menu')
                return 'Кто же нас создал?!' \
                       '\nНикто не знает.' \
                       '\nМы самый главный секрет человечества...' \
                       '\n\nСоздатель: [id1|Павел Дуров]' \
                       '\nМы в ВК: [panorama_kubsu|ИА «Панорама КубГУ»]', kbrd.get_keyboard()

        # Личный кабинет
        elif payload.get('type') == 'personal-area':
            kbrd = keyboards.backKbr(lang, 'main-menu_list')
            return 'Разработка', kbrd.get_keyboard()

        # Магазин
        elif payload.get('type') == 'shop':
            kbrd = keyboards.backKbr(lang, 'main-menu_list')
            return 'Разработка', kbrd.get_keyboard()

        message = 'text'
        keyboard = keyboards.backKbr('ru-RU', 'main-menu_list')
        return message, keyboard
