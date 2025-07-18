from aiogram.types import Message
from pathlib import Path
from core.scraping import scrape_ads
from core.constants import DATA_DIR

async def search_cmd(message: Message):
    if not message.text:
        await message.reply(
            "⚠️ <b>Usage</b> : /search &lt;url&gt; &lt;nombre_de_pages&gt;",
            parse_mode="HTML",
        )
        return
    
    try:
        _, url, page = message.text.split(maxsplit=2)
        page_int = int(page)
    except ValueError:
        await message.reply(
            "⚠️ <b>Usage</b> : /search &lt;url&gt; &lt;nombre_de_pages&gt;",
            parse_mode="HTML",
        )
        return
    
    # Supprimer les anciennes données avant de commencer le nouveau scraping
    data_dir = DATA_DIR
    if data_dir.exists():
        # Supprimer tous les fichiers ads_*.json
        files_to_delete = list(data_dir.glob("ads_*.json"))
        
        if files_to_delete:
            deleted_count = 0
            for file_path in files_to_delete:
                try:
                    file_path.unlink()
                    deleted_count += 1
                except Exception as e:
                    print(f"Erreur lors de la suppression de {file_path}: {e}")
            
            await message.reply(
                f"🗑️ {deleted_count} anciens fichiers supprimés. Début du nouveau scraping...",
                parse_mode="HTML",
            )
        else:
            await message.reply("🔄 Début du scraping...", parse_mode="HTML")
    else:
        data_dir.mkdir(parents=True, exist_ok=True)
        await message.reply(
            "🔄 Création du répertoire de données et début du scraping...",
            parse_mode="HTML",
        )
    
    # Lancer le scraping
    count = len(scrape_ads(url, page_int))
    if count:
        await message.reply(
            f"✅ <b>Recherche terminée</b> : {count} annonces trouvées pour {page_int} pages",
            parse_mode="HTML",
        )
    else:
        await message.reply(
            "❌ Aucune annonce trouvée. Vérifie l'URL ou réessaie plus tard.",
            parse_mode="HTML",
        )