from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup , State
from database import postgres_db
from create_bot import bot
import keyboards.client_kb as kb
from create_bot import main_admin


class FSMClient(StatesGroup):
    client_id = State()
    pdf_file = State()
    variant = State()
    group = State()



async def start_command(message: types.Message):
    await start_menu(message)


async def start_menu(message: types.Message):
    user_id = message.chat.id
    user= await postgres_db.get_user(user_id)
    if user_id>0:
        if user is None:
            await postgres_db.add_user(user_id)
        with open('images/mainBanner.jpg', 'rb') as photo:
            await bot.send_photo(message.chat.id, photo,
                                 caption='Вітаємо! 👋🏽\nЦе сервіс допомоги з Лабораторними роботами!'
                                         '\n\nВиберіть дію:', reply_markup=kb.ikb_client_main_menu())

async def main_menu(call:types.CallbackQuery):
    await call.message.delete()
    await start_menu(call.message)
async def info(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.message.chat.id,text='Інформація про сервіс:\n\n'
                           'Цей сервіс допоможе вам з лабораторними роботами.\n'
                           'Ви надаєте файл з вашою лабораторною, ваш варіант та номер групи в якій ви навчаєтесь.\n'
                           'Вартість однієі лабораторної роботи - 120-200 грн.\n'
                           'Після відправки файлу ви отримаєте номер картки на яку потрібно здійснити оплату.\n'
                           'Після оплати ви отримаєте готову лабораторну роботу.\n'
                           'Термін виконання - якщо ви подали до 13:00, тоді ви отримаєте готову до 00:00 цього дня, якщо після, тоді до 12:00 наступного дня.\n'
                           ,reply_markup=kb.ikb_client_back_to_main_menu())

async def order(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await FSMClient.pdf_file.set()
    await bot.send_message(call.message.chat.id, 'Відправте файл з лабораторною роботою 👇🏼',
                           reply_markup=kb.ikb_client_back_to_main_menu())
    await state.update_data(client_id=call.message.chat.id)

async def pdf_file(message: types.Message, state: FSMContext):
    if not message.document:
        await message.answer("Будь ласка, надішліть документ у форматі PDF. 👇🏼")
        return
    async with state.proxy() as data:
        data['pdf_file'] = message.document.file_id
    await FSMClient.variant.set()  # Перехід до наступного стану
    await message.answer('Введіть ваш варіант 👇🏼')

async def variant(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['variant'] = message.text
    await FSMClient.group.set()  # Перехід до наступного стану
    await message.answer('Введіть номер групи 👇🏼')

async def group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
    data = await state.get_data()
    await postgres_db.add_order(data['pdf_file'], data['variant'], data['group'], message.chat.id)
    username = message.from_user.username
    if username:
        await bot.send_message(message.chat.id, 'Ваша заявка прийнята, менеджер звʼяжеться з вами найближчим часом',
                           reply_markup=kb.ikb_client_back_to_main_menu())
    else:
        await bot.send_message(message.chat.id, 'Ваша заявка прийнята, оскільки у вас немає юзернейму, напишіть будь ласка менеджеру: @ippo_labs ',
                               reply_markup=kb.ikb_client_back_to_main_menu())
    await bot.send_message(main_admin, f'Нова заявка на лабораторну роботу\n'
                                       f'Варіант: {data["variant"]}\n'
                                       f'Група: {data["group"]}\n'
                                       f'Від {message.chat.id}\n'
                                       f'Юзернейм: @{message.from_user.username if message.from_user.username else "немає юзернейму"}')
    await bot.send_document(main_admin, data['pdf_file'])
    await state.finish()
async def orders_list(call: types.CallbackQuery):
    orders = await postgres_db.get_order(call.message.chat.id)
    if orders is None:
        await call.message.answer('Ви ще не замовляли лабораторні роботи')
    else:
        await call.message.answer(f'Ваша заявка:\n'
                                  f'Варіант: {orders["variant"]}\n'
                                  f'Група: {orders["student_group"]}\n'
                                  f'Статус: {orders["status"]}\n'
                                  f'Ціна: {orders["price"]}\n'
                                  f'Дата замовлення: {orders["date"]}')







def register_handlers_client(dp: Dispatcher):
    # Реєструємо хендлер для /start з перевіркою на відсутність активного стану
    dp.register_message_handler(start_command, commands=['start'], state=None)

    dp.register_callback_query_handler(main_menu, text='main_menu', state="*")  # Дозволяємо обробку в будь-якому стані
    dp.register_callback_query_handler(info, text='info', state="*")
    dp.register_callback_query_handler(order, text='order', state="*")
    dp.register_message_handler(pdf_file, content_types=types.ContentType.DOCUMENT, state=FSMClient.pdf_file)
    dp.register_message_handler(variant, state=FSMClient.variant)
    dp.register_message_handler(group, state=FSMClient.group)





