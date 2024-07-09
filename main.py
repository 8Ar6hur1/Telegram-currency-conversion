import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot('7202485590:AAFFM1Wdl_Fqto5opLeHxD-3Rgmp5saOEIA')
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Введіть сумму')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = float(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, '*Невірний формат.* \nВведіть коректну суму ще раз', parse_mode='Markdown')
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=3)
        buttons = [
            # Dollar
            types.InlineKeyboardButton('USD/UAH', callback_data='USD/UAH'),
            types.InlineKeyboardButton('USD/EUR', callback_data='USD/EUR'),
            types.InlineKeyboardButton('USD/GBP', callback_data='USD/GBP'),
            types.InlineKeyboardButton('USD/JPY', callback_data='USD/JPY'),
            types.InlineKeyboardButton('USD/CNY', callback_data='USD/CNY'),
            types.InlineKeyboardButton('USD/RUB', callback_data='USD/RUB'),
            # Euro
            types.InlineKeyboardButton('EUR/UAH', callback_data='EUR/UAH'),
            types.InlineKeyboardButton('EUR/USD', callback_data='EUR/USD'),
            types.InlineKeyboardButton('EUR/GBP', callback_data='EUR/GBP'),
            types.InlineKeyboardButton('EUR/JPY', callback_data='EUR/JPY'),
            types.InlineKeyboardButton('EUR/CNY', callback_data='EUR/CNY'),
            types.InlineKeyboardButton('EUR/RUB', callback_data='EUR/RUB'),
            # Other
            types.InlineKeyboardButton('Інше значення', callback_data='else'),
        ]
        markup.add(*buttons)
        bot.send_message(message.chat.id, 'Оберіть валюту', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, '*Сума має бути більша нуля(0).* \nВведіть коректну суму ще раз', parse_mode='Markdown')
        bot.register_next_step_handler(message, summa)

@bot.callback_query_handler(func=lambda call: call.data == 'else')
def handle_else(call):
    bot.send_message(call.message.chat.id, '*Введіть своє значення.* \nПриклад: USD/UAH', parse_mode='Markdown')
    bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
    try:
        values = message.text.upper().strip().split('/')
        if len(values) != 2:
            raise ValueError("Невірний формат валютного пари")

        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Отримана сума: {round(res, 2)} {values[1]} \nВведіть нову сумму', parse_mode='Markdown')
        bot.register_next_step_handler(message, summa)
    except Exception as e:
        bot.send_message(message.chat.id, f'*Щось пішло не так.*\nПомилка: {str(e)}', parse_mode='Markdown')
        bot.register_next_step_handler(message, my_currency)

@bot.callback_query_handler(func=lambda call: call.data.startswith(('USD/', 'EUR/')))
def handle_currency_operations(call):
    try:
        values = call.data.split('/')
        if len(values) != 2:
            raise ValueError("Невірний формат валютного пари")

        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Отримана сума: {round(res, 2)} {values[1]}', parse_mode='Markdown')
        bot.register_next_step_handler(call.message, summa)
    except Exception as e:
        bot.send_message(call.message.chat.id, f'*Щось пішло не так.*\nПомилка: {str(e)}', parse_mode='Markdown')
        bot.register_next_step_handler(call.message, summa)

bot.polling(non_stop=True)
