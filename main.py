import random
import sqlite3
from sqlite3 import Error
import telebot
from telebot import types
from aiogram import Bot, Dispatcher
from googletrans import Translator, constants
from pprint import pprint
import datetime


bot = telebot.TeleBot('5485448146:AAEbBQrsmJXeftqkjCGSW-zeW5YtaAqwMeE', parse_mode='HTML')

translator = Translator()

#date = str(datetime.date.today())

#d = date.replace('-', '')


def get_id(message):
    user_id = message.from_user.id
    return user_id


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path, check_same_thread=False)
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


path = 'words.sql'

connection = create_connection(path)

cursor = connection.cursor()


def execute_query(query):
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


def create_table(message, name):
    create_users_table = f"""
        CREATE TABLE IF NOT EXISTS {name} (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          english VARCHAR(100),
          russian VARCHAR(100)
        );
        """
    execute_query(create_users_table)


def counting(message):
    try:
        cursor.execute(f"SELECT id FROM count{get_id(message)}")
        count = cursor.fetchall()
        count = int(count[-1][-1])
        connection.commit()
        return count
    except Error as e:
        bot.send_message(message.chat.id, f"The error '{e}' occurred")
        start(message)


def translate_it(message):
    msg = bot.send_message(message.chat.id, 'Enter English word')
    bot.register_next_step_handler(msg, translate_it2)


def translate_it2(message):
    tr = translator.translate(message.text, dest='ru', src='en')
    msg = bot.send_message(message.chat.id, 'Here is the result')
    bot.send_message(message.chat.id, f"{tr.origin} ({tr.src}) --> {tr.text} ({tr.dest})")
    translate_it3(msg, tr.origin, tr.text)


def translate_it3(message, eng, rus):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Translate another word")
    item2 = types.KeyboardButton("Save this word")
    item3 = types.KeyboardButton("To main menu")
    markup.add(item1, item2, item3)
    msg = bot.send_message(message.chat.id, 'Do you want to repeat?', reply_markup=markup)
    bot.register_next_step_handler(msg, translate_it4, eng, rus)

def translate_it4(message, eng, rus):
    if message.text == 'Translate another word':
        translate_it(message)
    elif message.text == 'To main menu':
        start(message)
    elif message.text == 'Save this word':
        save_translated(message, eng, rus)
    else:
        bot.send_message(message.chat.id(message, 'Oops'))
        start(message)


def save_translated(message, eng, rus):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Restart")
    item2 = types.KeyboardButton("To main menu")
    markup.add(item1, item2)
    create_table(message, f'user{get_id(message)}')
    add = f"INSERT INTO user{get_id(message)} (english, russian) VALUES ('{eng}', '{rus}')"
    try:
        cursor.execute(add)
        connection.commit()
        msg = bot.send_message(message.chat.id, f"The pair added successfully", reply_markup=markup)
        translate_it3(msg, eng, rus)
    except Error as e:
        msg = bot.send_message(message.chat.id, f"The error '{e}' occurred")
        start(msg)


def show(message):
    try:
        bot.send_message(message.chat.id, "Here is your dictionary:")
        cursor.execute(f"SELECT english, russian FROM user{get_id(message)}")
        result = cursor.fetchall()
        for i in range(len(result)):
            bot.send_message(message.chat.id, ": ".join(result[i]))
        connection.commit()
        start(message)
    except Error as e:
        bot.send_message(message.chat.id, f"The error '{e}' occurred")
        start(message)


def delete(message):
    msg = bot.send_message(message.chat.id, 'What word do you want to delete?')
    bot.register_next_step_handler(msg, delete2)


def delete2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Restart")
    item2 = types.KeyboardButton("To main menu")
    markup.add(item1, item2)
    cursor = connection.cursor()
    key = message.text
    delete = f"DELETE FROM user{get_id(message)} WHERE english = '{key}' OR russian = '{key}'"
    try:
        cursor.execute(delete)
        connection.commit()
        msg = bot.send_message(message.chat.id, "The pair deleted successfully", reply_markup=markup)
        bot.register_next_step_handler(msg, repeat_delete)
    except Error as e:
        msg = bot.send_message(message.chat.id, f"The error '{e}' occurred", reply_markup=markup)
        bot.register_next_step_handler(msg, repeat_delete)


