from plugins.db import ensure_connection

@ensure_connection
def start(conn, count_player, id_game, id_player, status):
    c = conn.cursor()

    c.execute(f'SELECT * FROM spygame WHERE id_player = {id_player}')
    if c.fetchone() is None:
        c.execute(f'INSERT INTO spygame(id_game, id_player, status, count_player) VALUES (?, ?, ?, ?)', (id_game, id_player, status, count_player,))
        conn.commit()
        return int(count_player) - 1
    else:
        return int(count_player)


@ensure_connection
def getVoice(conn, id_game, id_player):
    c = conn.cursor()

    c.execute(f'SELECT voices FROM spygame WHERE id_player = {id_player} AND id_game = {id_game}')
    (voice,) = c.fetchone()
    voices = int(voice) + 1
    c.execute(f"UPDATE spygame SET voices = '{voices}' WHERE id_game='{id_game}' AND id_player='{id_player}'")
    conn.commit()
    return voices

@ensure_connection
def kick(conn, id_game, id_player):
    c = conn.cursor()

    c.execute(f'DELETE FROM spygame WHERE id_game = {id_game} AND id_player = {id_player}')
    conn.commit()
    return True

@ensure_connection
def getCount(conn, id_game):
    c = conn.cursor()

    c.execute(f'SELECT count_player FROM spygame WHERE id_game={id_game}')
    (count,) = c.fetchone()
    return count

@ensure_connection
def random(conn, id_game):
    count = getCount(id_game=id_game)
    c = conn.cursor()
    c.execute(f'SELECT * FROM spygame WHERE id_game={id_game}')
    text = c.fetchall()

    print(count/(checkSpy(id_game=id_game)+1))

    while True:
        print(2)
        for block in text:
            if block[3] == 'person':
                import random
                rand = random.randint(1, count)
                if rand == 1:
                    c.execute(f"UPDATE spygame SET status = '{'spy'}' WHERE id_game='{id_game}' AND id_player='{block[2]}'")
                    conn.commit()
        if (count/(checkSpy(id_game=id_game)+1)>1 and count/(checkSpy(id_game=id_game)+1) <4):
            break

    return True

@ensure_connection
def checkSpy(conn, id_game):
    c = conn.cursor()

    c.execute(f'SELECT status FROM spygame WHERE id_game={id_game}')
    status = c.fetchall()

    spy_count = 0
    for block in status:
        for status in block:
            if status == 'spy':
                spy_count = +1


    return  spy_count

@ensure_connection
def getCountLocation(conn):
    c = conn.cursor()

    c.execute(f'SELECT id FROM location ORDER BY id DESC LIMIT 1 ')
    count = c.fetchone()
    return count

@ensure_connection
def location(conn):
    c = conn.cursor()

    c.execute(f'SELECT local_name FROM location')
    locals = c.fetchall()

    import random
    (count,) = getCountLocation()
    loc = random.randint(0, count)
    i = 0
    for block in locals:
        (local_cur, ) = block
        if i == loc:
            break
        i = i+1
    return local_cur

@ensure_connection
def getPerson(conn, id_game):
    c = conn.cursor()
    c.execute(f'SELECT * FROM spygame WHERE id_game={id_game}')
    status = c.fetchall()

    pers=[]
    for block in status:
        if block[3] == 'person':
            pers.append(block[2])

    return pers

@ensure_connection
def getSpy(conn, id_game):
    c = conn.cursor()
    c.execute(f'SELECT * FROM spygame WHERE id_game={id_game}')
    status = c.fetchall()

    spy=[]
    for block in status:
        if block[3] == 'person':
            spy.append(block[2])

    return spy

@ensure_connection
def getPlayers(conn, id_game):
    c = conn.cursor()
    c.execute(f'SELECT * FROM spygame WHERE id_game={id_game}')
    status = c.fetchall()

    player=[]
    for block in status:
        player.append(block[2])

    return player

@ensure_connection
def finish(conn, id_game):
    c = conn.cursor()
    c.execute(f'DELETE FROM spygame WHERE id_game = {id_game}')
    conn.commit()
    return 'Игра окончена.'