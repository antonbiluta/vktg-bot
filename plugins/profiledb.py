from plugins.db import ensure_connection

@ensure_connection
def checkUser(conn, uid):
    c = conn.cursor()
    try:
        c.execute(f'SELECT * FROM profiles WHERE vk_id={uid}')
        if c.fetchone() is None:
            return False
        else:
            return True
    except:
        return False

@ensure_connection
def register(conn, uid, name, status):
    c = conn.cursor()
    c.execute(f'INSERT INTO profiles(vk_id, name, status) VALUES (?, ?, ?)', (uid, name, status,))
    conn.commit()
    return True

@ensure_connection
def editName(conn, uid, name):
    c = conn.cursor()
    c.execute(f'UPDATE profiles SET name ="{name}" WHERE vk_id={uid}')
    conn.commit()
    return True

@ensure_connection
def editPhoto(conn, uid, photo):
    c = conn.cursor()
    c.execute(f'UPDATE profiles SET photo = "{photo}" WHERE vk_id={uid}')
    conn.commit()
    return True

@ensure_connection
def getData(conn, uid):
    c = conn.cursor()
    c.execute(f'SELECT * FROM profiles WHERE vk_id={uid}')
    (id_k, vk_id, tg_id, name, faculty, short_info, more_info, lang, status, photo) = c.fetchone()
    return {"name": name,
            "points": "1255",
            "short_mes": short_info,
            "faculty": faculty,
            "lang": lang,
            "info": more_info,
            "link_avatar": photo,
            "status": status
            }