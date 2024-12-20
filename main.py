import asyncio
import os

from request import get_forecast_city_by_name, get_city_location_key, check_bad_weather

from dotenv import load_dotenv
from aiogram import Bot, types, F, html, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(Command('start'))
async def cmd_start(msg: types.Message):
    """
    команда старт для начала диалога с ботом
    :param msg:
    :return:
    """
    kb = [
        [types.KeyboardButton(text="/start")],
        [types.KeyboardButton(text="/help")],
        [types.KeyboardButton(text="/geo")]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Нажми на /weather")
    await msg.answer('Hello 👋, it is weather Bot. He helps you to find the '
                     'information about the weather and some forecasts.', reply_markup=keyboard)

    await msg.answer('выбери опцию', reply_markup=main_kb)


@dp.callback_query(F.data == "forecast_now")
async def send_random_value(callback: types.CallbackQuery):
    """
    определяет прогноз погоды сейчас где находится пользователь
    :param callback: forecast_now
    :return: str
    """
    await callback.message.answer('Напиши 2 города в которых ты хочешь узнать погоду')

    

    await callback.message.answer('Вот и погодка в первом городе )))')
    # await callback.message.answer(get_forecast_city_by_name(api_key=TOKEN, city_name=city_1, days=0))
    await callback.message.answer('Вот и погодка во втором городе )))')
    # await callback.message.answer(get_forecast_city_by_name(api_key=TOKEN, city_name=city_2, days=0))


@dp.callback_query(F.data == "3_days")
async def send_random_value(callback: types.CallbackQuery):
    """
    определяет прогноз погоды на 3 дня по месту куда указал пользователь
    :param callback: 3_days
    :return: str
    """
    await callback.message.answer('Напиши 2 города в которых ты хочешь узнать погоду')

    @dp.message(F.text)
    async def message_city(msg: types.Message):
        """
        используем функцию для определения из какого города пользователь
        :param msg:
        :return: dict
        """
        city_1 = msg.text
        await msg.answer(f'Вот какая погода в {city_1}\n',
                         get_forecast_city_by_name(api_key=TOKEN, city_name=city_1, days=5))

    @dp.message(F.text)
    async def message_city(msg: types.Message):
        """
        используем функцию для определения из какого города пользователь
        :param msg:
        :return: dict
        """
        city_2 = msg.text
        await msg.answer(f'Вот какая погода в {city_2}\n',
                         get_forecast_city_by_name(api_key=TOKEN, city_name=city_2, days=5))

    await callback.message.answer('Погода вроде нормик, но не факт')


@dp.callback_query(F.data == "5_days")
async def send_random_value(callback: types.CallbackQuery):
    """
    определяет прогноз погоды на 5 дней по месту куда указал пользователь
    :param callback: 5_days
    :return: str
    """
    await callback.message.answer('Напиши 2 города в которых ты хочешь узнать погоду')


    @dp.message(F.text)
    async def message_city(msg: types.Message):
        """
        используем функцию для определения из какого города пользователь
        :param msg:
        :return: dict
        """
        city_1 = msg.text
        await msg.answer(f'Вот какая погода в {city_1}\n', get_forecast_city_by_name(api_key=TOKEN, city_name=city_1, days=5))


    @dp.message(F.text)
    async def message_city(msg: types.Message):
        """
        используем функцию для определения из какого города пользователь
        :param msg:
        :return: dict
        """
        city_2 = msg.text
        await msg.answer(f'Вот какая погода в {city_2}\n',
                         get_forecast_city_by_name(api_key=TOKEN, city_name=city_2, days=5))

    await callback.message.answer('Погода вроде нормик, но не факт')


# keybord buttons
lst_of_main_btns = [
[InlineKeyboardButton(text='Прогноз на 3 дня', callback_data='3_days')],
[InlineKeyboardButton(text='Прогноз на 5 дней', callback_data='5_days')],
[InlineKeyboardButton(text='Прогноз просто сейчас', callback_data='forecast_now')]
]

# the main keyboard for the telegram bot
main_kb = InlineKeyboardMarkup(inline_keyboard=lst_of_main_btns)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main(), debug=True)