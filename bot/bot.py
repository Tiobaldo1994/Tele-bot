from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

import config
import keyboard

import logging       # ПРОСТО ВЫВОДИТ В КОНСОЛЬ ИНФОРМАЦИЮ, КОГДА БОТ ЗАПУСТИТСЯ


storage = MemoryStorage()                           # FOR FSM
bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

class meinfo(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()

@dp.message_handler(Command("sign"), state=None)  # Создаем команду /me для админа.
async def enter_meinfo(message: types.Message):
    # if message.chat.id == config.admin:
    await message.answer("Начинаем запись.\n"  # Бот спрашивает ссылку
                             "Введите желаемую процедуру")
    await meinfo.Q1.set()  # и начинает ждать наш ответ.

@dp.message_handler(state=meinfo.Q1)  # Как только бот получит ответ, вот это выполнится
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1=answer)  # тут же он записывает наш ответ (наш линк)

    await message.answer("Сохранено. \n"
                         "Введите желаемую дату и время.")
    await meinfo.Q2.set()  # дальше ждёт пока мы введем текст


@dp.message_handler(state=meinfo.Q2)  # Текст пришел, значит переходим к этому шагу
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer2=answer)  # опять же он записывает второй ответ

    await message.answer("Отметили в календаре. А теперь выберите мастера", reply_markup=keyboard.master)
    await meinfo.Q3.set()


@dp.message_handler(state=meinfo.Q3)  # Текст пришел а значит переходим к этому шагу
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer3=answer)  # опять же он записывает второй ответ
    await message.answer(
        "Ваш заказ сохранен.\nВ ближайшее время Вам позвонит администратор\n уточнить пару моментов. Введите команду /call, чтобы указать свой номер.")

    data = await state.get_data()  #
    answer1 = data.get("answer1")  # тут он сует ответы в переменную, чтобы сохранить их в "БД" и вывести в след. сообщении
    answer2 = data.get("answer2")  #
    answer3 = data.get("answer3")

    joinedFile = open("info.txt", "w", encoding="utf-8")  # Вносим в "БД" encoding="utf-8" НУЖЕН ДЛЯ ТОГО, ЧТОБЫ ЗАПИСЫВАЛИСЬ СМАЙЛИКИ
    joinedFile.write(str(answer1))
    joinedFile.write('\n')
    joinedFile.write(str(answer2))
    joinedFile.write('\n')
    joinedFile.write(str(answer3))
    joinedFile.close()

    await message.answer(f'Процедура : {answer1}\nДата и время: {answer2}\nМастер: {answer3}')
    await state.finish()

@dp.message_handler(Command("start"), state=None)
async def welcome(message):
    await bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}, Выберите желаемую процедуру\n для записи нажмиnt /sign", reply_markup=keyboard.start, parse_mode='Markdown')


@dp.message_handler(Text(equals="Стрижка"))
async def with_puree(message: types.Message):

    await message.reply("""Отличный выбор!\n
    Наш прайс:\n
    Каре - 18 BYN\n
    До плеч - 21 BYN\n
    Ниже плеч - 23 BYN""")


@dp.message_handler(lambda message: message.text == "Окрашивание")
async def without_puree(message: types.Message):
    await message.reply("""Вот это интересно!\n
    Наш прайс:\n
    Окрашивание корней- 30-50  BYN\n
    Однотонное/тонирование - 40-60  BYN\n
    Окрашивание челки - 30-50 BYN\n
    Сложное окрашивание - 120-200 BYN""")

@dp.message_handler(lambda message: message.text == "Уходовые процедуры")
async def without_puree(message: types.Message):
    await message.reply("""Самое время!\n
    Наш прайс:\n
    Полировка - 30-50  BYN\n
    Ламинирование - 40-60  BYN\n
    Ботекс - 30-50 BYN\n
    Счастье для волос - 120-200 BYN""")

@dp.message_handler(commands="call")
async def cmd_special_buttons(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Поделиться контактом", request_contact=True))
    await message.answer("Для удобства записи укажите ваш номер телефона:", reply_markup=keyboard)



if __name__ == "__main__":

    executor.start_polling(dp, skip_updates=True)