def repeat_delete(message):
    msg = message.text
    if msg == 'Restart':
        return delete(message)
    else:
        return start(message)


def add_eng(message):
    msg = bot.send_message(message.chat.id, 'Enter new word in English: ')
    key = message.text
    bot.register_next_step_handler(msg, add_rus, key)


def add_rus(message, key):
    msg = bot.send_message(message.chat.id, 'Enter new word in Russian: ')
    val = message.text
    bot.register_next_step_handler(msg, adding, key, val)


def adding(message, key, val):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Restart")
    item2 = types.KeyboardButton("To main menu")
    markup.add(item1, item2)
    add = f"INSERT INTO user{get_id(message)} (english, russian) VALUES ('{key}', '{val}')"
    try:
        cursor.execute(add)
        connection.commit()
        msg = bot.send_message(message.chat.id, f"The pair added successfully", reply_markup=markup)
        bot.register_next_step_handler(msg, repeat_add_word)
    except Error as e:
        msg = bot.send_message(message.chat.id, f"The error '{e}' occurred")
        bot.register_next_step_handler(msg, repeat_add_word)


def repeat_add_word(message):
    menu = message.text
    if menu == 'Restart':
        return add_eng(message)
    else:
        return start(message)


def _10aday(message):
    day_dict = [[x for x in range(2)] for y in range(10)]
    cursor.execute(f"SELECT english, russian FROM user{get_id(message)}")
    result = cursor.fetchall()
    for i in range(0, 10):
        temp = result[i]
        eng = str(temp[0])
        rus = str(temp[1])
        day_dict[i][0] = eng
        day_dict[i][1] = rus
        i += 1
    for i in range(0, 10):
        delete = f"DELETE FROM user{get_id(message)} WHERE english = '{day_dict[i][0]}'"
        cursor.execute(delete)
        i += 1
    connection.commit()
    learn_1st(message, day_dict)


def learn_1st(message, day_dict):
    try:
        create_users_table = f"""
                        CREATE TABLE IF NOT EXISTS count{get_id(message)} (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          count INT
                        );
                        """
        execute_query(create_users_table)
        cursor.execute(f"INSERT INTO count{get_id(message)} (count) VALUES ('first{datetime.datetime.today()}')")
        connection.commit()
    except Error as e:
        bot.send_message(message.chat.id, f"The error '{e}' occurred")
        start(message)
    bot.send_message(message.chat.id, "Here is words for training:")
    for i in range(0, 10):
        bot.send_message(message.chat.id, f'{day_dict[i][0]} - {day_dict[i][1]}')
    temp = day_dict.copy()
    first_day_dict = []
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('YES')
    markup.add(item1)
    bot.send_message(message.chat.id, "Are you ready?", reply_markup=markup)
    bot.register_next_step_handler(message, learn_1st_1, day_dict, temp, first_day_dict)

def learn_1st_1(message, day_dict, temp, first_day_dict):
    num = random.randint(0, len(day_dict) - 1)
    word = day_dict[num]
    rand = random.randint(1, 4)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if rand == 1:
        item1 = types.KeyboardButton(f'{word[1]}')
        item2 = types.KeyboardButton(f'{temp[random.randint(0, 9)][1]}')
        item3 = types.KeyboardButton(f'{temp[random.randint(0, 9)][1]}')
        item4 = types.KeyboardButton(f'{temp[random.randint(0, 9)][1]}')
    elif rand == 2:
        item1 = types.KeyboardButton(f'{temp[random.randint(0, 9)][1]}')
        item2 = types.KeyboardButton(f'{word[1]}')
        item3 = types.KeyboardButton(f'{temp[random.randint(0, 9)][1]}')
        item4 = types.KeyboardButton(f'{temp[random.randint(0, 9)][1]}')
    elif rand == 3:
        item1 = types.KeyboardButton(f'{temp[random.randint(0, 9)][1]}')
        item2 = types.KeyboardButton(f'{temp[random.randint(0, 9)][1]}')
        item3 = types.KeyboardButton(f'{word[1]}')
        item4 = types.KeyboardButton(f'{temp[random.randint(0, 9)][1]}')
    else:
        item1 = types.KeyboardButton(f'{temp[random.randint(0, 9)][1]}')
        item2 = types.KeyboardButton(f'{temp[random.randint(0, 9)][1]}')
        item3 = types.KeyboardButton(f'{temp[random.randint(0, 9)][1]}')
        item4 = types.KeyboardButton(f'{word[1]}')
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, f"Choose <b>{word[0]}</b> in Russian", reply_markup=markup)
    bot.register_next_step_handler(message, learn_1st_2, day_dict, temp, word, num, first_day_dict)


