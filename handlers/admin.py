from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup , State
from database import postgres_db
from create_bot import bot
import keyboards.client_kb as kb
from create_bot import main_admin

class FSMAdminSend(StatesGroup):
    user_id = State()
    message = State()

async def admin_send_command(message: types.Message):
# Початок стану
    await FSMAdminSend.user_id.set()
    await message.reply("Введіть ID користувача 👇🏼")


# Обробка ID користувача
async def process_user_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.text
    await FSMAdminSend.message.set()  # Перехід до наступного стану
    await message.reply("Тепер введіть повідомлення 👇🏼")


# Обробка повідомлення і відправка його користувачу
async def process_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = data['user_id']
        user_message = message.text

    try:
        await bot.send_message(chat_id=user_id, text=user_message)
        await message.reply(f"Повідомлення надіслано користувачу з ID {user_id}")
    except Exception as e:
        await message.reply(f"Помилка під час відправки повідомлення: {e}")

    await state.finish()  # Завершуємо стан

def register_handlers_admin(dp: Dispatcher):
    # Реєструємо хендлер для /admin_send лише коли немає активного стану
    dp.register_message_handler(admin_send_command, commands=['admin_send'], state=None)  # Вказуємо state=None

    # Обробка станів для admin_send
    dp.register_message_handler(process_user_id, state=FSMAdminSend.user_id)
    dp.register_message_handler(process_message, state=FSMAdminSend.message)