# Programme principal de l'application
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileDialog, QListWidget, QMessageBox, QDialog
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QAction
import popups.demande_mdp_maitre
import popups.nouveau_mdp
import popups.creation_groupe
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
        enregistrer_base.triggered.connect(self.enregistrer)
        self.menu_fichier.addAction(enregistrer_base)

        enregistrer_sous = QAction("Enregistrer sous", self)
        enregistrer_sous.setShortcut("Ctrl+Shift+S")
        enregistrer_sous.triggered.connect(self.enregistrer_sous)
        self.menu_fichier.addAction(enregistrer_sous)
        
        quitter_app = QAction("Quitter", self)
        quitter_app.setShortcut("Ctrl+Q")
        quitter_app.triggered.connect(self.quitter)
        self.menu_fichier.addAction(quitter_app)
        
        # Menu "Entrées"
        self.menu_entrees = self.barre_menus.addMenu("Entrées")
        ajouter_entree = QAction("Nouvelle entrée", self)
        ajouter_entree.setShortcut("Ctrl+E")
        ajouter_entree.triggered.connect(self.nouveau_mdp)
        self.menu_entrees.addAction(ajouter_entree)
        
        # Menu "Groupes"
        self.menu_groupes = self.barre_menus.addMenu("Groupes")
        # Ajouter l'action de création d'un groupe
        creer_groupe = QAction("Créer un groupe", self)
        creer_groupe.setShortcut("Ctrl+G")
        creer_groupe.triggered.connect(self.creer_groupe)
        self.menu_groupes.addAction(creer_groupe)
        
        
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


    def nouveau_groupe(self) -> None:
        """Permet à l'utilisateur de créer une nouvelle table dans la base de données."""
        popup_creation_groupe = popups.creation_groupe.DemandeCreerGroupe()

        resultat = popup_creation_groupe.exec()

        if resultat and popup_creation_groupe.nom_groupe_valide:
            table = popup_creation_groupe.champ_nom_groupe.text()
            self.base.creer_table(table)
            self.base.changer_table_actuelle(table)
            self.changer_table_actuelle(table)


    def enregistrer(self) -> None:
        """Enregistre la base de données actuelle dans son fichier."""
        
        if self.base is not None:
            # Si le fichier de la base de données a déjà été créé, le mettre à jour
            if self.base.fichier_existant():
                self.base.enregistrer()

            # Sinon, demander à l'utilisateur où enregistrer la base
            else:
                self.enregistrer_sous()

    
    def nouveau_mdp(self) -> None:
        """Demande à l'utilisateur de saisir un mot de passe à ajouter dans la base de données."""

        popup_nouveau_mdp = popups.nouveau_mdp.DemandeNouveauMdp()
        resultat = popup_nouveau_mdp.exec()

        if resultat == QDialog.DialogCode.Accepted:
            donnees_entree = popup_nouveau_mdp.obtenir_entrees()
            print("Données de l'entrée :", donnees_entree)
            self.base.ajouter_entree(donnees_entree)
            self.actualiser_liste_entrees(self.base.table_actuelle)

        else:
            print("Création de l'entrée annulée")    


    def creer_groupe(self) -> None:
        """Demande à l'utilisateur le nom d'un groupe et le crée."""

        popup_creation_groupe = popups.creation_groupe.DemandeCreerGroupe()
        resultat = popup_creation_groupe.exec()

        if resultat == QDialog.DialogCode.Accepted and popup_creation_groupe.nom_groupe_valide:
            table = popup_creation_groupe.champ_nom_groupe.text()
            self.base.creer_table(table)
            self.base.changer_table_actuelle(table)
            self.changer_table_actuelle(table)

        else:
            print("Création du groupe annulée")    

    
    def changer_table_actuelle(self, table:str) -> None:
        """Change la table de la base de données actuellement affichée par celle donnée en paramètre."""
        self.base.changer_table_actuelle(table)
        self.actualiser_liste_entrees(self.base.table_actuelle)
        self.setWindowTitle(f"{self.base.fichier} | {self.base.table_actuelle}")

            

    
    def actualiser_menu_groupes(self):
        """Actualise le menu 'Groupes' afin d'y afficher les tables de la base de données actuellement ouverte."""
        
        self.menu_groupes.clear() # Supprimer tous les boutons du menu "Groupes"
        # Ajouter l'action de création d'un groupe
        creer_groupe = QAction("Créer un groupe", self)
        creer_groupe.setShortcut("Ctrl+G")
        self.menu_groupes.addAction(creer_groupe)
        
        self.menu_groupes.addSeparator()
        
        for table in self.base.tables:
            action_table = QAction(table, self)
            print(table, type(table))
             
            # ⚠️ capture correcte de la variable
            action_table.triggered.connect(
                lambda checked, t=table: self.changer_table_actuelle(t)
            )
            
            self.menu_groupes.addAction(action_table)
            
        
        
    def ouvrir_base(self) -> None:
        """Affiche un dialogue pour ouvrir une base de données."""

        dialogue_fichier = QFileDialog(self, "Ouvrir une base de données", "", "Base de données SQL (*.db)")

        resultat = dialogue_fichier.exec()

        if resultat:

            popup_mdp_maitre = popups.demande_mdp_maitre.DemandeMdp(titre_fenetre="Mot de passe maître", hashes=self.hashs_maitres["hashes"], mode="validation")
            resultat_mdp = popup_mdp_maitre.exec()


            if resultat_mdp == QDialog.DialogCode.Accepted:
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

            else:
                print("Ouverture de la base de données annulée")            

            if self.base is not None:
                self.actualiser_liste_entrees("Internet")
                self.actualiser_menu_groupes()
                


        

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

        resultat = popup_mdp_maitre.exec()

        if resultat == QDialog.DialogCode.Accepted:
            mdp_maitre = popup_mdp_maitre.obtenir_mdp() # Obtenir le mot de passe maître saisi par l'utilisateur
            print(f"Mot de passe maître: {mdp_maitre}")
            print(f"Hash du mot de passe maître: {mdp.hash.hash_mdp(mdp_maitre)}")
            hash_mdp = mdp.hash.hash_mdp(mdp_maitre)



            # Choisir le dossier d'enregistrement
            nouveau_fichier, _ = QFileDialog.getSaveFileName(self, "Enregistrer la nouvelle base de données", "", "Base de données SQL (*.db)")
            
            if nouveau_fichier:
                print(f"Fichier choisi : {nouveau_fichier}")

                self.base = bdd.bdd.BDD(nouveau_fichier)
                self.base.reinitialiser()
                self.base.changer_table_actuelle("Internet")
                self.changer_table_actuelle("Internet")
                self.base.enregistrer() # Enregistrer la base de données dans un fichier
                self.hashs_maitres["hashes"].append(hash_mdp)
                mdp.hash.enregistrer_hashs_maitres(self.hashs_maitres)

        else:
            print("Création de la base de données annulée")                        

    
    def quitter(self) -> None:
        """Quitte l'application en vérifiant que la base de données ouverte est enregistrée."""

        if self.base is not None:
            if not self.base.est_enregistree:
                demande_enregistrement = QMessageBox.warning(self, "Enregistrer avant de quitter ?", "Vous êtes sur le point de quitter l'application, ce qui va entraîner la perte des modifications non enregistrées. Voulez-vous enregistrer avant de quitter ?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
                
                if demande_enregistrement == QMessageBox.StandardButton.Yes:
                    print("Enregistrement de la base de données")
                    self.enregistrer()
                    self.close()

                elif demande_enregistrement == QMessageBox.StandardButton.No:
                    print("Fermeture de l'application sans enregistrer")
                    self.close()

                elif demande_enregistrement == QMessageBox.StandardButton.Cancel:
                    print("Annulation de la fermeture")


                


        else:
            self.close()





# Créer l'application
app = QApplication([])
fenetre = FenetreAppli()
fenetre.show()
app.exec()