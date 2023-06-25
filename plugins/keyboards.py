import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from plugins.languages import btn

settings = dict(one_time=False, inline=True)


#########################
#       Выбрать язык
# -----------------------
#  Русский | Английский | Другой
#########################
def lang():
    keyboard = VkKeyboard(**settings)
    keyboard.add_callback_button(label='🇷🇺 Русский', color=VkKeyboardColor.PRIMARY, payload={'type': 'lang_rus'})
    keyboard.add_callback_button(label='🇬🇧 English', color=VkKeyboardColor.PRIMARY, payload={'type': 'lang_eng'})
    keyboard.add_callback_button(label='Other', color=VkKeyboardColor.SECONDARY,
                                 payload={'type': 'other-lang', 'back-menu': 'lang'})
    return keyboard


#########################
#       Другие языки
# -----------------------
#  Итальянский | Армянский | Украинский, Казахстанский
#                   Назад
#########################
def other_lang(lang):
    btn_name = btn[lang]
    keyboard = VkKeyboard(**settings)
    keyboard.add_callback_button(label='🇮🇹 Italia', color=VkKeyboardColor.PRIMARY, payload={'type': 'lang_it'})
    keyboard.add_line()
    keyboard.add_callback_button(label='🇦🇲 հայերեն', color=VkKeyboardColor.PRIMARY, payload={'type': 'lang_am'})
    keyboard.add_line()
    keyboard.add_callback_button(label='🇺🇦 Український', color=VkKeyboardColor.PRIMARY, payload={'type': 'lang_ua'})
    keyboard.add_line()
    keyboard.add_callback_button(label='🇰🇿 Казахстанский', color=VkKeyboardColor.PRIMARY,
                                 payload={'type': 'lang_kz'})
    keyboard.add_line()
    keyboard.add_callback_button(label=btn_name['back'], color=VkKeyboardColor.NEGATIVE, payload={'type': 'set-change_lang'})
    return keyboard


#########################
#       Соглашение
# -----------------------
#  Принять | Отклонить
#########################
def agreement(lang):
    btn_name = btn[lang]
    keyboard = VkKeyboard(**settings)
    keyboard.add_callback_button(label=btn_name['accept'], color=VkKeyboardColor.POSITIVE,
                                 payload={'type':'agr_yes'})
    keyboard.add_callback_button(label=btn_name['deny'], color=VkKeyboardColor.NEGATIVE, payload={'type':'agr_no'})
    return keyboard


####################################################
#                   Первое меню
# --------------------------------------------------
#  Главное меню | Команды | Документация | Настройки
####################################################
def new_start(lang):
    btn_name = btn[lang]
    keyboard = VkKeyboard(**settings)
    keyboard.add_callback_button(label=btn_name['main-menu'], color=VkKeyboardColor.PRIMARY,
                                 payload={'type': 'main-menu_list'})
    keyboard.add_callback_button(label=btn_name['commands'], color=VkKeyboardColor.SECONDARY,
                                 payload={'type': 'command_list'})
    keyboard.add_callback_button(label=btn_name['instructions'], color=VkKeyboardColor.SECONDARY,
                                 payload={'type': 'doc_list'})
    keyboard.add_callback_button(label=btn_name['settings'], color=VkKeyboardColor.SECONDARY,
                                 payload={'type': 'settings-menu'})
    return keyboard


