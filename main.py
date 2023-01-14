from bs4 import BeautifulSoup
import requests
from settings import TOKEN

def parse_data(query):
    if query != 'скидка':
        return 'Некорректный запрос.'
    try:
        url = 'https://www.wildberries.ru/catalog/zhenshchinam'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', {'class': 'dtList-inner'})
        result = []
        for item in items:
            discount = item.find('span', {'class': 'discount-value'}).text
            if int(discount[:-1]) >= 35:
                result.append(item.find('span', {'class': 'goods-name'}).text)
        if len(result) == 0:
            return 'В разделе одежды ничего со скидкой больше или равно 35% не найдено.'
        return '\n'.join(result[:10])
    except:
        return 'Возникла ошибка при парсинге сайта.'

def welcome_message():
    return 'Здравствуйте! Я помогу Вам найти 10 товаров с сайта wildberris из раздела одежда со скидкой больше или равно 35%. Для этого напишите мне "скидка".'
import telebot

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome_message(message):
    bot.send_message(message.chat.id, welcome_message())

@bot.message_handler(content_types=['text'])
def send_query_response(message):
    bot.send_message(message.chat.id, parse_data(message.text))

bot.polling()