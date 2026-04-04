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
        
        self.tables = self.recuperer_tables()
        print(self.tables)


        self.afficher_contenu()
        
        print("Contenu de la base de données:", self.contenu_base())

        


    def recuperer_tables(self) -> list:
        """Renvoie la liste contenant le nom de chaque table de la base."""

        # Récupérer les tables du fichier
        self.curseur.execute("SELECT name FROM sqlite_master WHERE type='table'")

        tables = [t[0] for t in self.curseur.fetchall()]
        return tables
    

    def est_valide(self) -> bool:
        """Vérifie si la base de données a un contenu valide et renvoie True si c'est le cas, False sinon.
        Une base de données est considérée comme invalide si elle ne présente pas au minimum les tables 'Master' et 'Internet' et qu'elles ont le contenu attendu."""

        if "Master" and "Internet" in self.tables:
            contenu_master = self.contenu_table("Master")
            assert len(contenu_master) == 1

            contenu_internet = self.contenu_table("Internet")
            for compte in contenu_internet:
                if not all([type(info).__name__ == "str"] for info in compte):
                    return False

            return True
        
        else:
            return False    

    
    def contenu_base(self) -> dict:
        """Renvoie l'intégralité du contenu de la base de données."""
        
        contenu = {}
        
        for table in self.tables:
            contenu[table] = self.contenu_table(table)
        
        return contenu
    
    def contenu_table(self, table:str) -> list:
        """Renvoie l'intégralité du contenu d'une table de la base de données."""
        
        assert table in self.tables, f"La table {table} n'existe pas."
        
        self.curseur.execute(f"SELECT * FROM {table}")
        
        return self.curseur.fetchall()
    

    def afficher_contenu(self) -> None:
        """Affiche dans la console l'intégralité du contenu de la base de données."""
        for table in self.tables:
            print(f"--{table}--")
            self.curseur.execute(f"SELECT * FROM {table}")
            for resultat in self.curseur.fetchall():
                print(resultat)

            print()


    def enregistrer(self) -> None:
        """Enregistre la base de données dans un fichier."""
        self.connexion.commit()


    def fermer_connexion(self) -> None:
        """Ferme la connexion avec la base de données."""
        self.connexion.close()           