##################################################
#                                   Главное меню
# ------------------------------------------------
#  Вуз (university)               | Факультеты (faculties) | Навигатор (nav) | F.A.Q (menu-faq)
#  Личный кабинет (personal-area) | Модули (app-menu)      | Магазин (shop)
#                                  Настройки (settings-menu)
##################################################
def main_menu(lang):

    btn_name = btn[lang]
    btn_menu = btn_name['main-menu-list']

    keyboard = VkKeyboard(**settings)

    keyboard.add_callback_button(label=btn_menu['university'], color=VkKeyboardColor.SECONDARY,
                                 payload={'type': 'university', 'back-menu': 'main-menu_list'})
    keyboard.add_callback_button(label=btn_menu['faculties'], color=VkKeyboardColor.SECONDARY,
                                 payload={'type': 'faculties', 'back-menu': 'main-menu_list'})
    keyboard.add_callback_button(label=btn_menu['nav'], color=VkKeyboardColor.SECONDARY,
                                 payload={'type': 'menu-nav', 'back-menu': 'main-menu_list'})
    keyboard.add_callback_button(label=btn_menu['faq'], color=VkKeyboardColor.SECONDARY,
                                 payload={'type': 'menu-faq', 'back-menu': 'main-menu_list'})
    keyboard.add_line()
    keyboard.add_callback_button(label=btn_menu['personal-area'], color=VkKeyboardColor.PRIMARY,
                                 payload={"type": "show_snackbar", "text": "Личный кабинет скоро появится."
                                                                           "\n\n*Уведомление исчезнет само по себе "
                                                                           "через несколько секунд"})
                                 #payload={'type': 'personal-area', 'back-menu': 'main-menu_list'})
    keyboard.add_callback_button(label=btn_menu['app'], color=VkKeyboardColor.SECONDARY,
                                 payload={'type': 'app-menu'})
    keyboard.add_callback_button(label=btn_menu['shop'], color=VkKeyboardColor.POSITIVE,
                                 payload={"type": "show_snackbar", "text": "Магазин скоро появится."
                                                                           "\n\n*Уведомление исчезнет само по себе "
                                                                           "через несколько секунд"})
                                 #payload={'type': 'shop', 'back-menu': 'main-menu_list'})
    keyboard.add_line()
    keyboard.add_callback_button(label=btn_menu['settings'], color=VkKeyboardColor.NEGATIVE,
                                 payload={'type': 'settings-menu', 'back-menu': 'main-menu_list'})

    return keyboard

##################################
#      Клавиатура приложений
# --------------------------------
#  Wi-Fi | Бланки | Моб.Приложения
#         Назад
##################################
def app(lang, back):
    btn_name = btn[lang]
    btn_menu = btn_name['app-menu']

    keyboard = VkKeyboard(**settings)
    keyboard.add_callback_button(label=btn_menu['wifi'], color=VkKeyboardColor.PRIMARY, payload={'type': 'wifi'})
    keyboard.add_callback_button(label=btn_menu['blanks'], color=VkKeyboardColor.PRIMARY, payload={'type': 'blanks'})
    keyboard.add_callback_button(label=btn_menu['smartapp'], payload={'type': 'mobapp'})

    keyboard.add_line()
    keyboard.add_callback_button(label=btn_menu['panorama'], color=VkKeyboardColor.POSITIVE, payload={'type': 'panorama'})
    keyboard.add_callback_button(label=btn_name['back'], color=VkKeyboardColor.NEGATIVE, payload={'type': back})
    return keyboard

#######################################################
#                        Вуз
# ----------------------------------------------------
#  О КубГУ (info-kubsu)   | Поступление (input-kubsu)
#  Унив.Жизнь (univ-live) | Рассылка (spam)
#                       Назад
#######################################################
def univ(lang, back):
    btn_name = btn[lang]
    btn_menu = btn_name['univ-menu']

    keyboard = VkKeyboard(**settings)
    keyboard.add_callback_button(label=btn_menu['info-kubsu'], color=VkKeyboardColor.PRIMARY,
                                 payload={'type': 'info-kubsu'})
    keyboard.add_callback_button(label=btn_menu['inkubsu'], color=VkKeyboardColor.PRIMARY,
                                 payload={'type': 'input-kubsu'})
    keyboard.add_line()
    keyboard.add_callback_button(label=btn_menu['univ-live'], color=VkKeyboardColor.PRIMARY,
                                 payload={'type': 'univ-live'})
    keyboard.add_callback_button(label=btn_menu['spam'], color=VkKeyboardColor.PRIMARY, payload={'type': 'spam'})

    keyboard.add_line()
    keyboard.add_callback_button(label=btn_name['back'], color=VkKeyboardColor.NEGATIVE, payload={'type': back})
    return keyboard


