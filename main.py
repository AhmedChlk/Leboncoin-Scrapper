import asyncio
from aiogram import Bot, Dispatcher
import infra.logger  # noqa: F401
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from bot.config import TOKEN
from bot.handlers import register_handlers

async def main():
    if TOKEN is None:
        raise ValueError("Le TOKEN du bot Telegram n'est pas défini.")
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    register_handlers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
