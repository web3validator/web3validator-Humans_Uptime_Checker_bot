import asyncio, toml, json, logging
import math

from aiogram import Bot
from aiogram.dispatcher.fsm.storage.redis import RedisStorage, StorageKey

from tgbot.config import Config

# from aiogram.dispatcher.fsm.context import FSMContext

from schedulers.function import get_keys_redis,check_number_missed_blocks, send_message_user
from schedulers.exceptions import NoSlashingInfo, raise_error
from schedulers.exceptions import raise_error
from funtion import * #, get_index_by_address


async def check_user_node( 
        bot: Bot,
        config: Config,
        storage: RedisStorage,
        ) -> None:

    config_toml = toml.load("config.toml")
    time_repeat = config_toml["time_repeat"]
    allow_missed_block = config_toml["missed_blocks"]
    urls = await check_url()

    if urls["active_urls"] == []:

        for id in config.tg_bot.admin_ids:
            logging.info(id)
            await bot.send_message(
            chat_id=id,
            text=f'RPC not working 🔴, network {config_toml["network"]}',
            )

        return 
    
    url = urls["active_urls"][0]

    keys = get_keys_redis(config)


    for key in keys:
        key = key.split(":")

        bot_id = int(key[1])
        chat_id = int(key[2])
        user_id = int(key[3])
        
        logging.info(f"User: id - {user_id}")

        data = await storage.get_data(bot, StorageKey(bot_id=bot_id, chat_id=chat_id, user_id=user_id))
        list_users = list(data["validators"].keys())
        logging.info(f"Users: {len(list_users)}")


        for moniker in data["validators"].keys():
            logging.info(f"Moniker: {moniker}")

            # validators = await get_validators(url)
            # validator = validators[await get_index_by_moniker(moniker, validators)]
            # signing_info = await slashing_signing_info(validator.get("consensus_pubkey").get("key"), url)
            signing_infos = await slashing_signing_info_all(url)
            signing_info = signing_infos[await get_index_by_consAddr(data["validators"][moniker]["const_addr"], signing_infos)]

            first_snapshot_missed_block = data["validators"][moniker]["last_missed_block"]
            second_snapshot_missed_block = int(signing_info.get("missed_blocks_counter"))

            if check_number_missed_blocks(first_snapshot_missed_block, second_snapshot_missed_block, allow_missed_block):

                await send_message_user(bot=bot, chat_id=chat_id, moniker=moniker, missed_blocks=second_snapshot_missed_block)

            data["validators"][moniker]["last_missed_block"] = second_snapshot_missed_block

        

        data["rpc"] = urls


        await storage.update_data(bot, StorageKey(bot_id=bot_id, chat_id=chat_id, user_id=user_id), data)
        logging.debug(f"Data sheduler: {data}")

