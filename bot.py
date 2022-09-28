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
    await message.answer("Salom bu bot orqali gaplarni tarjima qilishingiz so`zlar haqida ma'lumotlar olishingiz mumkin va inglizcha ko`p so`zlarni qanday talafuz qilinishini ham o`rganishingiz mumkin")

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
     await message.answer("/start botni yangilash\nbitta inglizcha so`z yubirish orqali u so`z haqida malumot olishingiz mumkin yoki inglizchadan boshqa tilda so`z yuborish orqali u haqida malumot ola olmasligizngiz mumkin chunki biz siz yuborgan so`zni ingliz tiliga tarjima qilamiz va u haqda ma'lumot qidiramiz.\n⚠️Maslahat: So`z haqida ma`lumot olish uchun inglizcha so`z yuboring\n2 va undan orqtiq xabar yuborsangiz, masalan: o`zbekcha xabarni inglizchaga inglizcha xabarni o`zbek tiligi tarjima qilishi mumkin.\nBot muammolarini bizga yuborsangiz biz sizdan xursand bo`lamiz\n👨‍💻admin: aristocratdev.t.me")


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
            await message.reply(f"word: {word_id}\nDefenition:\n{lookup['definitions']}")
            if lookup.get("audio"):
                await message.reply_voice(lookup['audio'])
        else:
            await message.reply(f"qidirligan so`z: {word_id}\nBunday Soz Topilmadi ✌️😕")

   

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)