import asyncio
import json
import logging
import environs
import math

from aiogram import Bot
from aiogram.dispatcher.fsm.storage.redis import RedisStorage


# from api.requests import MintScanner
from schedulers.exceptions import NoSlashingInfo, raise_error
from schedulers.exceptions import raise_error
from funtion import get_index_by_moniker #, get_index_by_address

# from name_node import skipped_blocks_allowed, time_jail, name

env = environs.Env()
env.read_env()
ADMIN_ID = env.str("ADMINS")


def two_zero(integer):
    if integer < 10:
        return "0" + str(integer)

    else:
        return integer






async def sends_message_client(bot: list, user_id: int | str, moniker: str, 
                percentages: int , skipped_blocks_allowed: int, time_to_jail: int, missed_blocks_counter_new: int):

                if not missed_blocks_counter_new:
        
                    return

                elif percentages > (skipped_blocks_allowed * 0.7):
                    await bot.send_message(user_id, f"<b>Moniker: {moniker}.</b>"
                                        f"\n<b>I've just found {percentages} missed blocks out of {skipped_blocks_allowed} total.</b>"
                                        f"\n<b>You have ~{ two_zero( math.floor(time_to_jail / 60) ) }:{ two_zero( time_to_jail % 60 ) } hours before jailing.</b>"
                                        f"\n <b>If you don't fix it, your validator will go to jail.</b>")

                else:
                    await bot.send_message(user_id, f"<b>Moniker: {moniker}.</b>"
                                        f"\nI've just found {percentages} missed blocks out of {skipped_blocks_allowed} total."
                                        f"\nYou have ~ { two_zero( math.floor(time_to_jail / 60) ) }:{ two_zero( time_to_jail % 60 ) } hours before jailing.")

