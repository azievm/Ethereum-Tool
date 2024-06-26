from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from functions import get_balance_address
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

API_TOKEN = config["Telegram"]["api_token"]

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    waiting_for_string = State()


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton("Узнать баланс 💰")
    keyboard.add(button)
    await message.answer("Приветствую! Это тестовый бот для работы с API Alchemy", reply_markup=keyboard)


@dp.message_handler(Text(equals="Узнать баланс 💰", ignore_case=True))
async def process_button(message: types.Message):
    await Form.waiting_for_string.set()
    await message.reply("Пожалуйста, отправь мне адрес кошелька эфира:")


@dp.message_handler(state=Form.waiting_for_string)
async def process_string(message: types.Message, state: FSMContext):
    address_eth = message.text

    balance_eth = get_balance_address(address_eth)

    await message.reply(f"{balance_eth} ETH")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