###############################################
#                   Поступление
# --------------------------------------------
# Бакалавр/Маг (bacmag) | Аспирантура (aspir)
#                     Назад
###############################################
def inputkubsu(lang, back):
    btn_name = btn[lang]
    btn_menu = btn_name['inkubsu-btn']['naprav']

    keyboard = VkKeyboard(**settings)
    keyboard.add_callback_button(label=btn_menu['bakmag'], color=VkKeyboardColor.PRIMARY, payload={'type': 'bacmag'})
    keyboard.add_callback_button(label=btn_menu['aspir'], color=VkKeyboardColor.PRIMARY, payload={'type': 'aspir'})

    keyboard.add_line()
    keyboard.add_callback_button(label=btn_name['back'], color=VkKeyboardColor.NEGATIVE, payload={'type': back})
    return keyboard


#
def bacmag(lang, back):
    btn_name = btn[lang]
    btn_menu = btn_name['inkubsu-btn']['whatis']

    keyboard = VkKeyboard(**settings)
    keyboard.add_callback_button(label=btn_menu['what-bakmag'], color=VkKeyboardColor.PRIMARY, payload={'type': ''})
    keyboard.add_callback_button(label=btn_menu['what-aspir'], color=VkKeyboardColor.PRIMARY, payload={'type': ''})
    keyboard.add_line()
    keyboard.add_callback_button(label=btn_menu['contacts'], color=VkKeyboardColor.PRIMARY, payload={'type': ''})
    keyboard.add_callback_button(label=btn_menu['napravs'], color=VkKeyboardColor.PRIMARY, payload={'type': ''})
    keyboard.add_line()
    keyboard.add_callback_button(label=btn_menu['help-abit'], color=VkKeyboardColor.PRIMARY, payload={'type': ''})
    keyboard.add_callback_button(label=btn_menu['info-home'], color=VkKeyboardColor.PRIMARY, payload={'type': ''})
    keyboard.add_line()
    keyboard.add_callback_button(label=btn_menu['documents'], color=VkKeyboardColor.PRIMARY, payload={'type': ''})
    keyboard.add_callback_button(label=btn_menu['coast'], color=VkKeyboardColor.PRIMARY, payload={'type': ''})

    keyboard.add_line()
    keyboard.add_callback_button(label=btn_name['back'], color=VkKeyboardColor.NEGATIVE, payload={'type': back})
    return keyboard

###########################################################################
#                           Университетская жизнь
# ------------------------------------------------------------------------
#  Новости (univ-live-news)              | Мероприятия (univ-live-plans)
#  Структура (univ-live-struct)          | Клубы (univ-live-clubs)
#  Возможности (univ-live-opportunities) | Музеи (univ-live-museum)
#                                   Назад
###########################################################################
def univLife(lang, back):
    btn_name = btn[lang]
    btn_menu = btn_name['univ-live-menu']

    keyboard = VkKeyboard(**settings)
    keyboard.add_callback_button(label=btn_menu['news'], color=VkKeyboardColor.PRIMARY,
                                 payload={'type': 'univ-live-news'})
    keyboard.add_callback_button(label=btn_menu['events'], color=VkKeyboardColor.PRIMARY,
                                 payload={'type': 'univ-live-plans'})
    keyboard.add_line()
    keyboard.add_callback_button(label=btn_menu['structs'], color=VkKeyboardColor.PRIMARY,
                                 payload={'type': 'univ-live-struct'})
    keyboard.add_callback_button(label=btn_menu['clubs'], color=VkKeyboardColor.PRIMARY,
                                 payload={'type': 'univ-live-clubs'})
    keyboard.add_line()
    keyboard.add_callback_button(label=btn_menu['opportunities'], color=VkKeyboardColor.PRIMARY,
                                 payload={'type': 'univ-live-opportunities'})
    keyboard.add_callback_button(label=btn_menu['museums'], color=VkKeyboardColor.PRIMARY,
                                 payload={'type': 'univ-live-museum'})

    keyboard.add_line()
    keyboard.add_callback_button(label=btn_name['back'], color=VkKeyboardColor.NEGATIVE, payload={'type': back})
    return keyboard


