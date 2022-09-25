import logging
from googletrans import Translator
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5347442866:AAHHXVNR2L_VFFaIR7ejq43yPXhmR_fmJ9c'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Salom Men Hozircha Google orqali tarjima qila olaman")


@dp.message_handler()
async def code(message="admin"):
    await message.reply("aristocratdev.t.me`")

@dp.message_handler()
async def tarjimon(message: types.Message):
    user_msg = message.text
    send_msg = Translator.translate(user_msg, dest='en')
    await message.reply(send_msg)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)