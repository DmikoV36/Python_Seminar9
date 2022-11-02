import telebot
from telebot import types
import psycopg2

conn = psycopg2.connect(dbname='Population, density and surface area', user='postgres', 
                        password='1111', host='localhost')
cursor = conn.cursor()

API_TOKEN='*****'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton("Форматы поиска информации")
    markup.add(item1)
    bot.send_message(message.chat.id,"Я могу найти информацию из базы ООН по численности населения в разных регионах.", reply_markup=markup)

@bot.message_handler(commands=['info_region'])
def info_region(message):
    quest = message.text.split()[1:]
    if quest == [] or len(quest) < 2:
        bot.send_message(message.chat.id, 'Информация в запросе не соответствует формату. Регион и год обязательны для ввода.')
    else:
        if quest[0].isdigit():
            cursor.execute(f"SELECT region, year, series, value FROM data_table WHERE year = '{quest[1]}' and iso = '{quest[0]}';")
        else:
            cursor.execute(f"SELECT region, year, series, value FROM data_table WHERE year = '{quest[1]}' and region = '{quest[0]}';")
        records = cursor.fetchmany(size=8)
        if records != []:
            bot.send_message(message.chat.id, f'{records}')
        else:
            bot.send_message(message.chat.id, 'Такие данные в базе не найдены')
        print(records)

@bot.message_handler(commands=['population_region'])
def population_region(message):
    quest = message.text.split()[1:]
    if quest == [] or len(quest) < 2:
        bot.send_message(message.chat.id, 'Информация в запросе не соответствует формату. Регион и год обязательны для ввода.')
    else:
        if quest[0].isdigit():
            cursor.execute(f"SELECT region, year, series, value FROM data_table WHERE year = '{quest[1]}' and iso = '{quest[0]}' and series = 'Population mid-year estimates (millions)';")
        else:
            cursor.execute(f"SELECT region, year, series, value FROM data_table WHERE year = '{quest[1]}' and region = '{quest[0]}' and series = 'Population mid-year estimates (millions)';")
        records = cursor.fetchall()
        if records != []:
            bot.send_message(message.chat.id, f'Население {records[0][0]} в {records[0][1]} году составляло {records[0][3]} млн.чел.')
        else:
            bot.send_message(message.chat.id, 'Такие данные в базе не найдены')
        print(records)

@bot.message_handler(commands=['m_population'])
def m_population(message):
    quest = message.text.split()[1:]
    if quest == [] or len(quest) < 2:
        bot.send_message(message.chat.id, 'Информация в запросе не соответствует формату. Регион и год обязательны для ввода.')
    else:
        if quest[0].isdigit():
            cursor.execute(f"SELECT region, year, series, value FROM data_table WHERE year = '{quest[1]}' and iso = '{quest[0]}' and series LIKE '%for males%';")
        else:
            cursor.execute(f"SELECT region, year, series, value FROM data_table WHERE year = '{quest[1]}' and region = '{quest[0]}' and series LIKE '%for males%';")
        records = cursor.fetchall()
        if records != []:
            bot.send_message(message.chat.id, f'Мужское население {records[0][0]} в {records[0][1]} году составляло {records[0][3]} млн.чел.')
        else:
            bot.send_message(message.chat.id, 'Такие данные в базе не найдены')
        print(records)

@bot.message_handler(commands=['f_population'])
def f_population(message):
    quest = message.text.split()[1:]
    if quest == [] or len(quest) < 2:
        bot.send_message(message.chat.id, 'Информация в запросе не соответствует формату. Регион и год обязательны для ввода.')
    else:
        if quest[0].isdigit():
            cursor.execute(f"SELECT region, year, series, value FROM data_table WHERE year = '{quest[1]}' and iso = '{quest[0]}' and series LIKE '%for females%';")
        else:
            cursor.execute(f"SELECT region, year, series, value FROM data_table WHERE year = '{quest[1]}' and region = '{quest[0]}' and series LIKE '%for females%';")
        records = cursor.fetchall()
        if records != []:
            bot.send_message(message.chat.id, f'Женское население {records[0][0]} в {records[0][1]} году составляло {records[0][3]} млн.чел.')
        else:
            bot.send_message(message.chat.id, 'Такие данные в базе не найдены')
        print(records)

@bot.message_handler(commands=['sex_ratio'])
def sex_ratio(message):
    quest = message.text.split()[1:]
    if quest == [] or len(quest) < 2:
        bot.send_message(message.chat.id, 'Информация в запросе не соответствует формату. Регион и год обязательны для ввода.')
    else:
        if quest[0].isdigit():
            cursor.execute(f"SELECT region, year, series, value FROM data_table WHERE year = '{quest[1]}' and iso = '{quest[0]}' and series LIKE 'Sex ratio%';")
        else:
            cursor.execute(f"SELECT region, year, series, value FROM data_table WHERE year = '{quest[1]}' and region = '{quest[0]}' and series LIKE 'Sex ratio%';")
        records = cursor.fetchall()
        if records != []:
            bot.send_message(message.chat.id, f'Соотношение полов в {records[0][0]} в {records[0][1]} году составляло {records[0][3]} мужчин на 100 женщин')
        else:
            bot.send_message(message.chat.id, 'Такие данные в базе не найдены')
        print(records)

