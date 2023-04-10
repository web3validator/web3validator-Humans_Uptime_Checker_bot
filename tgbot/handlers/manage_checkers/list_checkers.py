import toml, logging


from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.handlers.manage_checkers.router import checker_router
from tgbot.keyboards.inline import menu, to_menu

@checker_router.callback_query(text="list")
async def list_my_validators(callback: CallbackQuery, state: FSMContext):
    """List all registered validators"""

    config = toml.load("config.toml")
    logging.info(f"I display the list on the screen {callback.from_user.id}")

    data = await state.get_data()
    validators = data.get('validators')
    validators_list = list(validators.keys())
    network = config["network"]

    if not validators:
        await callback.answer(
            'Sorry, but I didn\'t find any checker. \n'
            'First, create a checker',
            # show_alert=True
        )

        return

    validators_str = 'I\'m checking the following validators:\n\n'
    validators_str = validators_str + '\n'.join([
        f'{num}. {network} {validator}\n'
        for num, validator in enumerate(validators.keys(), 1)
    ]
    )
    await callback.message.edit_text(validators_str,
                                        reply_markup=to_menu())
    
    logging.info(f"I displayed the list on the screen {callback.from_user.id}: success ✅\n")

    
    
