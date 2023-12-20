import sqlite3 as sq

from create_bot import bot


def sql_start():
    global base, cur
    base = sq.connect('quizbot.db')
    cur = base.cursor()
    if base:
        print('База данных успешно подключена')
        base.execute('CREATE TABLE IF NOT EXISTS User_list(user_id int, user_balance int)')
        base.commit()
        base.execute(
            'CREATE TABLE IF NOT EXISTS Games_list(photo text, name text, description text, solve text, id int not null)')
        # description text -  задание на игру, которое будет вызываться после входа юзера в чат
        # solve text - ответ на задание на игру, которое будет вызываться после вывода description text
        base.commit()
        base.execute(
            'CREATE TABLE IF NOT EXISTS Games_types(id int not null, type text, price int,  time int)')
        base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO User_list VALUES(?, ?)', tuple(data.values(), ))
        base.commit()


async def sql_add_command2(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO Games_list VALUES(?, ?, ?, ?, ?)', tuple(data.values(), ))
        base.commit()


async def sql_add_command3(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO Games_types VALUES(?, ?, ?, ?)',
                    (data['id'], data['type'], data['price'], data['time'],))
        base.commit()


async def sql_select_command(message):
    for ret in cur.execute('SELECT * FROM User_list ').fetchall():
        await bot.send_message(message.from_user.id, ret[0], ret[1])


async def sql_select_command2(state):
    async with state.proxy() as data:
        return cur.execute('SELECT type, price FROM Games_types WHERE type = ?', tuple(data))


async def sql_select_command3(huy):
    return cur.execute('SELECT price FROM Games_types WHERE type == ' + '"' + str(huy) + '"')


async def sql_select_command4(state):
    async with state.proxy() as data:
        return cur.execute('SELECT type FROM Games_types', data)


async def sql_select_command6(message):
    for ret in cur.execute('SELECT type FROM Games_types').fetchall():
        # await bot.send_message(message.chat.id,'Выберите тип игры, который хотите оплатить:')
        await message.answer(f'{ret[0]}\r\n ')


async def sql_select_command5(message):
    for ret in cur.execute('SELECT * FROM Games_list').fetchall():
        await bot.send_message(message.chat.id, ret[0], f'{ret[1]} {ret[2]}')


async def sql_select_command10():
    return cur.execute('SELECT Games_types.type FROM Games_types')


async def sql_select_command7(sex):
    return cur.execute(
            'SELECT description, solve FROM Games_list, Games_types WHERE Games_list.id == Games_types.id and '
            'Games_types.type == ' + '"' + str(sex) + '"')
            #await bot.send_message(chat_id='-1001781599983', text=ret[0]+'\n на ответ у вас есть 30 секунд')


async def sql_select_command8(check):
    return cur.execute(
        'SELECT Games_list.solve FROM Games_list, Games_types WHERE Games_list.id == Games_types.id and Games_types.type == ' + '"' + str(
            check) + '"')


async def sql_read(message):
    for ret in cur.execute('SELECT * FROM Games_list').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n {ret[2]}')


async def sql_read2():
    return cur.execute('SELECT * FROM Games_list').fetchall()


async def sql_read3(state):
    async with state.proxy() as data:
        return cur.execute('SELECT * FROM Games_types WHERE game_type = ?;', (data,))


async def sql_delete_command(data):
    cur.execute('''DELETE FROM Games_list WHERE name = ?;''', (data,))
    base.commit()
    print('Удалено')


async def sql_read4(message):
    return cur.execute('SELECT Games_types.type FROM Games_types WHERE Games_types.type == "' + message.text + '"')
