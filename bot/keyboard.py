from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

######################################################
start = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False) # СОЗДАЕМ ВООБЩЕ ОСНОВУ ДЛЯ КНОПОК

haircut = types.KeyboardButton("Стрижка")
color = types.KeyboardButton("Окрашивание")
care = types.KeyboardButton("Уходовые процедуры")
start.add(haircut, color, care)


master = InlineKeyboardMarkup()
master.add(InlineKeyboardButton('Артем', callback_data = 'Artem'))
master.add(InlineKeyboardButton('Ирина', callback_data = 'Irina'))
master.add(InlineKeyboardButton('Кристина', callback_data = 'Christina'))

