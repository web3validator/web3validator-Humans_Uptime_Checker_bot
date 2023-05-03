# from cgitb import text
from aiogram import Router
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.fsm.context import FSMContext

import funtion as f
import logging


from tgbot.keyboards.inline import menu

user_router = Router()


@user_router.message(commands=["start"])
async def user_start(message: Message, state: FSMContext, bot: Bot):
    # await message.answer_sticker(sticker="sticker/cyberG.webp")
    data = await state.get_data()

    if data == {}:
        data = f.create_dict()

    # if data['message_id'] != '':
    #     await bot.delete_message(chat_id=message.chat.id, message_id=data["message_id"])
    
    logging.info(f"Message_id: {data['message_id']}")
    


    msg = await message.answer(f'Hello, {message.chat.first_name}! \n'
                        '\n'
                        'You can add validator checker through <code>create checker</code> command. \n'
                        ' - This will make me check this validator for missing blocks. \n'
                        'You can show your validator checker through <code>list checker</code> command.\n'
                        'You can delete your validator checker through <code>delete checker</code> command.\n'
                        '\n'
                        'Hey, if you like this bot, you can delegate funds to the web34ever validator.', reply_markup= menu())
    
    data['message_id'] = msg.message_id

    await state.update_data(data)
    await state.set_state(None)
    

@user_router.callback_query(text="menu")
async def Menu(callback: CallbackQuery):
    await callback.message.edit_text("<b>Menu</b>", reply_markup=menu())