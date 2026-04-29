"""copie_temp.py permet de faire une copie temporaire d'un élément dans le presse-papiers"""
import pyperclip
from concurrent.futures import ThreadPoolExecutor
import time


executeur = ThreadPoolExecutor(max_workers=1)


def copie_temporaire(texte:str, delai:int) -> None:
    """Copie l'élement fourni dans le presse-papiers, attend, puis vide le presse-papiers."""
    pyperclip.copy(texte)
    time.sleep(delai)
    pyperclip.copy("") # Effacer le contenu du presse-papiers


def copie_timeout(texte:int, delai=12)  -> None:
    """Effectue une copie temporaire d'un élément dans une tâche parallèle."""
    executeur.submit(copie_temporaire, texte, delai)
      