from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

request_location = ReplyKeyboardMarkup(resize_keyboard=True).\
        add(KeyboardButton('Отправить геолокацию', request_location=True, callback='location'))

request_contact = ReplyKeyboardMarkup(resize_keyboard=True).\
        add(KeyboardButton('Отправить номер телефона', request_contact=True, callback='phone'))

ikb_send_services = InlineKeyboardMarkup(row_width=2)
ikb_send_services.add(
    InlineKeyboardButton('Легковой автомобиль', callback_data='auto_l'),
    InlineKeyboardButton('Грузовой автомобиль', callback_data='auto_freight'),
    InlineKeyboardButton('Спецтехника', callback_data='auto_special'),
    InlineKeyboardButton('Микроавтобус', callback_data='auto_minibus'),
    InlineKeyboardButton('Трал', callback_data='auto_trawl'),
)