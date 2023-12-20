from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from create_bot import bot, dp
from aiogram import Bot
from aiogram import Dispatcher, types
from database import database_conn


class FSMAdmin(StatesGroup):
    type = State()
    solve = State()



        #print(y)




    '''if y == user_solut and message.chat.id == -1001781599983:
        print('yes')
        await bot.send_message(chat_id='-1001781599983', text='правильный ответ')
        await message.reply(text='вы победили, вы можете вывести деньги по кнопке /Вывести')
    else:
        print('no')
        await bot.send_message(chat_id='-1001781599983', text='неверно')'''
# chat_id = '-1001781599983'
# text='Правила такие-то'
# MethodSendToGroup = 'https://api.telegram.org/bot5655918097:AAGoOiVHZsbQdTfk0fUW798szIfMZV9kJ7s/sendMessage?chat_id=-1001781599983&text=lol'.format(
# token='5655918097:AAGoOiVHZsbQdTfk0fUW798szIfMZV9kJ7s')
# while True:
# response = requests.post(MethodSendToGroup)
# result = response.json()
# print(result)
