import asyncio
import os

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from request import get_forecast_city_by_name, get_city_location_key, check_bad_weather, presentation_of_the_data

from dotenv import load_dotenv
from aiogram import Bot, types, F, html, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup

load_dotenv()

TOKEN = os.getenv('TOKEN')
TOKEN_API = os.getenv('TOKEN_API')
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

users_data = {}

class Form(StatesGroup):
    """
    класс состояний в которых может находиться бот
    :param : city_one, city_two, city_now
    """
    city_one_choosing = State()
    city_two_choosing = State()
    city_now_done = State()

@dp.message(Command('start'))
async def cmd_start(msg: types.Message):
    """
    команда старт для начала диалога с ботом
    :param msg: str
    :return:
    """

    kb = [
        types.KeyboardButton(text="/start"),
        types.KeyboardButton(text="/help"),
        types.KeyboardButton(text="/geo")
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=[kb], resize_keyboard=True, input_field_placeholder="Нажми на /weather")
    await msg.answer('Hello 👋, it is weather Bot. He helps you to find the '
                     'information about the weather and some forecasts.', reply_markup=keyboard)

    await msg.answer('выбери опцию', reply_markup=main_kb)

@dp.message(Command('help'))
async def help(msg: types.Message):
    await msg.answer('вот функции которые ты можешь использовать:')
    await msg.answer("""
    /start - начало работы бота, 
    /help - все функции бота, 
    /geo - в разработке ))
    """)

@dp.callback_query(StateFilter(None), F.data == "3_days")
async def send_random_value(callback: types.CallbackQuery, state: FSMContext):
    """
    определяет прогноз погоды на 3 дня по месту куда указал пользователь
    :param callback: 3_days
    :return: str
    """

    kb = [
        types.KeyboardButton(text="/start"),
        types.KeyboardButton(text="/help"),
        types.KeyboardButton(text="/geo")
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=[kb], resize_keyboard=True,
                                         input_field_placeholder="выбери первый город")

    await callback.message.answer('Напиши первый город', reply_markup=keyboard)

    await state.set_state(Form.city_one_choosing)


@dp.message(Form.city_one_choosing)
async def city_one_choose_for_3_days(msg: types.Message, state: FSMContext):

    await state.update_data(choosen_city_one=msg.text)

    users_data['city_one_choosing'] = msg.text

    kb = [
        types.KeyboardButton(text="/start"),
        types.KeyboardButton(text="/help"),
        types.KeyboardButton(text="/geo")
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=[kb], resize_keyboard=True,
                                         input_field_placeholder="выбери второй город")

    await msg.answer("Спасибо, напиши название второго города", reply_markup=keyboard)


    await state.set_state(Form.city_two_choosing)



@dp.message(Form.city_two_choosing)
async def city_two_choose_for_3_days(msg: types.Message, state: FSMContext):

    await state.update_data(choosen_city_two=msg.text)

    users_data['city_two_choosing'] = msg.text

    await msg.answer("Thank you for choosing the second city")
    await state.set_state(Form.city_now_done)

    user_data = await state.get_data()

    try:

        data_1 = get_forecast_city_by_name(api_key=TOKEN_API, city_name=users_data['city_one_choosing'], days=3)
        data_2 = get_forecast_city_by_name(api_key=TOKEN_API, city_name=users_data['city_two_choosing'], days=3)

        kb = [
            types.KeyboardButton(text="/start"),
            types.KeyboardButton(text="/help"),
            types.KeyboardButton(text="/geo")
        ]

        keyboard = types.ReplyKeyboardMarkup(keyboard=[kb], resize_keyboard=True,
                                             input_field_placeholder="вот и погодка в городах")

        text = f"Полученные данные: для города {html.bold(users_data['city_one_choosing'])}\n"
        for key, value in data_1.items():
            text += f"{key}: {html.bold(value)}\n"
        await msg.answer(text)

        text = f"Полученные данные: для города {html.bold(users_data['city_two_choosing'])}\n"
        for key, value in data_2.items():
            text += f"{key}: {html.bold(value)}\n"
        await msg.answer(text)

        await msg.answer(f'<b>Thank you</b>, {msg.from_user.first_name}', parse_mode=ParseMode.HTML)

    except Exception as e:

        print(f"Ошибка при запросе к API: {e}")
        return None

    finally:

        await state.clear()


@dp.callback_query(StateFilter(None), F.data == "5_days")
async def send_random_value(callback: types.CallbackQuery, state: FSMContext):
    """
    определяет прогноз погоды на 5 дней по месту куда указал пользователь
    :param callback: 5_days
    :return: str
    """

    kb = [
        types.KeyboardButton(text="/start"),
        types.KeyboardButton(text="/help"),
        types.KeyboardButton(text="/geo")
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=[kb], resize_keyboard=True,
                                         input_field_placeholder="выбери первый город")


    await callback.message.answer('Напиши название первого города', reply_markup=keyboard)

    await state.set_state(Form.city_one_choosing)


@dp.message(Form.city_one_choosing)
async def city_one_choose_for_5_days(msg: types.Message, state: FSMContext):

    await state.update_data(choosen_city_one=msg.text)

    users_data['city_one_choosing'] = msg.text

    kb = [
        types.KeyboardButton(text="/start"),
        types.KeyboardButton(text="/help"),
        types.KeyboardButton(text="/geo")
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=[kb], resize_keyboard=True,
                                         input_field_placeholder="выбери второй город")

    await msg.answer("Спасибо, напиши название второго города")

    await state.set_state(Form.city_two_choosing)



@dp.message(Form.city_two_choosing)
async def city_two_choose_for_5_days(msg: types.Message, state: FSMContext):

    await state.update_data(choosen_city_two=msg.text)

    users_data['city_two_choosing'] = msg.text

    kb = [
        types.KeyboardButton(text="/start"),
        types.KeyboardButton(text="/help"),
        types.KeyboardButton(text="/geo")
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=[kb], resize_keyboard=True,
                                         input_field_placeholder="вот и погодка")

    await msg.answer("Спасибо, вот погодка", reply_markup=keyboard)

    await state.set_state(Form.city_now_done)

    user_data = await state.get_data()


    try:

        data_1 = get_forecast_city_by_name(api_key=TOKEN_API, city_name=users_data['city_one_choosing'], days=5)
        data_2 = get_forecast_city_by_name(api_key=TOKEN_API, city_name=users_data['city_two_choosing'], days=5)


        text = f"Полученные данные: для города {html.bold(users_data['city_one_choosing'])}\n"
        for key, value in data_1.items():
            text += f"{key}: {html.bold(value)}\n"
        await msg.answer(text)

        text = f"Полученные данные: для города {html.bold(users_data['city_two_choosing'])}\n"
        for key, value in data_2.items():
            text += f"{key}: {html.bold(value)}\n"
        await msg.answer(text)

        await msg.answer(f'<b>Thank you</b>, {msg.from_user.first_name}', parse_mode=ParseMode.HTML)

    except Exception as e:

        print(f"Ошибка при запросе к API: {e}")

        return None

    finally:

        await state.clear()


@dp.message(F.data == 'forecast_now')
async def for_now(msg: types.Message):
    await msg.answer(html.bold("I am sorry, right now this function is not being allow ("))

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