##################################################################
#                           Клубы
# ----------------------------------------------------------------
#  Пресс-центр (presscenter)    | Империал (imperial)
#  Зелёный Кубик (greencubik)   | Седьмая Грань (gamedesign)
#  ЦПВ (patriotvosp)            | КПД (debatclub)
#  КСН (clubnastav)             | ОРСО (studotryad)
#  ЦНК (nackult)                | Назад
##################################################################
def clubsMenu(lang, back):
    btn_name = btn[lang]
    btn_menu = btn_name['univ-live-menu']['clubs-menu']

    keyboard = VkKeyboard(**settings)
    keyboard.add_callback_button(label=btn_menu['presscenter'], payload={'type': 'presscenter'})
    keyboard.add_callback_button(label=btn_menu['imperial'], payload={'type': 'imperial'})
    keyboard.add_line()
    keyboard.add_callback_button(label=btn_menu['greencubik'], payload={'type': 'greencubik'})
    keyboard.add_callback_button(label=btn_menu['sevengran'], payload={'type': 'gamedesign'})
    keyboard.add_line()
    keyboard.add_callback_button(label=btn_menu['patriotvosp'], payload={'type': 'patriotvosp'})
    keyboard.add_callback_button(label=btn_menu['pardeb'], payload={'type': 'debatclub'})
    keyboard.add_callback_button(label=btn_menu['nastav'], payload={'type': 'clubnastav'})
    keyboard.add_callback_button(label=btn_menu['shtab'], payload={'type': 'studotryad'})
    keyboard.add_line()
    keyboard.add_callback_button(label=btn_menu['nackult'], payload={'type': 'nackult'})
    keyboard.add_callback_button(label=btn_name['back'], color=VkKeyboardColor.NEGATIVE, payload={'type': back})
    return keyboard

##################################################
#               Навигатор
# ------------------------------------------------
# По вузу | Где поесть | Распечатать | Отдохнуть
#                Назад
##################################################
def nav_menu(lang, back):

    btn_name = btn[lang]
    btn_menu = btn_name['navigation']
    keyboard = VkKeyboard(**settings)
    keyboard.add_callback_button(label=btn_menu['univ'], color=VkKeyboardColor.SECONDARY, payload={'type': '1'})
    keyboard.add_callback_button(label=btn_menu['eat'], color=VkKeyboardColor.SECONDARY, payload={'type': '2'})
    keyboard.add_callback_button(label=btn_menu['print'], color=VkKeyboardColor.SECONDARY, payload={'type': '3'})
    keyboard.add_callback_button(label=btn_menu['relax'], color=VkKeyboardColor.SECONDARY, payload={'type': '4'})

    keyboard.add_line()
    keyboard.add_callback_button(label=btn[lang]['back'], color=VkKeyboardColor.NEGATIVE, payload={'type': back})

    return keyboard


##################################################
#               Факультеты
# ------------------------------------------------

##################################################
def facults_menu(lang, back):
    btn_name = btn[lang]
    btn_menu = btn_name['facultets']

    keyboard = VkKeyboard(**settings)
    keyboard.add_callback_button(label=btn_menu['list'], color=VkKeyboardColor.POSITIVE, payload={'type': 'fac1'})
    keyboard.add_callback_button(label=btn[lang]['back'], color=VkKeyboardColor.NEGATIVE, payload={'type': back})
    return keyboard


def facults_menu1(lang, back):
    btn_name = btn[lang]
    btn_menu = btn_name['facultets']

    keyboard = VkKeyboard(**settings)
    keyboard.add_callback_button(label=btn_menu['biofacult'], color=VkKeyboardColor.SECONDARY, payload={'type': 'biofacult'})
    keyboard.add_callback_button(label=btn_menu['iggts'], color=VkKeyboardColor.SECONDARY, payload={'type': 'iggts'})
    keyboard.add_callback_button(label=btn_menu['fad'], color=VkKeyboardColor.SECONDARY, payload={'type': 'fad'})
    keyboard.add_callback_button(label=btn_menu['jurfuck'], color=VkKeyboardColor.SECONDARY, payload={'type': 'jurfuck'})
    keyboard.add_callback_button(label=btn_menu['fismo'], color=VkKeyboardColor.SECONDARY, payload={'type': 'fismo'})
    keyboard.add_line()
    keyboard.add_callback_button(label=btn_name['next'], color=VkKeyboardColor.PRIMARY,
                                     payload={'type': 'faculties'})
    keyboard.add_callback_button(label=btn_name['prev'], color=VkKeyboardColor.PRIMARY, payload={'type': 'fac2'})

    keyboard.add_line()
    keyboard.add_callback_button(label=btn[lang]['back'], color=VkKeyboardColor.NEGATIVE, payload={'type': back})

    return keyboard


