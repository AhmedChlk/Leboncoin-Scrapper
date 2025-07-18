"""
Module utilitaire pour nettoyer les données de scraping
"""

from pathlib import Path
import os
import glob
import logging
from core.constants import DATA_DIR, EXPORTS_DIR

logger = logging.getLogger(__name__)

def cleanup_ads_data():
    """
    Supprime tous les fichiers ads_*.json du répertoire de données
    """
    data_dir = DATA_DIR

    if not data_dir.exists():
        logger.info("Répertoire de données n'existe pas, rien à nettoyer")
        return 0
    
    # Supprimer tous les fichiers ads_*.json
    files_to_delete = list(data_dir.glob("ads_*.json"))
    
    deleted_count = 0
    for file_path in files_to_delete:
        try:
            file_path.unlink()
            deleted_count += 1
            logger.info(f"Fichier supprimé: {file_path}")
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de {file_path}: {e}")
    
    logger.info(f"Nettoyage terminé: {deleted_count} fichiers supprimés")
    return deleted_count

def get_ads_files_count() -> int:
    """Return the number of ads files present in ``DATA_DIR``."""
    data_dir = DATA_DIR

    if not data_dir.exists():
        return 0

    return len(list(data_dir.glob("ads_*.json")))

def cleanup_exports() -> int:
    """Remove every file from the export directory."""
    exports_dir = EXPORTS_DIR

    if not exports_dir.exists():
        logger.info("Répertoire exports n'existe pas, rien à nettoyer")
        return 0
    
    deleted_count = 0
    for file_path in exports_dir.iterdir():
        if file_path.is_file():
            try:
                file_path.unlink()
                deleted_count += 1
                logger.info(f"Fichier export supprimé: {file_path}")
            except Exception as e:
                logger.error(f"Erreur lors de la suppression de {file_path}: {e}")
    
    logger.info(f"Nettoyage des exports terminé: {deleted_count} fichiers supprimés")
    return deleted_count
