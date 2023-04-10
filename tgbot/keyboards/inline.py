from distutils.command.build import build
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="create checker 📝", callback_data="create")
    builder.button(text="list 📋", callback_data="list")
    builder.button(text="delete checker 🗑", callback_data="delete")
    builder.button(text="status", callback_data="status")
#    builder.button(text="gov", callback_data="gov")
    builder.adjust(2)

    return builder.as_markup()

def validator_moniker(validator_moniker):

    builder = InlineKeyboardBuilder()
    for num in len(validator_moniker) :
        builder.add( text=validator_moniker[num], callback_data=num )

    return builder.as_markup()


def to_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="Menu", callback_data="menu")
    builder.adjust(1)
    return builder.as_markup()

def list_validators(validarots: list, func: str):
    builder = InlineKeyboardBuilder()
    for num in range(len(validarots)):
        builder.add( InlineKeyboardButton(text=validarots[num], callback_data=f"{func}&{validarots[num]}") )
    builder.adjust(4)
    builder.row(InlineKeyboardButton(text="Menu", callback_data="menu"))
    
    return builder.as_markup()
