from aiogram.types import Message



async def start_cmd(message: Message):
    await message.answer(
        "✅ <b>Bienvenue sur ton bot !</b>\nTape /amazon ou /cdiscount",
        parse_mode="HTML",
    )
