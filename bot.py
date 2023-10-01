import logging
import config as cfg
import markups as nav
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from db import Database
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
logging.basicConfig(level=logging.INFO)

bot = Bot(token='6252866243:AAETikQiexAm4lBByvhA8t-7ENbcLIYbZIQ')   
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database('database.db')

photo = open('C:/Users/22835/Desktop/enrd/futbolkii/1.jpg', 'rb')

admin_id = 903671604

class Form(StatesGroup):
    futbolka = State() 
    futbolka2 = State()

@dp.message_handler(commands=['start'])
async def starting(message: types.Message):
   await bot.send_message(message.from_user.id, "1. Здравствуйте! Этот бот создан для автоматического принятия заказов на футболки @yaenyx\nЕсли вы хотите совершить заказ - напишите 'Сделать заказ', либо воспользуйтесь кнопкой ниже. ",reply_markup=nav.Menu)

@dp.message_handler(commands=['sendall'])
async def sendall(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id == 727959236:
            text = message.text[9:]
            users = db.get_users()
            for row in users:
                try:
                    await bot.send_message(row[0], text)
                    if int(row[1]) != 1:
                        db.set_active(row[0], 1)
                except:
                    db.set_active(row[0], 0)
                    
            await bot.send_message(message.from_user.id, "Рассылка успешно сделана")
            print("Рассылка успешно завершена!")
        

@dp.message_handler(text=['Сделать заказ'])
async def cmd_start(message: types.Message):
    await Form.futbolka.set()
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await bot.send_message(message.from_user.id, "2. Наш ассортимент:\n1. hosayn [1099р] \n2. kktk? [1099р]  \n3. octo [1199р] \n4. stfu. [1199р]",reply_markup=nav.Cost)

@dp.message_handler(state='*', text='Отмена')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('ОК', reply_markup=nav.mainMenu)
    
@dp.message_handler(state=Form.futbolka)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['futbolka'] = message.text
        await bot.forward_message(admin_id, message.from_user.id, message.message_id)
        await bot.send_message(message.from_user.id, "3. Максимальной ценой будет 1599р (С учетом доставки по всей РФ)\n Вы согласны с ценой? ", reply_markup=nav.Answer)
        await state.finish()
@dp.message_handler(text=['Да'])
async def cmd_yes(message: types.Message):
        await bot.send_message(message.from_user.id, "4. Отлично! Ваш заказ отправлен продавцу и вскоре он напишет вам для расчета стоимости доставки и прочих уточнений.", reply_markup=nav.Menu)
        await bot.forward_message(admin_id, message.from_user.id, message.message_id)

@dp.message_handler(text=['Нет'])
async def cmd_yes(message: types.Message):
        await bot.send_message(message.from_user.id, "Хорошо", reply_markup=nav.Menu)
        await bot.forward_message(admin_id, message.from_user.id, message.message_id)
    

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)