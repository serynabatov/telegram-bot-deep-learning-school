from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from callback import remember_callback

choice = InlineKeyboardMarkup(
           inline_keyboard = [
                  [
                      InlineKeyboardButton(text="\"Ван Гог\"", 
                                           callback_data=remember_callback.new(item_name="First" )),
                      InlineKeyboardButton(text="Перенос стилей",
                                           callback_data=remember_callback.new(item_name="Second"))
                  ],
                  [
                      InlineKeyboardButton(text="Отмена", callback_data=remember_callback.new(item_name="Abort"))
                  ]
           ]
)

yes_or_no = InlineKeyboardMarkup(
              inline_keyboard = [
                     [
                       InlineKeyboardButton(text="Да", callback_data=remember_callback.new(item_name="Yep"))
                     ],
                     [
                       InlineKeyboardButton(text="Нет", callback_data=remember_callback.new(item_name="Nope"))
                     ]
              ]
)