def learn_1st_2(message, day_dict, temp, word, num, first_day_dict):
    if message.text == word[1]:
        a = day_dict.pop(num)
        first_day_dict.append(a)
        bot.reply_to(message, 'Correct')
    else:
        bot.reply_to(message, 'Wrong')
        bot.send_message(message.chat.id, f'<b>{word[1]}</b> is correct')
    if day_dict == []:
        create_table(message, f'first{get_id(message)}')
        create_table(message, f'first_temp{get_id(message)}')
        if counting(message) % 2 == 1:
            try:
                for i in range(0, len(first_day_dict)):
                    add = f"INSERT INTO first{get_id(message)} (english, russian)\
                     VALUES ('{first_day_dict[i][0]}', '{first_day_dict[i][1]}')"
                    cursor.execute(add)
                    connection.commit()
            except Error as e:
                bot.send_message(message.chat.id, f"The error '{e}' occurred")
                start(message)
            learn_2nd(message, first_day_dict)
        else:
            try:
                for i in range(0, len(first_day_dict)):
                    add = f"INSERT INTO first_temp{get_id(message)} (english, russian)\
                     VALUES ('{first_day_dict[i][0]}', '{first_day_dict[i][1]}')"
                    cursor.execute(add)
                    connection.commit()
            except Error as e:
                bot.send_message(message.chat.id, f"The error '{e}' occurred")
                start(message)
            learn_2nd(message, first_day_dict)
    else:
        learn_1st_1(message, day_dict, temp, first_day_dict)


def learn_2nd(message, first_day_dict):
    if counting(message) % 2 == 1 and counting(message) != 1:
        try:
            bot.send_message(message.chat.id, "Here is words for training:")
            cursor.execute(f"SELECT english, russian FROM first_temp{get_id(message)}")
            first_day_dict = cursor.fetchall()
            cursor.execute(f"DROP TABLE first_temp{get_id(message)}")
            connection.commit()
        except Error as e:
            bot.send_message(message.chat.id, f"The error '{e}' occurred")
            start(message)
        for i in range(0, 10):
            bot.send_message(message.chat.id, f'{first_day_dict[i][0]} - {first_day_dict[i][1]}')
        second_day_dict = []
        temp = first_day_dict.copy()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('YES')
        markup.add(item1)
        bot.send_message(message.chat.id, "Are you ready?", reply_markup=markup)
        bot.register_next_step_handler(message, learn_2nd_1, second_day_dict, first_day_dict, temp)
    elif counting(message) % 2 != 1:
        try:
            bot.send_message(message.chat.id, "Here is words for training:")
            cursor.execute(f"SELECT english, russian FROM first{get_id(message)}")
            first_day_dict = cursor.fetchall()
            cursor.execute(f"DROP TABLE first{get_id(message)}")
            connection.commit()
        except Error as e:
            bot.send_message(message.chat.id, f"The error '{e}' occurred")
            start(message)
        for i in range(0, 10):
            bot.send_message(message.chat.id, f'{first_day_dict[i][0]} - {first_day_dict[i][1]}')
        second_day_dict = []
        temp = first_day_dict.copy()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('YES')
        markup.add(item1)
        bot.send_message(message.chat.id, "Are you ready?", reply_markup=markup)
        bot.register_next_step_handler(message, learn_2nd_1, second_day_dict, first_day_dict, temp)
    else:
        bot.send_message(message.chat.id, f"Great job! See you tomorrow")
        menu(message)


