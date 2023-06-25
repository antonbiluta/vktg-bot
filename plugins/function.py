from plugins.db import ensure_connection

@ensure_connection
def checkUser(peer_id, uname, conn):
    c = conn.cursor()
    c.execute(f'SELECT * FROM accounts WHERE uid = {peer_id}')
    try:
        if c.fetchone() is None:
            c.execute(f'INSERT INTO accounts(uid, uname) VALUES (?, ?)', (peer_id, uname,))
            conn.commit()
            c.execute(f'INSERT INTO skills(id_person) VALUES (?)', (peer_id,))
            conn.commit()
            c.execute(f'INSERT INTO ScheduleSpam(uid) VALUES (?)', (peer_id,))
            conn.commit()
            return True, 1
        else:
            return True, 2
    except:
        return False


@ensure_connection
def getFacInfo(fac, conn):
    c = conn.cursor()
    c.execute(f'SELECT info FROM faculties WHERE fac = "{fac}"')
    try:
        (zapros, ) = c.fetchone()
        return zapros
    except:
        pass


@ensure_connection
def getListUser(block, conn):
    c = conn.cursor()
    c.execute(f'SELECT uid FROM ScheduleSpam WHERE {block} = 1')
    if c.fetchone is None:
        pass
    else:
        return c.fetchone()


@ensure_connection
def register(conn, user_id, uname):
    c = conn.cursor()
    c.execute(f"SELECT * FROM accounts WHERE uid={user_id}")

    if c.fetchone() is None:
        c.execute(f'INSERT INTO accounts(uid, uname) VALUES (?, ?)', (user_id, uname,))
        conn.commit()
        c.execute(f'INSERT INTO skills(id_person) VALUES (?)', (user_id,))
        conn.commit()
        c.execute(f'INSERT INTO ScheduleSpam(uid) VALUES (?)', (user_id,))
        conn.commit()
        return 'Вы успешно зарегистрировались!'
    else:
        return 'Вы уже зарегистрированы!'

@ensure_connection
def registerGroup(conn, peer_id, uname):
    c = conn.cursor()
    c.execute(f"SELECT * FROM accounts WHERE uid={peer_id}")
    if c.fetchone() is None:
        c.execute(f'INSERT INTO accounts(uid, uname) VALUES (?, ?)', (peer_id, uname,))
        conn.commit()
        return True
    else:
        return False

@ensure_connection
def setLang(conn, user_id, lang):
    c = conn.cursor()
    c.execute(f"UPDATE accounts SET lang = '{lang}' WHERE uid = {user_id}")
    return True

@ensure_connection
def checkLang(conn, user_id):
    c = conn.cursor()
    c.execute(f'SELECT lang FROM accounts WHERE uid = {user_id}')
    if c.fetchone is None:
        return 'en-GB'
    else:
        (lang, ) = c.fetchone()
        return lang


@ensure_connection
def checkAgree(conn, user_id):
    c = conn.cursor()
    c.execute(f'SELECT agree FROM accounts WHERE uid = {user_id}')
    if c.fetchone is None:
        return False
    else:
        (answer,) = c.fetchone()
        if answer == 1:
            return True
        else:
            return False


@ensure_connection
def setAgree(conn, user_id, status):
    c = conn.cursor()
    c.execute(f"UPDATE accounts SET agree = '{status}' WHERE uid = {user_id}")
    return True


@ensure_connection
def getMassiv(conn, char):
    c = conn.cursor()

    if char is None:
        func = '>'
        default = 0

    else:
        func = f'{char}'
        default = 2000000000

    pers = c.execute(f'SELECT uid FROM accounts WHERE uid {func}{default}')

    mas = []
    for block in pers:
        for x in block:
            mas.append(x)

    return mas

@ensure_connection
def checkReg(conn, peer_id):
    c = conn.cursor()
    c.execute(f'SELECT * FROM accounts WHERE uid={peer_id}')
    if c.fetchone() is None:
        return False
    else:
        return True


