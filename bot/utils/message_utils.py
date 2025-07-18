from aiogram.types import Message

MAX_MESSAGE_LENGTH = 4096

async def send_long_message(message: Message, text: str, *, parse_mode: str = "HTML") -> None:
    """Send *text* splitting into multiple messages if needed."""
    for i in range(0, len(text), MAX_MESSAGE_LENGTH):
        await message.answer(text[i : i + MAX_MESSAGE_LENGTH], parse_mode=parse_mode)