async def add_user_checker(bot: Bot, mint_scanner: MintScanner, #user_id: int, platform: str, moniker: str,
                           storage: RedisStorage):
    logging.info('Я почав розсилку')


    async def check_block(old_new, new):
        logging.debug(f"old_new {old_new}")
        if old_new >= 28:
            return 1
        else:
            #checkers[str(user_id)][platform][moniker]['last_check'] = new
            return 0

    async def check(old, new):
        right_blocks = await check_block(new - old, new)
        logging.debug(f"right_blocks {right_blocks}")
        if right_blocks:
            old = checkers.get('validators')[str(user_id)][moniker]['last_check']
            # rizn = new - old
            vidsot_skip_blok = (100 * new) / skipped_blocks_allowed
            vidsot_time_to_jail = (
                ((100 - vidsot_skip_blok) * time_jail) / 100) / 60
            # return right_blocks, round(vidsot_skip_blok, 2), round(vidsot_time_to_jail)
            return right_blocks, new, round(vidsot_time_to_jail)
        else:
            return 0, 0, 0


    stake=[]

    all_cons_validators_one =None
    checkers = await storage.redis.get('checkers') or '{}'
    checkers = json.loads(checkers)
    # logging.info(f'{checkers}')

    
            



    if checkers == {}: 
        logging.info("Масив пустий {}")
        logging.info("Я закінчив роз силку")
        
        await storage.redis.set('checkers', json.dumps(checkers))
        return

    else:
        for id in checkers.get('validators'):
            for val in checkers.get('validators')[id]:
                if checkers.get('validators')[id][val]["addr_cons"] is None and len(stake) < 2*2:
                    stake.append(id)
                    stake.append(val)
        
        for user_id in checkers['validators']:
            for moniker in checkers['validators'][user_id]:
                logging.info(f'Оброблюється {user_id} {moniker}')
                

                if checkers['validators'].get(str(user_id)).get(moniker).get('addr_cons') is None and user_id in stake and moniker in stake:
                
                    # last_check = checkers[str(user_id)].get(moniker, {}).get('last_check', 0)
                    # data = await mint_scanner.get_repeated_missing_blocks(name, checkers[str(user_id)].get(moniker).get('cons_key'))
                    if checkers.get('all_missed') is None:
                        data = await mint_scanner.parse_application(name, moniker)
                        # logging.debug(f"data: {data}")
                        checkers['all_missed'] = data['data']['validators']


                        logging.debug(f'checkers["all_missed"] add validators_list {data["data"]["validators"][get_index_by_moniker(moniker, data["data"]["validators"])]}')
                        logging.info(f"Get missed_blocks_counter, validators, missed_blocks_counter ")

                        if not data['ok']:
                            await bot.send_message(ADMIN_ID, "Error happened: " + data['error'] + "\n\n" + f'{moniker=}, {name=}')
                            raise raise_error(data['error'])

                        missed_blocks_counter = data['missed_blocks_counter']

                        logging.info(f"Missed blocks counter {moniker} : {missed_blocks_counter} first")

                    else:
                        data = await mint_scanner.get_repeated_missing_block(name, checkers['all_missed'][(get_index_by_moniker(moniker, checkers['all_missed']))].get('consensus_pubkey').get('key'))
                        missed_blocks_counter = int(data['missed_blocks_counter']['missed_blocks_counter'])

                        logging.info(f"Missed blocks counter {moniker} : {missed_blocks_counter} second")



                    
                    logging.info(f'Sleeping for 180 seconds ')
                    await asyncio.sleep(180)
                    data_new = await mint_scanner.get_repeated_missing_block(name, checkers['all_missed'][get_index_by_moniker(moniker, checkers['all_missed'])].get("consensus_pubkey").get('key'))
                    checkers['validators'][user_id][moniker]['addr_cons'] = data_new['missed_blocks_counter']['address']
                    missed_blocks_counter_new = int(data_new['missed_blocks_counter']['missed_blocks_counter'])

                    logging.debug(f" old_rezult {type(missed_blocks_counter)} , new_rezult {type(missed_blocks_counter_new)}")
                    logging.info(f'{data_new}')

                    logging.info(f"Get second missed blocks counter {moniker}: {missed_blocks_counter_new} rizn {missed_blocks_counter_new - missed_blocks_counter}")

                    missed_blocks_counter_new, percentages, time_to_jail = await check( missed_blocks_counter, missed_blocks_counter_new )

                    logging.debug(f"missed_blocks: {missed_blocks_counter_new}, percentages: {percentages}, time_to_jail: {time_to_jail} ")

                    await sends_message_client(bot, user_id, moniker, percentages, skipped_blocks_allowed, time_to_jail, missed_blocks_counter_new)
                    
                elif checkers['validators'].get(str(user_id)).get(moniker).get('addr_cons') is not None:
                    logging.info("cons_true")
                    if all_cons_validators_one is None:
                        all_cons_validators_one = await mint_scanner.get_repeated_missing_blocks(name, checkers.get('validators').get(str(user_id)).get(moniker).get('addr_cons'))
                        
                        logging.info(f'Sleeping for 180 const')
                        await asyncio.sleep(180)
                        all_cons_validators_second = await mint_scanner.get_repeated_missing_blocks(name, checkers.get('validators').get(str(user_id)).get(moniker).get('addr_cons'))

                    logging.debug(f" const: {checkers['validators'][str(user_id)][moniker]['addr_cons']}")
                    index = get_index_by_address(checkers['validators'][str(user_id)][moniker]['addr_cons'],
                                                all_cons_validators_one['missed_blocks_counters'])
                    logging.info(f"index cons_validators: {index}")

                    cons_val_one = int(all_cons_validators_one['missed_blocks_counters'][index].get('missed_blocks_counter'))
                    #cons_val_one = 130
                    logging.info(f"Missed blocks counter {moniker} : {cons_val_one} const")

                    cons_val_two = int(all_cons_validators_second['missed_blocks_counters'][index].get('missed_blocks_counter'))
                    logging.info(f"Second Missed blocks counter {moniker} : {cons_val_two} const")

                    missed_blocks_counter_new, percentages, time_to_jail = await check( cons_val_one, cons_val_two )

                    await sends_message_client(bot, user_id, moniker, percentages, skipped_blocks_allowed, time_to_jail, missed_blocks_counter_new)
                    
                    # if checkers.get('all_missed') is None:
                    #     data = await mint_scanner.parse_application(name, moniker)
                    #     checkers['all_missed'] = data['data']['validators']

                    # if not data['ok']:
                    #     await bot.send_message(ADMIN_ID, "Error happened: " + data['error'] + "\n\n" + f'{moniker=}, {name=}')
                    #     raise raise_error(data['error'])

                    # missed_blocks_counter = data['missed_blocks_counter']
                    # consensus_pubkey = data['data']['consensus_pubkey']

        checkers['all_missed'] = None
        checkers['miss_all_blocks'] = None
        logging.info(f"Я закінчив роз силку full \n{checkers}\n")
        await storage.redis.set('checkers', json.dumps(checkers))
    
async def proposals(bot: Bot, mint_scanner: MintScanner, #user_id: int, platform: str, moniker: str,
                           storage: RedisStorage):
                           pass