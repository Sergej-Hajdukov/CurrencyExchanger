import telebot
from config import currency, TOKEN
from extensions2 import APIException, CurrencyExchanger


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Чтобы начать работать, введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести><количество переводимой валюты>\nУвидеть список всех доступных валют: \
/values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currency.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().replace(',', '.').split()

        if len(values) != 3:
            raise APIException('Задано не 3 параметра, см. /help')

        base, quote, amount = values
        total_base = CurrencyExchanger.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} составляет {round(float(total_base) * float(amount), 4)} {quote}'
        bot.send_message(message.chat.id, text)


bot.polling()