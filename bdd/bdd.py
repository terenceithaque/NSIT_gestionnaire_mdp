"""bdd.py contient une classe BDD représentant une base de données SQLite de mots de passe."""
import sqlite3


class BDD:
    """Une base de données SQLite contenant des mots de passe."""
    def __init__(self, fichier="new_file.db"):
        
        self.fichier = fichier # Fichier de la base de données
        print(self.fichier)

        # Connexion à la base de données
        self.connexion = sqlite3.Connection(self.fichier)
        self.curseur = self.connexion.cursor()

        # Récupérer toutes les tables du fichier
        self.curseur.execute("SELECT name FROM sqlite_master WHERE type='table'")

        self.tables = self.curseur.fetchall()

        print(self.tables)