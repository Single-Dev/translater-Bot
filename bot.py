import logging
import hashlib
from time import sleep
from googletrans import Translator
from aiogram import Bot, Dispatcher, executor, types
from oxford import getDefinitions, getInlineDefinitions
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle


translater = Translator()
API_TOKEN = '5347442866:AAEbThSlucl31cjTEdZbRfbFvh9XNO6nuvE'
# API_TOKEN = '5567666571:AAHtd55YKgj6M5xEPbpvL4UmxUkloVj0aGE'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Salom bu bot orqali gaplarni tarjima qilishingiz so`zlar haqida ma'lumotlar olishingiz mumkin va inglizcha ko`p so`zlarni qanday talafuz qilinishini ham o`rganishingiz mumkin")
    # mb=100
    # for i in range(mb):
    #     sleep(0.5)
    #     await message.answer(f"{i/mb*100:.1f} % shuncha yuklandi.", end=message.delete)

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
     await message.answer("/start botni yangilash\nbitta inglizcha so`z yubirish orqali u so`z haqida malumot olishingiz mumkin yoki inglizchadan boshqa tilda so`z yuborish orqali u haqida malumot ola olmasligizngiz mumkin chunki biz siz yuborgan so`zni ingliz tiliga tarjima qilamiz va u haqda ma'lumot qidiramiz.\n⚠️Maslahat: So`z haqida ma`lumot olish uchun inglizcha so`z yuboring\n2 va undan orqtiq xabar yuborsangiz, masalan: o`zbekcha xabarni inglizchaga inglizcha xabarni o`zbek tiligi tarjima qilishi mumkin.\nBot muammolarini bizga yuborsangiz biz sizdan xursand bo`lamiz\n👨‍💻admin: aristocratdev.t.me")

@dp.message_handler(commands=['settings'])
async def send_welcome(message: types.Message):
    
    await message.answer("")

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
            if lang == "en":
                await message.reply(f"word: {word_id}\nDefinitions:\n{lookup['definitions']}\n")
            if lang == "uz":
                await message.reply(f"so`z: {word_id}\nMa'lumotlar:\n{translater.translate(lookup['definitions'], dest='uz' ).text}\n")
            if lookup.get("audio"):
                await message.reply_voice(lookup['audio'])
        else:
            await message.reply(f"qidirligan so`z: {word_id}\nBunday Soz Topilmadi 😕 \nSiz bunday degan bo`lishingiz mumkin 'cars' aslida 'car' orqali topasiz.")

@dp.inline_handler()
async def inline(inline_query: InlineQuery):
    inline_search = inline_query.query
    text = translater.translate(inline_search, dest="en").text
    lookup = getInlineDefinitions(text)
    if lookup:
        text = lookup['definitions']
    else:
        text = "topilmadi"
    input_content = InputTextMessageContent(f"word:{inline_search}\nDefinitions:\n{text}")
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    item = InlineQueryResultArticle(
        id=result_id,
        title=text,
        input_message_content=input_content,
    )
    await bot.answer_inline_query(inline_query.id, results=[item])
   

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)