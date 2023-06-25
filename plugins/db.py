import sqlite3


def ensure_connection(func):
    """ Декоратор для подключения к СУБД: открывает соединение,
        выполняет переданную функцию и закрывает за собой соединение.
        Потокобезопасно!
    """
    def inner(*args, **kwargs):
        with sqlite3.connect('VKBot.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, force_table: bool = False, force_schedule: bool = False, force_date: bool = False, force_news: bool = False):
    """ Проверить что нужные таблицы существуют, иначе создать их

        Важно: миграции на такие таблицы вы должны производить самостоятельно!

        :param conn: подключение к СУБД
        :param force: явно пересоздать все таблицы
    """
    c = conn.cursor()

    # Информация о пользователе
    # TODO: создать при необходимости...

    # Сообщения от пользователей
    if force_table:
        c.execute('DROP TABLE IF EXISTS accounts')
    if force_schedule:
        c.execute('DROP TABLE IF EXISTS schedule')
    if force_date:
        c.execute('DROP TABLE IF EXISTS num_week')
        c.execute('DROP TABLE IF EXISTS getweek')
    if force_news:
        c.execute('DROP TABLE IF EXISTS news')

    c.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id          INTEGER PRIMARY KEY,
                uid         INTEGER NOT NULL,
                admin       INTEGER NOT NULL DEFAULT 0,
                ban         INTEGER NOT NULL DEFAULT 0,
                balance     INTEGER NOT NULL DEFAULT 500,
                uname        TEXT
            )
    ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS schedule (
                id          INTEGER PRIMARY KEY,
                group_num   INTEGER NOT NULL,
                group_sec   INTEGER,
                days        TEXT NOT NULL,
                week        TEXT,
                predmet_num INTEGER NOT NULL,
                timeline    TEXT,
                audit       TEXT,
                predmet     TEXT NOT NULL
            )
        ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS getweek (
                id          INTEGER PRIMARY KEY,
                mydate      TEXT
            )
    ''')

    c.execute('''
                CREATE TABLE IF NOT EXISTS num_week (
                    id          INTEGER PRIMARY KEY,
                    num         INTEGER NOT NULL,
                    week        TEXT,
                    month_name  TEXT
                )
        ''')

    c.execute('''
                CREATE TABLE IF NOT EXISTS news (
                id              INTEGER PRIMARY KEY,
                title           TEXT NOT NULL,
                text            TEXT NOT NULL,
                footer          TEXT NOT NULL,
                comments        TEXT NOT NULL
                )
    ''')

    c.execute('''
                    CREATE TABLE IF NOT EXISTS quotationskubsu (
                    id              INTEGER PRIMARY KEY,
                    text            TEXT NOT NULL,
                    name_prepod     TEXT NOT NULL,
                    predmet         TEXT NOT NULL,
                    faculty         TEXT NOT NULL
                    )
        ''')

    # c.execute('''
    #             CREATE TABLE IF NOT EXISTS profiles
    # ''')

    # Сохранить изменения
    conn.commit()


if __name__=='__main__':
    init_db(force_schedule=True)