import telebot
import sqlite3
from telebot import types
bot=telebot.TeleBot('6150214692:AAHXDgVxVvBL9phQ_UhEeUY485D5Ibs_4R4')
name=""
ID=""
def main_panel():
    connection=sqlite3.connect("db.sql")
    cursor=connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS user(id int auto_increment primary_key, name varchar(50), password varchar(50))')
    connection.commit()
    cursor.close()
    connection.close()
    menu=types.InlineKeyboardMarkup(row_width=3)
    review=types.InlineKeyboardButton('Посмотреть',callback_data='menu1:review')
    add=types.InlineKeyboardButton('Добавить в Базу',callback_data='menu1:add')
    delete=types.InlineKeyboardButton('Удалить',callback_data='menu1:delete')
    menu.add(review,add,delete)
    return menu
@bot.message_handler(commands=['start'])
def start(message):
    menu=main_panel()
    bot.send_message(message.chat.id,f'<em>Здравствуйте <b>{message.from_user.first_name} {message.from_user.last_name}</b> 🙂\nВыберите действие</em>',reply_markup=menu,parse_mode='html')
@bot.callback_query_handler(func=lambda call: call.data.split(':')[0]=='menu1')
def choice(call):
    if call.data.split(':')[1]=='review':
        menu=types.InlineKeyboardMarkup(row_width=2)
        name=types.InlineKeyboardButton('По имени',callback_data='menu2:name')
        entire=types.InlineKeyboardButton('Всех',callback_data='menu2:all')
        menu.add(name,entire)
        bot.send_message(call.message.chat.id,'Выберите по критерию',reply_markup=menu)
    elif call.data.split(':')[1]=='delete':
        menu=types.InlineKeyboardMarkup(row_width=2)
        name=types.InlineKeyboardButton('По имени',callback_data='menu3:name')
        entire=types.InlineKeyboardButton('Всех',callback_data='menu3:all')
        menu.add(name,entire)
        bot.send_message(call.message.chat.id,'Выберите по критерию',reply_markup=menu)
    else:
        bot.send_message(call.message.chat.id,'<em>Напишите имя</em>',parse_mode='html')
        bot.register_next_step_handler(call.message,adding)
def adding(message):
    global name
    name=message.text.strip().lower()
    if len(name)<3:
        bot.send_message(message.chat.id,'<em>Слишком короткое имя 🙁 Напишите имя</em?',parse_mode='html')
        bot.register_next_step_handler(message,adding)
    else:
        bot.send_message(message.chat.id,'<em>Напишите пароль</em>',parse_mode='html')
        bot.register_next_step_handler(message,addition)
def addition(message):
    password=message.text
    connection=sqlite3.connect('db.sql')
    cursor=connection.cursor()
    cursor.execute('INSERT INTO user (name, password) VALUES ("%s","%s")' % (name,password))
    connection.commit()
    cursor.close()
    connection.close()
    bot.send_message(message.chat.id,'<b>Добавлено</b> 🙂\n\n',parse_mode='html')
    menu=main_panel()
    bot.send_message(message.chat.id,'Выберите действие',reply_markup=menu)
@bot.callback_query_handler(func=lambda call: call.data.split(':')[0]=='menu2')
def show(call):
    if call.data.split(':')[1]=='name':
        bot.send_message(call.message.chat.id,'<em>Напишите имя</em>',parse_mode='html')
        bot.register_next_step_handler(call.message,show_by_name)
    else:
        connection=sqlite3.connect('db.sql')
        cursor=connection.cursor()
        cursor.execute('SELECT * FROM user')
        values=cursor.fetchall()
        cursor.close()
        connection.close()
        if len(values)>0:
            data=''
            for e in values:
                data+=f'имя: {e[1]}, пароль: {e[2]}\n'
            bot.send_message(call.message.chat.id,f'<b>{data}</b>\n\n',parse_mode='html')
        else:
            bot.send_message(call.message.chat.id,f'<b>База пуста</b>\n\n',parse_mode='html')
        menu=main_panel()
        bot.send_message(call.message.chat.id,'Выберите действие',reply_markup=menu)
def show_by_name(message):
    global name
    name=message.text.lower()
    connection=sqlite3.connect('db.sql')
    cursor=connection.cursor()
    cursor.execute('SELECT * FROM user WHERE name=("%s")' % (name))
    values=cursor.fetchall()
    cursor.close()
    connection.close()
    if len(values)>0:
        data=''
        for e in values:
            data+=f'имя: {e[1]}, пароль: {e[2]}\n'
        bot.send_message(message.chat.id,f'<b>{data}</b>\n\n',parse_mode='html')
    else:
        bot.send_message(message.chat.id,f'<b>Нет записей с таким именем</b>\n\n',parse_mode='html')
    menu=main_panel()
    bot.send_message(message.chat.id,'Выберите действие',reply_markup=menu)
@bot.callback_query_handler(func=lambda call: call.data.split(':')[0]=='menu3')
def deleting(call):
    if call.data.split(':')[1]=='name':
        bot.send_message(call.message.chat.id,'<em>Напишите имя</em>',parse_mode='html')
        bot.register_next_step_handler(call.message,del_by_name)
    else:
        connection=sqlite3.connect('db.sql')
        cursor=connection.cursor()
        cursor.execute('DELETE FROM user')
        connection.commit()
        cursor.close()
        connection.close()
        bot.send_message(call.message.chat.id,f'<b>Удалено\n\n</b>',parse_mode='html')
        menu=main_panel()
        bot.send_message(call.message.chat.id,'Выберите действие',reply_markup=menu)
def del_by_name(message):
    global name
    name=message.text.lower()
    connection=sqlite3.connect('db.sql')
    cursor=connection.cursor()
    cursor.execute('DELETE FROM user WHERE name=("%s")' % (name))
    connection.commit()
    cursor.close()
    connection.close()
    bot.send_message(message.chat.id,f'<b>Удалено\n\n</b>',parse_mode='html')
    menu=main_panel()
    bot.send_message(message.chat.id,'Выберите действие',reply_markup=menu)
bot.polling(none_stop=True)