def learn_2nd_1(message, second_day_dict, first_day_dict, temp):
    num = random.randint(0, len(first_day_dict) - 1)
    word = first_day_dict[num]
    rand = random.randint(1, 4)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if rand == 1:
        item1 = types.KeyboardButton(f'{word[0]}')
        item2 = types.KeyboardButton(f'{temp[random.randint(0, 9)][0]}')
        item3 = types.KeyboardButton(f'{temp[random.randint(0, 9)][0]}')
        item4 = types.KeyboardButton(f'{temp[random.randint(0, 9)][0]}')
    elif rand == 2:
        item1 = types.KeyboardButton(f'{temp[random.randint(0, 9)][0]}')
        item2 = types.KeyboardButton(f'{word[0]}')
        item3 = types.KeyboardButton(f'{temp[random.randint(0, 9)][0]}')
        item4 = types.KeyboardButton(f'{temp[random.randint(0, 9)][0]}')
    elif rand == 3:
        item1 = types.KeyboardButton(f'{temp[random.randint(0, 9)][0]}')
        item2 = types.KeyboardButton(f'{temp[random.randint(0, 9)][0]}')
        item3 = types.KeyboardButton(f'{word[0]}')
        item4 = types.KeyboardButton(f'{temp[random.randint(0, 9)][0]}')
    else:
        item1 = types.KeyboardButton(f'{temp[random.randint(0, 9)][0]}')
        item2 = types.KeyboardButton(f'{temp[random.randint(0, 9)][0]}')
        item3 = types.KeyboardButton(f'{temp[random.randint(0, 9)][0]}')
        item4 = types.KeyboardButton(f'{word[0]}')
    markup.add(item1, item2, item3, item4)
    msg = bot.send_message(message.chat.id, f"Choose <b>{word[1]}</b> in English", reply_markup=markup)
    bot.register_next_step_handler(msg, learn_2nd_2, second_day_dict, first_day_dict, temp, word, num)


def learn_2nd_2(message, second_day_dict, first_day_dict, temp, word, num):
    if message.text == word[0]:
        a = first_day_dict.pop(num)
        second_day_dict.append(a)
        bot.reply_to(message, 'Correct')
    else:
        bot.reply_to(message, 'Wrong')
        bot.send_message(message.chat.id, f'<b>{word[0]}</b> is correct')
    if first_day_dict == []:
        create_table(message, f'second{get_id(message)}')
        create_table(message, f'second_temp{get_id(message)}')
        if counting(message) % 2 == 0:
            try:
                for i in range(0, len(second_day_dict)):
                    add = f"INSERT INTO second{get_id(message)} (english, russian)\
                                 VALUES ('{second_day_dict[i][0]}', '{second_day_dict[i][1]}')"
                    cursor.execute(add)
                    connection.commit()
            except Error as e:
                bot.send_message(message.chat.id, f"The error '{e}' occurred")
                start(message)
            learn_3rd(message)
        else:
            try:
                for i in range(0, len(second_day_dict)):
                    add = f"INSERT INTO second_temp{get_id(message)} (english, russian)\
                                 VALUES ('{second_day_dict[i][0]}', '{second_day_dict[i][1]}')"
                    cursor.execute(add)
                    connection.commit()
            except Error as e:
                bot.send_message(message.chat.id, f"The error '{e}' occurred")
                start(message)
            learn_3rd(message)
    else:
        learn_2nd_1(message, second_day_dict, first_day_dict, temp)


