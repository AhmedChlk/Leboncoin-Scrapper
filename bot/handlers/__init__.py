from aiogram.filters import Command
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.handlers.start import start_cmd
from bot.handlers.help import help_cmd
from bot.handlers.search.search_cmd import search_cmd
from bot.handlers.filter.filter_cmd import filter_cmd, stats_cmd, chart_cmd
from bot.handlers.export.export_cmd import export_cmd, export_callback
from bot.handlers.cleanup_cmd import cleanup_cmd


class ErrorHandlerMiddleware:
    async def __call__(self, handler, event, data):
        try:
            return await handler(event, data)
        except Exception as e:
            print(f"[ERREUR] {type(e).__name__}: {e}")
            if isinstance(event, types.Message):
                await event.reply(
                    "❌ Une erreur inattendue est survenue. Merci de réessayer ou de contacter l'administrateur."
                )
            return None


async def welcome_cmd(message: types.Message):
    """Commande de démarrage avec bouton d'aide"""
    welcome_text = (
        "🤖 <b>Bienvenue sur le Bot de Scraping & Analyse d'Annonces !</b>\n\n"
        "Ce bot vous permet de :\n"
        "• 🔍 Scraper des annonces (Leboncoin, etc.)\n"
        "• 📊 Analyser les données (prix, marques, villes)\n"
        "• 📈 Générer des graphiques\n"
        "• 🔧 Filtrer selon vos critères\n\n"
        "Cliquez sur le bouton ci-dessous pour voir toutes les commandes disponibles :"
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="📚 Aide & Commandes", callback_data="show_help")]]
    )
    await message.reply(welcome_text, reply_markup=keyboard)


async def help_callback(callback: types.CallbackQuery):
    """Gère le clic sur le bouton d'aide"""
    from bot.handlers.help import generate_help_text

    help_text = generate_help_text()
    await callback.message.answer(help_text, parse_mode="HTML")
    await callback.answer()


def register_handlers(dp):
    dp.message.middleware(ErrorHandlerMiddleware())
    dp.message.register(welcome_cmd, Command("start"))
    dp.message.register(help_cmd, Command("help"))
    dp.callback_query.register(help_callback, lambda c: c.data == "show_help")
    dp.message.register(search_cmd, Command("search"))
    dp.message.register(filter_cmd, Command("filter"))
    dp.message.register(stats_cmd, Command("stats"))
    dp.message.register(chart_cmd, Command("chart"))
    dp.message.register(export_cmd, Command("export"))
    dp.message.register(cleanup_cmd, Command("cleanup"))
    dp.callback_query.register(export_callback, lambda c: c.data.startswith("export_"))
