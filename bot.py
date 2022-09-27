import logging
from googletrans import Translator
from aiogram import Bot, Dispatcher, executor, types
from oxford import getDefinitions

translater = Translator()
API_TOKEN = '5347442866:AAHHXVNR2L_VFFaIR7ejq43yPXhmR_fmJ9c'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Salom Men Hozircha Google orqali tarjima qila olaman")


# @dp.message_handler()
# async def code(message="admin"):
#     await message.reply("aristocratdev.t.me")

@dp.message_handler()
async def tarjimon(message: types.Message):
    lang = translater.detect(message.text).lang
    if len(message.text.split()) >= 2:
        dest='uz' if lang == "en" else 'en'
        await message.reply(translater.translate(message.text, dest).text)
    else:
        if lang == "en":
            word_id = message.text
        else:
            word_id = translater.translate(message.text, dest='en').text
        lookup = getDefinitions(word_id)
        if lookup:
            await message.reply(f"word: {word_id} \n Defenition: \n {lookup['definitions']}")
            # if lookup.get("audio"):
            #     await message.reply_audio(lookup['audio'])
        else:
            await message.reply("Bunday Soz")

   



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)