def learn_3rd(message):
    if counting(message) % 2 == 1:
        try:
            bot.send_message(message.chat.id, "Here is words for training:")
            cursor.execute(f"SELECT english, russian FROM second{get_id(message)}")
            second_day_dict = cursor.fetchall()
            cursor.execute(f"DROP TABLE second{get_id(message)}")
            connection.commit()
        except Error as e:
            bot.send_message(message.chat.id, f"The error '{e}' occurred")
            start(message)
        for i in range(0, 10):
            bot.send_message(message.chat.id, f'{second_day_dict[i][0]} - {second_day_dict[i][1]}')
        third_day_dict = []
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('YES')
        markup.add(item1)
        bot.send_message(message.chat.id, "Are you ready?", reply_markup=markup)
        bot.register_next_step_handler(message, learn_3rd_1, second_day_dict, third_day_dict)
    elif counting(message) % 2 != 1  and counting(message) != 2:
        try:
            bot.send_message(message.chat.id, "Here is words for training:")
            cursor.execute(f"SELECT english, russian FROM second_temp{get_id(message)}")
            second_day_dict = cursor.fetchall()
            cursor.execute(f"DROP TABLE second_temp{get_id(message)}")
            connection.commit()
        except Error as e:
            bot.send_message(message.chat.id, f"The error '{e}' occurred")
            start(message)
        for i in range(0, 10):
            bot.send_message(message.chat.id, f'{second_day_dict[i][0]} - {second_day_dict[i][1]}')
        third_day_dict = []
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('YES')
        markup.add(item1)
        bot.send_message(message.chat.id, "Are you ready?", reply_markup=markup)
        bot.register_next_step_handler(message, learn_3rd_1, second_day_dict, third_day_dict)
    else:
        bot.send_message(message.chat.id, f"Great job! See you tomorrow")
        menu(message)


def learn_3rd_1(message, second_day_dict, third_day_dict):
    telebot.types.ReplyKeyboardRemove()
    num = random.randint(0, len(second_day_dict) - 1)
    word, temp_word = second_day_dict[num]
    showed_word = []
    rep_word = list(word)
    for i in range(0, len(word)):
        letter = random.randint(0, len(word) - 1 - i)
        a = rep_word.pop(letter)
        showed_word.append(a)
    showed_word = ','.join(showed_word)
    bot.send_message(message.chat.id, f'Gather the word <b>{second_day_dict[num][1]}</b> from letters "{showed_word}"')
    bot.register_next_step_handler(message, learn_3rd_2, second_day_dict, third_day_dict, word, num)


def learn_3rd_2(message, second_day_dict, third_day_dict, word, num):
    if message.text == word:
        a = second_day_dict.pop(num)
        third_day_dict.append(a)
        bot.reply_to(message, 'Correct')
    else:
        bot.reply_to(message, 'Wrong')
        bot.send_message(message.chat.id, f'<b>{word}</b> is correct')
    if second_day_dict == []:
        create_table(message, f'third{get_id(message)}')
        create_table(message, f'third_temp{get_id(message)}')
        if counting(message) % 2 == 0:
            try:
                for i in range(0, len(third_day_dict)):
                    add = f"INSERT INTO third{get_id(message)} (english, russian)\
                                     VALUES ('{third_day_dict[i][0]}', '{third_day_dict[i][1]}')"
                    cursor.execute(add)
                    connection.commit()
            except Error as e:
                bot.send_message(message.chat.id, f"The error '{e}' occurred")
                start(message)
            learn_4th(message)
        else:
            try:
                for i in range(0, len(third_day_dict)):
                    add = f"INSERT INTO third_temp{get_id(message)} (english, russian)\
                                     VALUES ('{third_day_dict[i][0]}', '{third_day_dict[i][1]}')"
                    cursor.execute(add)
                    connection.commit()
            except Error as e:
                bot.send_message(message.chat.id, f"The error '{e}' occurred")
                start(message)
            learn_4th(message)
    else:
        learn_3rd_1(message, second_day_dict, third_day_dict)