def facults_menu2(lang, back):
    btn_name = btn[lang]
    btn_menu = btn_name['facultets']

    keyboard = VkKeyboard(**settings)
    keyboard.add_callback_button(label=btn_menu['fktpm'], color=VkKeyboardColor.SECONDARY,
                                     payload={'type': 'fktpm'})
    keyboard.add_callback_button(label=btn_menu['matfak'], color=VkKeyboardColor.SECONDARY, payload={'type': 'matfak'})
    keyboard.add_callback_button(label=btn_menu['fppk'], color=VkKeyboardColor.SECONDARY, payload={'type': 'fppk'})
    keyboard.add_callback_button(label=btn_menu['rgf'], color=VkKeyboardColor.SECONDARY, payload={'type': 'rgf'})
    keyboard.add_line()
    keyboard.add_callback_button(label='<-', color=VkKeyboardColor.PRIMARY, payload={'type': 'fac1'})
    keyboard.add_callback_button(label='->', color=VkKeyboardColor.PRIMARY, payload={'type': 'fac3'})

    keyboard.add_line()
    keyboard.add_callback_button(label=btn[lang]['back'], color=VkKeyboardColor.NEGATIVE, payload={'type': back})

    return keyboard


def facults_menu3(lang, back):
    btn_name = btn[lang]
    btn_menu = btn_name['facultets']
    keyboard = VkKeyboard(**settings)
    keyboard.add_callback_button(label=btn_menu['fup'], color=VkKeyboardColor.SECONDARY,
                                     payload={'type': 'fup'})
    keyboard.add_callback_button(label=btn_menu['fhivt'], color=VkKeyboardColor.SECONDARY, payload={'type': 'fhivt'})
    keyboard.add_callback_button(label=btn_menu['ftf'], color=VkKeyboardColor.SECONDARY, payload={'type': 'ftf'})
    keyboard.add_callback_button(label=btn_menu['filfac'], color=VkKeyboardColor.SECONDARY, payload={'type': 'filfac'})
    keyboard.add_line()
    keyboard.add_callback_button(label='<-', color=VkKeyboardColor.PRIMARY, payload={'type': 'fac2'})
    keyboard.add_callback_button(label='->', color=VkKeyboardColor.PRIMARY, payload={'type': 'fac4'})

    keyboard.add_line()
    keyboard.add_callback_button(label=btn[lang]['back'], color=VkKeyboardColor.NEGATIVE, payload={'type': back})

    return keyboard


def facults_menu4(lang, back):
    btn_name = btn[lang]
    btn_menu = btn_name['facultets']
    keyboard = VkKeyboard(**settings)
    keyboard.add_callback_button(label=btn_menu['hudgraf'], color=VkKeyboardColor.SECONDARY,
                                     payload={'type': 'hudgraf'})
    keyboard.add_callback_button(label=btn_menu['econom'], color=VkKeyboardColor.SECONDARY, payload={'type': 'econom'})
    keyboard.add_callback_button(label=btn_menu['urfak'], color=VkKeyboardColor.SECONDARY, payload={'type': 'urfak'})
    keyboard.add_callback_button(label=btn_menu['inspo'], color=VkKeyboardColor.SECONDARY, payload={'type': 'inspo'})
    keyboard.add_line()
    keyboard.add_callback_button(label='<-', color=VkKeyboardColor.PRIMARY, payload={'type': 'fac3'})

    keyboard.add_line()
    keyboard.add_callback_button(label=btn[lang]['back'], color=VkKeyboardColor.NEGATIVE, payload={'type': back})

    return keyboard