@ensure_connection
def getAllRasp(conn, group: int, pod_group: None, day: str, week: str):
    c = conn.cursor()
    if pod_group is None:
        c.execute(
            f"SELECT predmet_num, timeline, predmet, audit FROM schedule WHERE group_num='{group}' AND days='{day}' AND (week='{week}' OR week IS NULL) ORDER BY predmet_num")
    else:
        c.execute(f"SELECT predmet_num, timeline, predmet, audit FROM schedule WHERE group_num='{group}' AND (group_sec='{pod_group}' OR group_sec=0) AND days='{day}' AND (week='{week}' OR week IS NULL) ORDER BY predmet_num")
    return c.fetchall()

@ensure_connection
def getNews(conn):
    c = conn.cursor()
    c.execute(f"SELECT title, text, footer, comments FROM news ORDER BY id DESC LIMIT 1")
    return c.fetchall()

@ensure_connection
def getWeek(conn, new_date):
    c = conn.cursor()
    c.execute(f'INSERT INTO getweek (mydate) VALUES (?)', (new_date,))
    c.execute(f"SELECT *, strftime('%W',mydate) AS weekofyear FROM getweek ORDER BY id DESC LIMIT 1")
    (var1, var2, number) = c.fetchone()
    c.execute(f"SELECT week FROM num_week WHERE num={number}")
    (result,) = c.fetchone()
    return result

@ensure_connection
def getIds(conn):
    c = conn.cursor()
    c.execute(f'SELECT uid, uname FROM accounts')
    return c.fetchall()

@ensure_connection
def getDay(conn, day):
    c = conn.cursor()
    c.execute(f"SELECT * FROM schedule WHERE days={day}")
    return c.fetchall()

@ensure_connection
def check_adm(conn, peer_id, lvl):
    c = conn.cursor()
    c.execute(f"SELECT * FROM accounts WHERE uid = '{peer_id}'")
    if c.fetchone() is None:
        return "Вам следует пройти регистрацию."
    else:
        c.execute(f"SELECT admin FROM accounts WHERE uid = {peer_id}")
        (admin, ) = c.fetchone()
        if admin >= lvl:
            return True
        else:
            return False

@ensure_connection
def checkGroup(conn, peer_id):
    try:
        if peer_id >= 2000000000:
            return True
        else:
            return False
    except:
        return False

@ensure_connection
def check_lvl_user(conn, peer_id):
    c = conn.cursor()
    c.execute(f'SELECT status FROM accounts WHERE uid = {peer_id}')
    (status,) = c.fetchone()
    # elem = []
    # if lvl == 1000:
    #     elem.append('Разработчик')
    #     elem.append('Серый кардинал актива')
    #     elem.append('Итальянский армянин проживающий в России')
    # if lvl == 100:
    #     elem.append('Разработчик')
    # if lvl == 90:
    #     elem.append('Тестировщик')
    # elif lvl == 80:
    #     elem.append('Администратор')
    # elif lvl == 32:
    #     elem.append('Председатель Студсовета')
    # elif lvl == 31:
    #     elem.append('Председатель Профбюро')
    # elif lvl == 30:
    #     elem.append('Активист')
    #
    # elif lvl == 11:
    #     elem.append('Профорг')
    # elif lvl == 10:
    #     elem.append('Староста')
    #
    # elif lvl == 0:
    #     elem.append('Студент')
    # status = ' | '.join(elem)
    return status


@ensure_connection
def add_status(conn, peer_id, new_status):
    c = conn.cursor()
    c.execute(f'SELECT status FROM accounts WHERE uid = {peer_id}')
    (status,)=c.fetchone()
    status = f'{status} | {new_status}'
    c.execute(f"UPDATE accounts SET status = '{status}' WHERE uid = {peer_id}")
    conn.commit()
    return True


@ensure_connection
def getHoros(conn, title):
    c = conn.cursor()
    c.execute(f'SELECT title, text, link_picture FROM horoscope WHERE title = "{title}"')
    return c.fetchone()

@ensure_connection
def checkName(conn, peer_id, title):
    c = conn.cursor()
    c.execute(f"SELECT uname FROM accounts WHERE uid={peer_id}")
    try:
        (name, ) = c.fetchone()
        if name != title:
            c.execute(f"UPDATE accounts SET uname = '{title}' WHERE uid = {peer_id}")
            conn.commit()
            return True
        else:
            return False
    except:
        return False


