import asyncio
import logging
import toml


from aiogram import Bot, Dispatcher

from schedulers.base import setup_scheduler
from tgbot.config import load_config
from tgbot.handlers.admin import admin_router
from tgbot.handlers.manage_checkers import checker_router
from tgbot.handlers.user import user_router
from tgbot.middlewares.config import ConfigMiddleware
from aiogram.dispatcher.fsm.storage.redis import RedisStorage, DefaultKeyBuilder, StorageKey
from schedulers.job_new import check_user_node
from tgbot.services import broadcaster


from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime


logger = logging.getLogger(__name__)


async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, 'I\'m running')


def register_global_middlewares(dp: Dispatcher, config):
    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")
    config_toml = toml.load("config.toml")
    time_repeat = config_toml["time_repeat"]

    storage = RedisStorage.from_url(config.redis_config.dsn(), key_builder=DefaultKeyBuilder(with_bot_id=True))


    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    dp = Dispatcher(storage=storage)
    scheduler = setup_scheduler(bot = bot, config = config, storage = storage)
    
    for router in [
        # admin_router,
        user_router,
        checker_router,

        ]:
        dp.include_router(router)

    register_global_middlewares(dp, config)
    dp['bot'] = bot
    # dp['scheduler'] = scheduler

    
    


    await on_startup(bot, config.tg_bot.admin_ids)
    scheduler.start()
    scheduler.add_job(
            check_user_node,
            IntervalTrigger(minutes=time_repeat),
            kwargs={
                'storage': storage,
            },
            next_run_time=datetime.now(),
            replace_existing=True
        )

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('I was stopped')
