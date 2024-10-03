from database import postgres_db
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def kb_client() -> ReplyKeyboardMarkup:
    start_button = KeyboardButton('/start')
    return kb_client


def ikb_client_main_menu() -> InlineKeyboardMarkup:
    ikb_client_main_menu = InlineKeyboardMarkup(row_width=1)
    notes = InlineKeyboardButton(text='Інфо', callback_data='info')
    reminders = InlineKeyboardButton(text='Замовити лабораторну роботу', callback_data='order')
    ikb_client_main_menu.add(notes, reminders)
    return ikb_client_main_menu


def ikb_client_back_to_main_menu() -> InlineKeyboardMarkup:
    ikb_client = InlineKeyboardMarkup()
    back = InlineKeyboardButton('🔙 Назад', callback_data='main_menu')
    ikb_client.add(back)
    return ikb_client



