from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

Menu = ReplyKeyboardMarkup(resize_keyboard = True)
btnProfile = KeyboardButton("Сделать заказ")
Menu.add(btnProfile)

Answer = ReplyKeyboardMarkup(resize_keyboard = True)
btnAns = KeyboardButton("Да")
btnAns2 = KeyboardButton("Нет")
Answer.add(btnAns)
Answer.add(btnAns2)

Cost = ReplyKeyboardMarkup(resize_keyboard = True)
btnCost1 = KeyboardButton("1")
btnCost2 = KeyboardButton("2")
btnCost3 = KeyboardButton("3")
btnCost4 = KeyboardButton("4")
Cost.add(btnCost1)
Cost.add(btnCost2)
Cost.add(btnCost3)
Cost.add(btnCost4)

cancel = ReplyKeyboardMarkup(resize_keyboard = True)
btnCancel = KeyboardButton("Отмена")
cancel.add(btnCancel)

