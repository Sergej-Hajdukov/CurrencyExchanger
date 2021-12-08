import telebot
from telebot import types
from config import currency, TOKEN
from extensions import APIException, CurrencyExchanger


bot = telebot.TeleBot(TOKEN)

exchange_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
buttons = []
for elem in currency.keys():
    buttons.append(types.KeyboardButton(elem.capitalize()))

exchange_markup.add(*buttons)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Чтобы начать работать, введите команду /convert\n \
Чтобы увидеть список всех доступных валют введите команду /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currency.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(commands=['convert'])
def convert(message: telebot.types.Message):
    text = 'Выберите валюту, стоимость которой хотите узнать'
    bot.reply_to(message, text, reply_markup=exchange_markup)
    bot.register_next_step_handler(message, base_handler)


def base_handler(message: telebot.types.Message):
    base = message.text.strip().lower()
    text = 'Выберите валюту, в которой хотите оценивать'
    bot.send_message(message.chat.id, text, reply_markup=exchange_markup)
    bot.register_next_step_handler(message, quote_handler, base)


def quote_handler(message: telebot.types.Message, base):
    quote = message.text.strip().lower()
    text = 'Введите количество конвертируемой валюты'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, quote)


def amount_handler(message: telebot.types.Message, base, quote):
    amount = message.text.strip().replace(',', '.')
    try:
        total_base = CurrencyExchanger.get_price(base, quote, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка конвертации\n{e}')
    else:
        text = f'Цена {amount} {base} составляет {round(float(total_base) * float(amount), 4)} {quote}'
        bot.send_message(message.chat.id, text)


bot.polling()
