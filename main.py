# Programme principal de l'application
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileDialog, QListWidget, QMessageBox
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QAction
import popups.demande_mdp_maitre
import bdd.bdd
import mdp.hash

class FenetreAppli(QMainWindow):
    """Une instance de fenêtre de l'application"""
    def __init__(self):
        # Hériter des attributs du parent QMainWindow
        super().__init__()
        
        # Disposition verticale des widgets
        self.parentLayout = QVBoxLayout()
        
        # Dimensions minimales de la fenêtre
        self.setMinimumSize(800,600)
        
        # Titre de la fenêtre
        self.setWindowTitle("Gestionnaire de mots de passe")
        
        # Barre de menus de l'application
        self.barre_menus = self.menuBar()
        
        # Menu "Fichier"
        self.menu_fichier = self.barre_menus.addMenu("Fichier")
        
        # Définir les actions du menu "Fichier"
        creer_base = QAction("Nouvelle base de données", self)
        creer_base.setShortcut("Ctrl+N")
        self.menu_fichier.addAction(creer_base)
        creer_base.triggered.connect(self.creer_base)
        
        ouvrir_base = QAction("Ouvrir une base de données", self)
        ouvrir_base.setShortcut("Ctrl+O")
        ouvrir_base.triggered.connect(self.ouvrir_base)
        self.menu_fichier.addAction(ouvrir_base)

        enregistrer_base = QAction("Enregistrer", self)
        enregistrer_base.setShortcut("Ctrl+S")
        self.menu_fichier.addAction(enregistrer_base)

        enregistrer_sous = QAction("Enregistrer sous", self)
        enregistrer_sous.setShortcut("Ctrl+Shift+S")
        enregistrer_sous.triggered.connect(self.enregistrer_sous)
        self.menu_fichier.addAction(enregistrer_sous)
        
        quitter_app = QAction("Quitter", self)
        quitter_app.setShortcut("Ctrl+Q")
        quitter_app.triggered.connect(self.close)
        self.menu_fichier.addAction(quitter_app)
        
        self.liste_entrees = QListWidget()
        self.parentLayout.addWidget(self.liste_entrees)

        # Widget central de la fenêtre
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.parentLayout)
        self.setCentralWidget(self.centralWidget)

        # Obtenir la liste des hashs de mots de passe maîtres
        self.hashs_maitres = mdp.hash.obtenir_hashs_maitres()
        print("Hashs maîtres :", self.hashs_maitres)

        # Base de données actuellement ouverte
        self.base = None


        

    def enregistrer_sous(self) -> None:
        """Enregistre la base de données actuelle dans un nouveau fichier."""

        # Si une base de données est actuellement ouverte
        if self.base is not None:

            nouveau_fichier, _ = QFileDialog.getSaveFileName(self, "Enregistrer sous", "", "Base de données SQL (*.db)")
            db = bdd.bdd.BDD(nouveau_fichier)
            db.maj_contenu(self.base.contenu)
            self.base = db

            self.setWindowTitle(nouveau_fichier)

        else:
            self.creer_base()



    def ouvrir_base(self) -> None:
        """Affiche un dialogue pour ouvrir une base de données."""

        dialogue_fichier = QFileDialog(self, "Ouvrir une base de données", "", "Base de données SQL (*.db)")

        resultat = dialogue_fichier.exec()

        if resultat:

            popup_mdp_maitre = popups.demande_mdp_maitre.DemandeMdp(titre_fenetre="Mot de passe maître", hashes=self.hashs_maitres["hashes"], mode="validation")
            popup_mdp_maitre.exec()
            fichier_selectionne = dialogue_fichier.selectedFiles()[0]
            self.base = bdd.bdd.BDD(fichier_selectionne)

            if not self.base.est_valide():
                reponse = QMessageBox.warning(self, "Base de données invalide", 
                                    """Cette base de données possède une structure innatendue. Vous devrez la réinitialiser afin de l'utiliser comme base de données de mots de passe. \n ATTENTION: RÉINITIALISER LA BASE DE DONNÉES VA SUPPRIMER L'INTÉGRALITÉ DE SON CONTENU. \n
                                    Procéder à la réinitialisation ?""",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                
                if reponse:
                    print("Réinitialisation...")
                    self.base.reinitialiser()

                else:
                    print("Annulé !")

            self.actualiser_liste_entrees("Internet")        
                


        

    def actualiser_liste_entrees(self, table:str) -> None:
        """Actualise la liste d'entrées afin d'afficher le contenu de la table indiquée."""

        contenu_table = self.base.contenu_table(table)

        self.liste_entrees.clear() # Supprimer les entrées précédentes

        for compte in contenu_table:
            infos = [str(info) + "|" for info in compte]
            self.liste_entrees.addItem(str(infos)) 

            


    def creer_base(self) -> None:
        """Crée une nouvelle base de données de mots de passe."""

        popup_mdp_maitre = popups.demande_mdp_maitre.DemandeMdp(titre_fenetre="Mot de passe maître", hashes=[], mode="creation")

        popup_mdp_maitre.exec()

        
        mdp_maitre = popup_mdp_maitre.obtenir_mdp() # Obtenir le mot de passe maître saisi par l'utilisateur
        print(f"Mot de passe maître: {mdp_maitre}")
        print(f"Hash du mot de passe maître: {mdp.hash.hash_mdp(mdp_maitre)}")
        hash_mdp = mdp.hash.hash_mdp(mdp_maitre)

        

        # Choisir le dossier d'enregistrement
        nouveau_fichier, _ = QFileDialog.getSaveFileName(self, "Enregistrer la nouvelle base de données", "", "Base de données SQL (*.db)")
        
        if nouveau_fichier:
            print(f"Fichier choisi : {nouveau_fichier}")

            self.base = bdd.bdd.BDD(nouveau_fichier)
            self.base.enregistrer() # Enregistrer la base de données dans un fichier
            self.hashs_maitres["hashes"].append(hash_mdp)
            mdp.hash.enregistrer_hashs_maitres(self.hashs_maitres)







# Créer l'application
app = QApplication([])
fenetre = FenetreAppli()
fenetre.show()
app.exec()