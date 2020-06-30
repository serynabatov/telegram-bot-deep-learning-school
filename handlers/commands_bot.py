import asyncio
from aiogram import types
from lambda_function import bot, dp, storage, event_loop
from keyboard import choice, yes_or_no
from machine_state import Machine_State
from aiogram.dispatcher import FSMContext
from context import Context
from strategy import Gogh, Transfer
from io import BytesIO


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message, loop=event_loop):
    await message.reply("Привет!\n", reply=False)
    await send_menu(message=message)


@dp.message_handler(commands=['help'])
async def send_menu(message: types.Message, loop=event_loop):
    await message.reply(
                        text = """ 
Что я умею? Я стараюсь преобразовывать картиночки в представленные режимы. Просто вызовите
/mode!
                        Мои команды:
                        /start - начать
                        /help - команда
                        /mode - режим
Прошу Вас присылать мне сообщения как изображения (фото). Спасибо, что вы меня слышите!
                        """, reply=False)


@dp.message_handler(commands=['mode'])
async def get_mode(message: types.Message, loop=event_loop):
    await message.answer(text="Выберите режим работы.\n"
                              "1 - Превратить картинку в \"Ван Гог\" стиль\n"
                              "2 - Сделать перенос стилей. Нужны 2 фотографии.",
                         reply_markup=choice)


@dp.callback_query_handler(text_contains="First")
async def prepare_to_load_gogh(call: types.CallbackQuery, loop=event_loop):
    gogh_mode = Gogh()
    global context
    context = Context(gogh_mode)
    await call.answer(cache_time=30)
    await call.message.answer("Вы выбрали \"Ван Гога\"! Пришлите изображение")
    await call.message.edit_reply_markup(reply_markup=None)
    await Machine_State.Q1.set()

@dp.callback_query_handler(text_contains="Second")
async def prepare_to_load_transfer(call: types.CallbackQuery, loop=event_loop):
    transfer_mode = Transfer()
    global context2
    context2 = Context(transfer_mode)
    await call.answer(cache_time=30)
    await call.message.answer("Вы выбрали перенос стилей! Пришлите 2 изображения в следующем порядке:\n"
                              "Сперва - стиль фотографии, а потом фото, которое хотите преобразовать!\n"
                               "Присылайте фотографии по отдельности, пожалуйста")
    await call.message.edit_reply_markup(reply_markup=None)
    await Machine_State.Q2.set()

@dp.message_handler(content_types=['photo'], state=Machine_State.Q1)
async def get_image(message: types.Message, state: FSMContext, loop=event_loop):
    new_file = await bot.get_file(message.photo[-1].file_id)
    photo_bytes = BytesIO()
    await new_file.download(photo_bytes)
    photo_bytes.seek(0)
    im = await loop.create_task(context.send(photo_bytes, loop))
    # -1 - для самого большого размера
    await message.reply_photo(im, caption='Новая фотография!')
    await state.finish()
    await message.answer(text="Вы хотите продолжить?", reply_markup=yes_or_no)

@dp.message_handler(content_types=['photo'], state=Machine_State.Q2)
async def get_style_image(message: types.Message, state: FSMContext, loop=event_loop):
    global new_file_style
    new_file_style = await bot.get_file(message.photo[-1].file_id)
    await Machine_State.Q3.set()

@dp.message_handler(content_types=['photo'], state=Machine_State.Q3)
async def get_context_image(message: types.Message, state: FSMContext, loop=event_loop):
    new_file_context = await bot.get_file(message.photo[-1].file_id)
    photo_bytes_style = BytesIO()
    await new_file_style.download(photo_bytes_style)
    photo_bytes_style.seek(0)
    photo_bytes_context = BytesIO()
    await new_file_context.download(photo_bytes_context)
    photo_bytes_context.seek(0)
    await message.answer(text="Пожалуйста, подождите. Мы начали обработку картинки!")
    im = await loop.create_task(context2.send([photo_bytes_style, photo_bytes_context],
                                              loop))
    await message.reply_photo(im, caption='Новая фотография!')
    await state.finish()
    await message.answer(text="Вы хотите продолжить?", reply_markup=yes_or_no)

@dp.callback_query_handler(text_contains="Yep")
async def continue_messaging(call: types.CallbackQuery, loop=event_loop):
   await call.answer(cache_time=30)
   await call.message.edit_reply_markup(reply_markup=None)
   await get_mode(call.message)

@dp.callback_query_handler(text_contains="Nope")
async def stop_messaging(call: types.CallbackQuery, loop=event_loop):
   await call.answer(cache_time=30)
   await call.message.answer("Ну, нет так нет. Чего бухтеть-то?\n До новых встреч!")
   await call.message.edit_reply_markup(reply_markup=None)

@dp.callback_query_handler(text_contains="Abort")
async def cancelling(call: types.CallbackQuery, loop=event_loop):
    await call.answer("Вы опечатались. С кем не бывает!")
    await call.message.edit_reply_markup(reply_markup=None)
