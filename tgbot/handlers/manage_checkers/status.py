import logging
from datetime import datetime
from socket import EAI_SERVICE
import asyncio, toml
import json
from termcolor import colored

from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

# from api.config import nodes
# from api.functions import get_index_by_moniker
# from api.requests import MintScanner
# from schedulers.jobs import add_user_checker
from tgbot.handlers.manage_checkers.router import checker_router
from tgbot.misc.states import Status
from tgbot.keyboards.inline import validator_moniker
from tgbot.keyboards.inline import menu, list_validators, to_menu

import os
from funtion import *




    
@checker_router.callback_query(text="status")
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
            "The status of which validator do you want to know?",
            reply_markup=list_validators(validators_list, "status")
        )
    
    




@checker_router.callback_query(Text(text_startswith="status&"))
async def enter_operator_address(callback: CallbackQuery, state: FSMContext):
    config = toml.load('config.toml')


    """Enter validator's name"""
    moniker = callback.data.split("&")[-1]
    logging.info(f"I display the status on the screen {callback.from_user.id}")

    data = await state.get_data()
    urls = await check_url()
    active_rpc = urls["numer_active"]
    number_rpc = urls["urls"]

    if urls["active_urls"] == []:
        await callback.answer(
        f'Sorry, rpc not working 🔴',
        show_alert=True, 
    )
        return

    url = urls["active_urls"][0]
    # url = data["rpc"]["active_urls"][0]

    


    validators = await get_validators(url)
    index = await get_index_by_moniker(moniker, validators)

    logging.info(f"Moniker: {moniker}. Index: {index}")
    validator = validators[await get_index_by_moniker(moniker, validators)]
    signing_info = await slashing_signing_info(validator.get("consensus_pubkey").get("key"), url)
    missed_block = signing_info["missed_blocks_counter"]



    jail = '🔴 true' if validator["jailed"] else '🟢 false'
    status = '🟢 BONDED' if validator["status"] == "BOND_STATUS_BONDED" else '🔴 UNBONDED'


    await callback.answer(
        f'status: '
        f'\n    moniker: {moniker}'
        f'\n    voting power: {validator["tokens"]}'
        f'\n    jailed:  {jail}'
        f'\n    validators status: {status}'
        f'\n    missed blocks: {missed_block}',
        show_alert=True, 
    )

    logging.info(f"I displayed the status on the screen {callback.from_user.id}: success ✅\n")

