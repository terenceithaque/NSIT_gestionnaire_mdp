"""bdd.py contient une classe BDD représentant une base de données SQLite de mots de passe."""
import sqlite3
import os
import mdp.hash

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

        # La table actuelle représente la table sur laquelle l'utilisateur travaille actuellement
        if len(self.tables) > 0:
            self.table_actuelle = self.tables[0]

        else:
            self.table_actuelle = ""    


        self.afficher_contenu()
        
        self.contenu = self.contenu_base() # Contenu de la base de données

        self.est_enregistree = True # Variable permettant de suivre l'état d'enregistrement de la base de données


    def fichier_existant(self) -> bool:
        """Renvoie True si le fichier de la base de données existe, False sinon."""
        return os.path.exists(self.fichier)
    
    
    def maj_master(self, mot_de_passe:str) -> None:
        """Met à jour la table Master contenant le hash du mot de passe maître."""
        self.curseur.execute(f"""UPDATE Master SET MasterMdp='{mdp.hash(mot_de_passe)};'""")
    

    def creer_table(self, table:str) -> None:
        """Crée une nouvelle table dans la base de données."""

        self.curseur.execute(f"""CREATE TABLE '{table}'
                            (id INTEGER PRIMARY KEY,
                            nomEntree TEXT,
                            nomUtil TEXT,
                            email TEXT);
                             """)

        self.tables = self.recuperer_tables() # Mettre à jour la liste des tables
        self.contenu = self.contenu_base() # Mettre à jour le contenu de la base

        self.est_enregistree = False 
    

    def reinitialiser(self) -> None:
        """Supprime l'intégralité des tables existantes de la base de données et crée la structure nécessaire pour traiter une base de données de mots de passe."""

        # Supprimer toutes les tables
        for table in self.tables:
            self.curseur.execute(f"DROP TABLE {table};")


        # Créer les tables 'Master' et 'Internet'
        self.curseur.execute("""CREATE TABLE Master (
                             MasterMdp TEXT NOT NULL)""")

        self.curseur.execute(f"""CREATE TABLE Internet (
                             id EntryID PRIMARY KEY,
                             nomEntree TEXT,
                             nomUtil TEXT,
                             email TEXT)""")    

        self.tables = self.recuperer_tables()
        self.enregistrer() # Enregistrer les modifications

    def changer_table_actuelle(self, table:str) -> None:
        """Change la table actuelle de la base de données pour celle donnée en paramètres."""

        assert table in self.tables, f"La table {table} n'existe pas"

        self.table_actuelle = table

    def recuperer_tables(self) -> list:
        """Renvoie la liste contenant le nom de chaque table de la base."""

        # Récupérer les tables du fichier
        self.curseur.execute("SELECT name FROM sqlite_master WHERE type='table'")

        tables = [t[0] for t in self.curseur.fetchall()]
        return tables
    
    def maj_contenu(self, contenu:dict) -> None:
        """Met à jour le contenu de la base de données en utilisant le dictionnaire donné en paramètre."""
        self.contenu = contenu


    def ajouter_entree(self, entree:dict) -> None:
        """Crée une nouvelle entrée dans la table actuelle."""
        
        self.curseur.execute(f"""INSERT INTO {self.table_actuelle} VALUES ({self.generer_id(self.table_actuelle)}, '{entree["titreEntree"]}', '{entree["nomUtil"]}', '{entree["mdp"]}')""")

        self.est_enregistree = False


    def est_valide(self) -> bool:
        """Vérifie si la base de données a un contenu valide et renvoie True si c'est le cas, False sinon.
        Une base de données est considérée comme invalide si elle ne présente pas au minimum les tables 'Master' et 'Internet' et qu'elles ont le contenu attendu."""

        if "Master" and "Internet" in self.tables:
            contenu_master = self.contenu_table("Master")
            assert 0 <= len(contenu_master) <= 1

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
    

    def generer_id(self, table:str) -> int:
        """Génère l'ID d'un élément pouvant être enregistré dans la table donnée. Cet ID correspond au nombre d'entrées dans la table en additionnant 1."""

        nb_entrees = len(self.contenu_table(table)) # Récupérer le nombre d'entrées de la table
        return nb_entrees + 1

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
        self.est_enregistree = True


    def fermer_connexion(self) -> None:
        """Ferme la connexion avec la base de données."""
        self.connexion.close()           