@ensure_connection
def getQuotation(conn):
    c = conn.cursor()
    c.execute(f"SELECT text, name_prepod, predmet, faculty FROM quotationskubsu ORDER BY RANDOM() LIMIT 1")
    return c.fetchall()




#Задачи
@ensure_connection
def setTask(conn, id_chat, task):
    c = conn.cursor()
    num = getNumTask(id_chat=id_chat)
    num = int(num) + 1
    c.execute(f'INSERT INTO task_list(id_chat, num, task) VALUES (?,?,?)', (id_chat, num, task,))
    conn.commit()
    return True

@ensure_connection
def getNumTask(conn, id_chat):
    c = conn.cursor()
    c.execute(f'SELECT num FROM task_list WHERE id_chat = {id_chat} ORDER BY id_task DESC LIMIT 1')
    try:
        (num,) = c.fetchone()
    except:
        num = 0
    return num

@ensure_connection
def updateTask(conn, id_chat):
    c = conn.cursor()
    new_num = 1
    c.execute(f'SELECT num FROM task_list WHERE id_chat = {id_chat}')
    for nums in c.fetchall():
        (num,) = nums
        if num != new_num:
            c.execute(f"UPDATE task_list SET num = '{new_num}' WHERE id_chat = {id_chat} AND num={num}")
        new_num+=1
    return True

@ensure_connection
def getTasks(conn, id_chat):
    c = conn.cursor()
    c.execute(f'SELECT num, task, status FROM task_list WHERE id_chat={id_chat}')
    return c.fetchall()

@ensure_connection
def delTask(conn, id_chat, num):
    c = conn.cursor()
    c.execute(f'DELETE FROM task_list WHERE id_chat={id_chat} AND num = {num}')
    return True

@ensure_connection
def editTask(conn, id_chat, num, new_task):
    c = conn.cursor()
    c.execute(f"UPDATE task_list SET task = '{new_task}' WHERE id_chat = {id_chat} AND num={num}")
    conn.commit()
    return True

@ensure_connection
def comTask(conn, id_chat, num):
    c = conn.cursor()
    c.execute(f"UPDATE task_list SET status = '✅' WHERE id_chat = {id_chat} AND num={num}")
    conn.commit()
    return True

@ensure_connection
def uncomTask(conn, id_chat, num):
    c = conn.cursor()
    c.execute(f"UPDATE task_list SET status = '❌' WHERE id_chat = {id_chat} AND num={num}")
    conn.commit()
    return True



# Напоминания
@ensure_connection
def setNotice(conn, id_chat, timeline, notic):
    c = conn.cursor()
    c.execute(f'INSERT INTO notification (id_chat, timeline, notice) VALUES (?,?,?)', (id_chat, timeline, notic,))
    conn.commit()

@ensure_connection
def getNotice(conn, timeline):
    c = conn.cursor()
    c.execute(f"SELECT id_chat, notice FROM notification WHERE timeline='{timeline}'")
    return c.fetchone()

@ensure_connection
def delNotice(conn, id_chat, notice):
    c = conn.cursor()
    c.execute(f'DELETE FROM notification WHERE id_chat={id_chat} AND notice="{notice}"')
    conn.commit()




@ensure_connection
def check_lvl(conn, peer_id):
    c = conn.cursor()
    try:
        c.execute(f'SELECT admin FROM accounts WHERE uid = {peer_id}')
        (lvl,) = c.fetchone()
        return lvl
    except:
        return 0


def retLvl(s):
    if s == "SuperAdmin":
        return 1000
    if s == "VkTester":
        return 90
    if s == "ActiveStudent":
        return 30
    if s == "Starosta":
        return 10
    if s == "Student":
        return 1
    if s == "User":
        return 0



@ensure_connection
def getCom(conn, cmd, peer_id):
    c = conn.cursor()

    lvl = check_lvl(peer_id=peer_id)

    try:
        c.execute(f'SELECT answer, lvl FROM commands WHERE command LIKE "%{cmd}%"')
        (text,levl) = c.fetchone()
        num_lvl=retLvl(s=levl)
        if lvl>=num_lvl:
            return text
    except:
        return "Я не знаю, что тебе ответить("

@ensure_connection
def getComList(conn):
    c = conn.cursor()
    c.execute(f'SELECT command FROM commands')
    return c.fetchall()