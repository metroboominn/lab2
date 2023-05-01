from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import random

TOKEN = "5978800429:AAFW2EW2GK1QMrKSu8_gtYTtz0299nMKGSE"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    random_number = State()
    user_number = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await UserState.random_number.set()
    await bot.send_message(message.chat.id, 'Загадано число от 1 до 50. Попробуй угадать)')


@dp.message_handler(state=UserState.random_number)
async def random_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['random_number'] = random.randint(1, 50)
    await UserState.next()
    if int(message.text) == data['random_number']:
        await message.reply('Ура! Ты угадал!')
        await state.finish()
    elif int(message.text) > data['random_number']:
        await message.reply('Неудача. Загаданное число меньше.')
    elif int(message.text) < data['random_number']:
        await message.reply('Неудача. Загаданное число больше.')


@dp.message_handler(state=UserState.user_number)
async def answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_number'] = int(message.text)
    if data['user_number'] == data['random_number']:
        await message.reply('Ура! Ты угадал!')
        await state.finish()
    elif data['user_number'] > data['random_number']:
        await message.reply('Неудача. Загаданное число меньше.')
        return answer
    elif data['user_number'] < data['random_number']:
        await message.reply('Неудача. Загаданное число больше.')
        return answer


if __name__ == "__main__":
    executor.start_polling(dp)
