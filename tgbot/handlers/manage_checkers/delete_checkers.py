import logging, json, toml
from aiogram import Bot
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.dispatcher.fsm.storage.redis import RedisStorage


# from api.config import nodes
# from api.requests import MintScanner
from tgbot.handlers.manage_checkers.router import checker_router
from tgbot.misc.states import DeleteChecker
from tgbot.keyboards.inline import menu, to_menu, list_validators

def num_data(data, keys_data):
    new_data = dict()
    j =  0 
    logging.info(f"{keys_data}")
    for i in keys_data:
        new_data[str( j )] = data[i]
        j += 1
    return new_data

# id_message = {}



@checker_router.callback_query(text="delete")
async def create_checker(callback: CallbackQuery, state: FSMContext):
    
    
    """Entry point for create checker conversation"""
    
    data = await state.get_data()

    validators = data.get('validators', {})
    validators_list = list(validators.keys())

    if not validators_list:
        await callback.answer(
            'Sorry, but I didn\'t find any checker. \n'
            'First, create a checker',
            # show_alert=True
        )

        return


    await callback.message.edit_text(
            'Let\'s see...\n'
            'What\'s your validator\'s name?',
            reply_markup=list_validators(validators_list, "delete")
        )


@checker_router.callback_query(Text(text_startswith="delete&"))
async def enter_operator_address(callback: CallbackQuery, state: FSMContext):
    
    config = toml.load("config.toml")

    """Enter validator's name"""

    moniker = callback.data.split("&")[-1]
    user_id = callback.from_user.id
    data = await state.get_data()

    

    validators = data.get('validators', {})
    logging.debug(f"All mass: {validators}")
    logging.info(f"User: {user_id}. Delete: {moniker}")
    
    del validators[moniker]
 
    await callback.message.edit_text(
        f'Okay, I deleted this checker : {moniker}',
        reply_markup=to_menu()
    )

    logging.info(f"I removed moniker {callback.from_user.id}: {moniker} success ✅\n")
    
    await state.update_data(data)
    await state.set_state(None)



