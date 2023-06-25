import codecs
import subprocess
import os

root_path = os.path.dirname(__file__)

def get_path(path='bin', sep=os.sep):
    return root_path + sep + path

def create_image(template=0, data={}):
    prepare_html(template, data)

    cmd = " ".join([
        get_path("bin\wkhtmltoimage.exe"),
        " --width 597"
        " --enable-local-file-access",
        "-q",
        get_path("templates\prepared.html"),
        get_path("data\profile.jpg"),
    ])
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    process.wait()
    return process

def prepare_html(template, data):
    """
    Передаю текст который нужно написать на картинке
    и выбираю шаблон с которым работать
    сохраняю в итоговый html, кот. потом буду конвертить в картинку
    :param template:
    :param data:
    :return:
    """
    with codecs.open(get_path(f"templates/profile.html"), 'r', 'utf-8') as f:
        t = f.read()
        t = t.replace('{root_path}', get_path('').replace('\\','/'))
        t = t.replace('{name}', data.get('name', 'Имя Фамилия'))
        t = t.replace('{points}', data.get('points', '4269'))
        t = t.replace('{short_mes}', data.get('short_mes', 'Короткое сообщение для всех'))
        t = t.replace('{faculty}', data.get('faculty', 'Факультет кринжа и кековых наук'))
        t = t.replace('{lang}', data.get('lang', 'Эльфийский'))
        t = t.replace('{info}', data.get('info', 'Чти меня'))
        t = t.replace('{status}', data.get('status', 'Ожидается'))
        t = t.replace('{link_avatar}', data.get('link_avatar', 'https://sun9-79.userapi.com/impg/BshZnHqYdKE1hu3oJ5PT0mh0XrML1SkaBGAc7g/IgCeFlpajrs.jpg?size=864x1080&quality=96&sign=7f5c2a401be3dd0987b3bb0d07ca166d&type=album'))

        with codecs.open(get_path(f"templates/prepared.html"), 'w', 'utf-8') as f:
            f.write(t)