def learn_4th(message):
    telebot.types.ReplyKeyboardRemove()
    if counting(message) % 2 == 0:
        try:
            bot.send_message(message.chat.id, "Here is words for training:")
            cursor.execute(f"SELECT english, russian FROM third_temp{get_id(message)}")
            third_day_dict = cursor.fetchall()
            cursor.execute(f"DROP TABLE third_temp{get_id(message)}")
        except Error as e:
            bot.send_message(message.chat.id, f"The error '{e}' occurred")
            start(message)
        for i in range(0, len(third_day_dict)):
            bot.send_message(message.chat.id, f'{third_day_dict[i][0]} - {third_day_dict[i][1]}')
        fourth_day_dict = []
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('YES')
        markup.add(item1)
        bot.send_message(message.chat.id, "Are you ready?", reply_markup=markup)
        bot.register_next_step_handler(message, learn_4th_1, third_day_dict, fourth_day_dict)
    elif counting(message) % 2 != 0 and counting(message) != 3:
        try:
            bot.send_message(message.chat.id, "Here is words for training:")
            cursor.execute(f"SELECT english, russian FROM third{get_id(message)}")
            third_day_dict = cursor.fetchall()
            cursor.execute(f"DROP TABLE third{get_id(message)}")
        except Error as e:
            bot.send_message(message.chat.id, f"The error '{e}' occurred")
            start(message)
        for i in range(0, len(third_day_dict)):
            bot.send_message(message.chat.id, f'{third_day_dict[i][0]} - {third_day_dict[i][1]}')
        fourth_day_dict = []
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('YES')
        markup.add(item1)
        bot.send_message(message.chat.id, "Are you ready?", reply_markup=markup)
        bot.register_next_step_handler(message, learn_4th_1, third_day_dict, fourth_day_dict)
    else:
        bot.send_message(message.chat.id, f"Great job! See you tomorrow")
        menu(message)



def learn_4th_1(message, third_day_dict, fourth_day_dict):
    num = random.randint(0, len(third_day_dict) - 1)
    word = third_day_dict[num]
    bot.send_message(message.chat.id, f'Enter <b>{word[1]}</b> in English')
    bot.register_next_step_handler(message, learn_4th_2, third_day_dict, fourth_day_dict, word, num)


def learn_4th_2(message, third_day_dict, fourth_day_dict, word, num):
    if message.text == word[0]:
        a = third_day_dict.pop(num)
        fourth_day_dict.append(a)
        bot.reply_to(message, 'Correct')
    else:
        bot.reply_to(message, 'Wrong')
        bot.send_message(message.chat.id, f'<b>{word[0]}</b> is correct')
    if third_day_dict == []:
        save_dict(message, fourth_day_dict)
    else:
        learn_4th_1(message, third_day_dict, fourth_day_dict)


def save_dict(message, fourth_day_dict):
    create_table(message, f'learned{get_id(message)}')
    for i in range(0, 10):
        word = fourth_day_dict[i]
        add = f"INSERT INTO learned{get_id(message)} (english, russian) VALUES ('{word[0]}', '{word[1]}')"
        try:
            cursor.execute(add)
            connection.commit()
            bot.register_next_step_handler(message, repeat_add_word)
        except Error as e:
            bot.send_message(message.chat.id, f"The error '{e}' occurred")
            bot.register_next_step_handler(message, repeat_add_word)
    bot.send_message(message.chat.id, f"The words added successfully")
    bot.send_message(message.chat.id, f"Great job! See you tomorrow")
    menu(message)


@bot.message_handler(commands=['start'])
def start(message):
    menu(message)


def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Learn words of the day")
    item2 = types.KeyboardButton("Add words")
    item3 = types.KeyboardButton("Delete words")
    item4 = types.KeyboardButton("Translate words")
    item5 = types.KeyboardButton("Show your dictionary")
    markup.add(item1, item2, item3, item4, item5)
    msg = bot.send_message(message.chat.id, f"What next?", reply_markup=markup)
    bot.register_next_step_handler(msg, choose)


def choose(message):
    if message.text == 'Learn words of the day':
        _10aday(message)
    elif message.text == 'Add words':
        add_eng(message)
    elif message.text == 'Delete words':
        delete(message)
    elif message.text == 'Translate words':
        translate_it(message)
    elif message.text == 'Show your dictionary':
        show(message)
    else:
        bot.reply_to(message, 'Try again')
        menu(message)


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        continue