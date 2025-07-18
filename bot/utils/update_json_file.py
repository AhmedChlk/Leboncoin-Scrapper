import json
import os


class FileNotFoundErrorCustom(Exception):
    """Raised when the JSON file does not exist."""


class KeyNotFoundError(Exception):
    """Raised when the given key is missing from the JSON file."""



def update_json_file(path: str, key: str, new_value: str) -> None:
    """Update *key* in the JSON file at *path* with *new_value*."""
    if not os.path.exists(path):
        raise FileNotFoundErrorCustom(f"Le fichier {path} n'a pas été trouvé.")

    # Charge le contenu JSON
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Vérifie si la clé existe
    if key not in data:
        raise KeyNotFoundError(f"La clé '{key}' n'existe pas dans le fichier JSON.")

    # Modifie la valeur
    data[key] = new_value

    # Sauvegarde les modifications
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