def fac_menu(lang, back, fac):
    btn_name = btn[lang]
    btn_menu = btn_name['facultets']['menu']

    keyboard = VkKeyboard(**settings)

    keyboard.add_callback_button(label=btn_menu['info'], payload={'type': 'fac', 'button': 'info', 'fac': fac})
    keyboard.add_callback_button(label=btn_menu['contacts'], payload={'type': 'fac', 'button': 'contacts', 'fac': fac})
    keyboard.add_callback_button(label=btn_menu['schedule'], payload={'type': 'fac', 'button': 'rasp', 'fac': fac})
    keyboard.add_line()
    keyboard.add_callback_button(label=btn_menu['stud'], payload={'type': 'fac', 'button': 'stud', 'fac': fac})
    keyboard.add_callback_button(label=btn_menu['prof'], payload={'type': 'fac', 'button': 'prof', 'fac': fac})
    keyboard.add_callback_button(label=btn_menu['sno'], payload={'type': 'fac', 'button': 'sno', 'fac': fac})

    keyboard.add_line()
    keyboard.add_callback_button(label=btn[lang]['back'], color=VkKeyboardColor.NEGATIVE, payload={'type': back})
    return keyboard


#################
#   Настройки
# ---------------
#  Сменить язык (set-change_lang)
#  О приложении (about-app)
#  VKPAY
#  Удалить себя (delete_account)
#     Назад
#################
def setting_menu(lang, back):
    btn_name = btn[lang]
    btn_menu = btn_name['setting-list']
    keyboard = VkKeyboard(**settings)
    keyboard.add_callback_button(label=btn_menu['change-lang'], color=VkKeyboardColor.SECONDARY,
                                 payload={'type': 'set-change_lang'})
    keyboard.add_callback_button(label=btn_menu['about'], color=VkKeyboardColor.SECONDARY,
                                 payload={'type': 'about-app', 'back-menu': 'settings-menu'})
    keyboard.add_line()
    keyboard.add_openlink_button(label="Donat", link="https://my.qiwi.com/Anton-BzvPXJ35lG")
    keyboard.add_callback_button(label=btn_menu['delete'], color=VkKeyboardColor.PRIMARY,
                                 payload={'type': 'delete_account'})

    keyboard.add_line()
    keyboard.add_callback_button(label=btn_name['back'], color=VkKeyboardColor.NEGATIVE, payload={'type': back})
    return keyboard


def getInfo():
    keyboard1 = VkKeyboard(**settings)
    keyboard1.add_callback_button(label='Кафедры', color=VkKeyboardColor.PRIMARY,
                                  payload={"type": "info_departments"})
    keyboard1.add_callback_button(label='Направления', color=VkKeyboardColor.PRIMARY,
                                  payload={"type": "info_directions"})
    keyboard1.add_callback_button(label='Контакты', color=VkKeyboardColor.PRIMARY,
                                  payload={"type": "info_contacts"})

    keyboard1.add_line()
    keyboard1.add_callback_button(label='Подробнее', color=VkKeyboardColor.POSITIVE,
                                  payload={"type": "open_link", "link": "https://www.kubsu.ru/ru/fktipm"})
    keyboard1.add_line()
    keyboard1.add_callback_button(label='Открыть приложение', color=VkKeyboardColor.NEGATIVE,
                                  payload={"type": "open_app", "app_id": 100500, "owner_id": 123456,
                                           "hash": "anything_data_100500"})
    keyboard1.add_line()
    keyboard1.add_callback_button(label='Покажи pop-up сообщение', color=VkKeyboardColor.SECONDARY,
                                  payload={"type": "show_snackbar", "text": "Это исчезающее сообщение"})

    return keyboard1


def getInfo2():
    keyboard2 = VkKeyboard(**settings)
    keyboard2.add_callback_button('Назад', color=VkKeyboardColor.NEGATIVE, payload={"type": "info_faculty"})

    return keyboard2

# Назад в любом блоке
def backKbr(lang, back):
    btn_name = btn[lang]

    keyboard = VkKeyboard(**settings)
    keyboard.add_callback_button(label=btn_name['back'], color=VkKeyboardColor.NEGATIVE,
                                 payload={'type': back})
    return keyboard

# Закрыть клавиатуру
def create_empty_keyboard():
    keyboard = VkKeyboard.get_empty_keyboard()
    return keyboard