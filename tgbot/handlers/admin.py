from aiogram import Router
from aiogram.types import Message

from tgbot.filters.admin import AdminFilter
from tgbot.keyboards.inline import menu

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(commands=["start"], state="*")
async def admin_start(message: Message):
    await message.reply("Hello, admin!", reply_markup= menu())
    