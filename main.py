import asyncio
import os
import sys
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.enums import ParseMode
from googletrans import Translator
from aiogram.client.default import DefaultBotProperties
from config import TOKEN
import random


API_TOKEN = TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)


# Создание объектов бота и диспетчера
bot = Bot(token=API_TOKEN)
# storage = MemoryStorage()
dp = Dispatcher()  # , storage=storage


# Папка для сохранения изображений.Создание папки 'img', если она не существует
if not os.path.exists('img'):
    os.makedirs('img', exist_ok=True)


# Инициализация переводчика
translator = Translator()


# Прописываем хендлер и варианты ответов:
@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое.', 'Не отправляй мне такое больше!']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')
    await message.reply("Фото сохранено!")


@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile("audio_TG02.ogg")
    await message.answer_voice(voice)


@dp.message()
async def handle_text(message: Message):
    translated_text = translator.translate(message.text, dest='en').text
    await message.reply(f"Переведенный текст: {translated_text}")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)
