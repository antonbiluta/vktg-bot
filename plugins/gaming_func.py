from plugins.db import ensure_connection
import random

@ensure_connection
def check_balance(conn, peer_id):
    c = conn.cursor()
    c.execute(f"SELECT balance FROM accounts WHERE uid = {peer_id}")
    (balance,) = c.fetchone()
    return balance

@ensure_connection
def buy_item(conn, peer_id, need_money, item):
    c = conn.cursor()
    money = check_balance(peer_id=peer_id)
    if money < need_money:
        need = need_money - money
        return f'У вас недостаточно средств. Нужно еще {need} СтудКоинов.'
    else:
        addItem(peer_id=peer_id, item=item)
        money2 = money - need_money
        c.execute(f"UPDATE accounts SET balance = '{money2}' WHERE uid='{peer_id}'")
        c.execute(f"SELECT balance FROM accounts WHERE uid = {peer_id}")
        (balance,) = c.fetchone()
        return f'Вы купили предмет "{item}" за {need_money} СтудКоинов.' \
               f'\n💳 Счет: {balance} СК.'

@ensure_connection
def lootGift(conn, from_id, need_money):
    c = conn.cursor()
    money = check_balance(peer_id=from_id)
    if money < need_money:
        need = need_money - money
        return f'У вас недостаточно средств. Нужно еще {need} СтудКоинов.'
    else:
        money2 = money - need_money
        c.execute(f"UPDATE accounts SET balance = '{money2}' WHERE uid='{from_id}'")
        conn.commit()

        if need_money == 100:
            one = 0.99
            two = 0.25
            three = 0.25
            four = 0.25
            five = 0.0001
            six = 0.00001
        if need_money == 5000:
            one = 0.8
            two = 0.3
            three = 0.3
            four = 0.3
            five = 0.001
            six = 0.0001

        if need_money == 10000:
            one = 0.7
            two = 0.35
            three = 0.35
            four = 0.35
            five = 0.005
            six = 0.0002


        items = [
            {
                'name': 'СтудКоин',
                'dropChance': one
            },
            {
                'name': 'акции компании "Ля Костя"',
                'dropChance': two
            },
            {
                'name': 'Книга "ЭЛЕМЕНТЫ ДИСКРЕТНОЙ МАТЕМАТИКИ" К.И. Костенко',
                'dropChance': three
            },
            {
                'name': 'Скидка 5% на место в очереди буфета',
                'dropChance': four
            },
            {
                'name': 'Джекпот',
                'dropChance': five
            },
            {
                'name': 'Мозг Гения',
                'dropChance': six
            },
        ]


        import functools

        def drop():
            total = functools.reduce(lambda accumulator, item: accumulator + float(item['dropChance']), items, 0)
            chance = random.uniform(0, float(total))
            current = 0
            for item in items:
                if (current <= chance and chance < (current + float(item['dropChance']))):
                    return item['name']
                current += float(item['dropChance'])

        win_item = drop()

        if win_item == 'СтудКоин':
            range_num = random.randint(1, 40)
            if range_num < 30:
                item_win = random.randint(600, 4999)
            elif range_num>=30 and range_num<37:
                item_win = random.randint(5000, 9999)
            else:
                item_win = random.randint(10000, 35000)
            addBalance(peer_id=from_id, balance_new=item_win)
            return f'Награда {item_win} sc' \
            f'\n💳 Счет: {check_balance(peer_id=from_id)} sc'
        elif win_item == 'Джекпот':
            addBalance(peer_id=from_id, balance_new=10000)
            return f'Награда джекпот!' \
                   f'\n💳 Счет: {check_balance(peer_id=from_id)} sc'
        else:
            return f'Награда {win_item}'

@ensure_connection
def addBalance(conn, peer_id, balance_new):
    c = conn.cursor()
    c.execute(f"SELECT balance FROM accounts WHERE uid = {peer_id}")
    (balance,) = c.fetchone()
    balance = balance + balance_new
    c.execute(f"UPDATE accounts SET balance = '{balance}' WHERE uid='{peer_id}'")
    conn.commit()
    return 'Баланс пополнен'

@ensure_connection
def getRaiting(conn):
    c = conn.cursor()
    c.execute(f"SELECT uname, balance FROM accounts ORDER BY balance DESC")
    return c.fetchall()

@ensure_connection
def addItem(conn, peer_id, item):
    c = conn.cursor()
    c.execute(f'INSERT INTO inventory(id_person, item) VALUES (?, ?)', (peer_id, item,))
    conn.commit()
    return True

@ensure_connection
def getInv(conn, peer_id):
    c = conn.cursor()
    c.execute(f'SELECT item FROM inventory WHERE id_person = {peer_id}')
    return c.fetchall()

@ensure_connection
def getSkills(conn, peer_id):
    c = conn.cursor()
    c.execute(f'SELECT health, intelligence, dexterity, wisdom, luck FROM skills WHERE id_person = {peer_id}')
    return c.fetchall()
