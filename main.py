import config
from aiogram import Bot, Dispatcher, executor, types
from keyboards import request_location, request_contact, ikb_send_services
from db import Database
from aiogram.types.reply_keyboard import ReplyKeyboardRemove


bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
db = Database('database.db')


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id)
        stic_hello = open('stickers/st_hello.webp', 'rb')
        await bot.send_sticker(message.chat.id, stic_hello)
        await bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}.\nНужна помощь? - Мы поможем!')
        await message.delete()


@dp.message_handler(commands=['help_me'])
async def help_me(message: types.Message):
    if message.chat.type == 'private':
        await bot.send_message(message.chat.id, 'Что бы мы смогли Вам помочь, отправьте свой номер телефона.',
                               reply_markup=request_contact)
        await message.delete()


@dp.message_handler(commands=['services'])
async def send_services(message: types.Message):
    if message.chat.type == 'private':
        await bot.send_message(message.chat.id, 'Услуги эвакуатора которые мы предоставляем:',
                               reply_markup=ikb_send_services)
        await message.delete()


@dp.message_handler(commands=['info'])
async def send_info(message: types.Message):
    if message.chat.type == 'private':
        await bot.send_message(message.chat.id, 'Мы работаем для Вас 24/7\n'
                                                'моб.: +375333589090\n'
                                                'Email: evoman.by@gmail.com\n'
                                                'Адрес: Республика Беларусь г.Мозырь, Нагорная 17')
        await message.delete()


@dp.callback_query_handler(lambda callback: callback.data.startswith('auto'))
async def callback_auto(callback: types.CallbackQuery):
    if callback.data == 'auto_l':
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                    text='Стоимость выбранной услуги от 80 рублей.', reply_markup=None)
    if callback.data == 'auto_freight':
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                    text='Стоимость выбранной услуги от 150 рублей.', reply_markup=None)
    if callback.data == 'auto_special':
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                    text='Стоимость выбранной услуги от 100 рублей.', reply_markup=None)
    if callback.data == 'auto_minibus':
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                    text='Стоимость выбранной услуги от 100 рублей.', reply_markup=None)
    if callback.data == 'auto_trawl':
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                    text='Стоимость выбранной услуги от 250 рублей.', reply_markup=None)


@dp.message_handler(content_types=['contact'])
async def send_contact(message: types.contact):
    if message.chat.type == 'private':
        await bot.send_message(message.from_user.id, 'Отправьте свою геолокацию', reply_markup=request_location)
        await bot.send_message(config.ADMIN, f"Нужна помошь!\n"
                                             f"Номер телефона: +{message.contact.phone_number}")


@dp.message_handler(content_types=['location'])
async def send_location(message: types.location):
    if message.chat.type == 'private':
        stic_call = open('stickers/st_call.webp', 'rb')
        await bot.send_sticker(message.chat.id, stic_call)
        await bot.send_message(message.from_user.id, 'Спасибо! Мы уже в пути и скоро свяжеся с Вами!',
                               reply_markup=ReplyKeyboardRemove())
        await bot.send_location(config.ADMIN, latitude=message.location.latitude, longitude=message.location.longitude)


@dp.message_handler(content_types=['text'])
async def send_welcome(message: types.Message):
    if message.chat.type == 'private':
        stic_ti_cho = open('stickers/st_unknow.webp', 'rb')
        await bot.send_sticker(message.chat.id, stic_ti_cho)
        await bot.send_message(message.chat.id, 'Извините, я не понимаю Вас пока-что, но обязательно научусь.')
        await message.delete()


async def on_startup(_):
    print('Бот запущен!')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)