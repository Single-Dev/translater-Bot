import logging
import hashlib
from time import sleep
from googletrans import Translator
from aiogram import Bot, Dispatcher, executor, types
from oxford import getDefinitions   
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle, CallbackQuery

# for btn
import btns as btn

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const


translater = Translator()
API_TOKEN = '5347442866:AAEqKFa3iKriwMTEz0IzOjDmvu43s6C9WJ0'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def go_clicked(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.message.answer("Going on!")




go_btn = Button(
    Const("Go"),
    on_click=go_clicked,
    id="go"
)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Salom bu bot orqali gaplarni tarjima qilishingiz so`zlar haqida ma'lumotlar olishingiz mumkin va inglizcha ko`p so`zlarni qanday talafuz qilinishini ham o`rganishingiz mumkin",)

    

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
     await message.answer("Botdagi Muammonni Menga Yuboring.", reply_markup=btn.admin_btn)


@dp.message_handler()
async def tarjimon(message: types.Message):
    lang = translater.detect(message.text).lang
    if len(message.text.split()) >= 2:
        dest='uz' if lang == "en" else 'en'
        # await message.reply(f"{lang} - {dest}\n{translater.translate(message.text, dest).text}")
        await message.reply(translater.translate(message.text, dest).text)
    else:
        dest='uz' if lang == "en" else 'en'
        await message.reply(translater.translate(message.text, dest).text)
        sleep(1)
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
        # else:
            # await message.answer(f"{word_id} Bo'yicha Malumotlar Topilmadi")

@dp.inline_handler()
async def inline(inline_query: InlineQuery):
    inline_search = inline_query.query
    lang = translater.detect(inline_search).lang
    dest='uz' if lang == "en" else 'en'
    text = translater.translate(inline_search, dest).text
    trans_input_content = InputTextMessageContent(text)

    result_id: str = hashlib.md5(text.encode()).hexdigest()
    item = InlineQueryResultArticle(
        id=result_id,
        title=text,
        input_message_content=trans_input_content,
    )
    await bot.answer_inline_query(inline_query.id, results=[item])
    # text_1 = translater.translate(inline_search, dest="en").text
    # lookup = getInlineDefinitions(text_1)
    # if lookup:
    #     text_1 = lookup['definitions']
    # else:
    #     text_1 = "topilmadi"
    # input_content = InputTextMessageContent(f"word:{inline_search}\nDefinitions:\n{text_1}")
    # result_id_1: str = hashlib.md5(text_1.encode()).hexdigest()
    # item_1 = InlineQueryResultArticle(
    #     id=result_id_1,
    #     title=text_1,
    #     input_message_content=input_content,
    # )
    # await bot.answer_inline_query(inline_query.id, results=[item_1])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)