@bot.message_handler(commands=['children'])
def children(message):
    quest = message.text.split()[1:]
    if quest == [] or len(quest) < 2:
        bot.send_message(message.chat.id, 'Информация в запросе не соответствует формату. Регион и год обязательны для ввода.')
    else:
        if quest[0].isdigit():
            cursor.execute(f"SELECT region, year, series, value FROM data_table WHERE year = '{quest[1]}' and iso = '{quest[0]}' and series LIKE '%0 to 14%';")
        else:
            cursor.execute(f"SELECT region, year, series, value FROM data_table WHERE year = '{quest[1]}' and region = '{quest[0]}' and series LIKE '%0 to 14%';")
        records = cursor.fetchall()
        if records != []:
            bot.send_message(message.chat.id, f'Детское население (от 0 до 14 лет) в {records[0][0]} в {records[0][1]} году составляло {records[0][3]}% от общего населения')
        else:
            bot.send_message(message.chat.id, 'Такие данные в базе не найдены')
        print(records)

@bot.message_handler(commands=['elderly'])
def elderly(message):
    quest = message.text.split()[1:]
    if quest == [] or len(quest) < 2:
        bot.send_message(message.chat.id, 'Информация в запросе не соответствует формату. Регион и год обязательны для ввода.')
    else:
        if quest[0].isdigit():
            cursor.execute(f"SELECT region, year, series, value FROM data_table WHERE year = '{quest[1]}' and iso = '{quest[0]}' and series LIKE '%60+%';")
        else:
            cursor.execute(f"SELECT region, year, series, value FROM data_table WHERE year = '{quest[1]}' and region = '{quest[0]}' and series LIKE '%60+%';")
        records = cursor.fetchall()
        if records != []:
            bot.send_message(message.chat.id, f'Население возрастной группы 60+ в {records[0][0]} в {records[0][1]} году составляло {records[0][3]}% от общего населения')
        else:
            bot.send_message(message.chat.id, 'Такие данные в базе не найдены')
        print(records)

@bot.message_handler(commands=['population_density'])
def population_density(message):
    quest = message.text.split()[1:]
    if quest == [] or len(quest) < 2:
        bot.send_message(message.chat.id, 'Информация в запросе не соответствует формату. Регион и год обязательны для ввода.')
    else:
        if quest[0].isdigit():
            cursor.execute(f"SELECT region, year, series, value FROM data_table WHERE year = '{quest[1]}' and iso = '{quest[0]}' and series = 'Population density';")
        else:
            cursor.execute(f"SELECT region, year, series, value FROM data_table WHERE year = '{quest[1]}' and region = '{quest[0]}' and series = 'Population density';")
        records = cursor.fetchall()
        if records != []:
            bot.send_message(message.chat.id, f'Плотность населения в {records[0][0]} в {records[0][1]} году составляла {records[0][3]} жителей на квадратный км.')
        else:
            bot.send_message(message.chat.id, 'Такие данные в базе не найдены')
        print(records)

@bot.message_handler(commands=['surface_area'])
def surface_area(message):
    quest = message.text.split()[1:]
    if quest == [] or len(quest) < 2:
        bot.send_message(message.chat.id, 'Информация в запросе не соответствует формату. Регион и год обязательны для ввода.')
    else:
        if quest[0].isdigit():
            cursor.execute(f"SELECT region, year, series, value FROM data_table WHERE year = '{quest[1]}' and iso = '{quest[0]}' and series LIKE 'Surface area%';")
        else:
            cursor.execute(f"SELECT region, year, series, value FROM data_table WHERE year = '{quest[1]}' and region = '{quest[0]}' and series LIKE 'Surface area%';")
        records = cursor.fetchall()
        if records != []:
            bot.send_message(message.chat.id, f'Площадь {records[0][0]} в {records[0][1]} году составляла {records[0][3]} тысяч квадратных км.')
        else:
            bot.send_message(message.chat.id, 'Такие данные в базе не найдены')
        print(records)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    print(message.text)
    if message.text.strip() == 'Форматы поиска информации':
        with open('Requests.txt', 'r', encoding="utf-8") as data:
            for line in data:
                bot.send_message(message.chat.id, line)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton("Форматы поиска информации")
        markup.add(item1)
        bot.send_message(message.chat.id, "Введите информацию в соотвествии с форматом запроса", reply_markup=markup)
    print('OK')

bot.polling()