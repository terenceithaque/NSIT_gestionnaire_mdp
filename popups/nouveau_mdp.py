"nouveau_mdp.py contient une classe DemandeNouveauMdp représentant une popup d'ajout d'un mot de passe"
from PyQt6.QtWidgets import QDialog, QLineEdit, QGridLayout, QPushButton, QWidget, QLabel, QMessageBox
import mdp.force_mdp


class DemandeNouveauMdp(QDialog):
    """Popup permettant à l'utilisateur de créer une nouvelle entrée dans la base de données de mots de passe.
    Les champs à spécifier sont: titre, nom de l'utilisateur ou adresse email, mot de passe. """
    
    def __init__(self) -> None:
        
        self.parentLayout = QGridLayout() # Disposer les widgets en grille

        self.setWindowTitle("Nouvelle entrée")

        self.labelTitre = "Titre de l'entrée:"
        self.champ_titre = QLineEdit()
        self.champ_titre.setPlaceholderText("Titre (page web / autre)")


        self.labelNomUtil = "Nom d'utilisateur ou email:"
        self.champ_nom_util = QLineEdit()
        self.champ_nom_util.setPlaceholderText("prenom.nom@example.com")

        self.labelMdp = "Mot de passe:"
        self.champ_mdp = QLineEdit()
        self.champ_mdp.setPlaceholderText("Mot de passe")
        self.champ_mdp.setEchoMode(QLineEdit.EchoMode.Password)
        self.bouton_afficher_cacher = QPushButton("Afficher")
        self.bouton_afficher_cacher.clicked.connect(self.modifier_affichage_mdp)


    def modifier_affichage_mdp(self) -> None:
        """Modifie l'affichage du mot de passe dans le champ de saisie."""

        # Si le mot de passe est actuellement caché
        if self.champ_mdp.echoMode() == QLineEdit.EchoMode.Password:
            # L'afficher
            self.champ_mdp.setEchoMode(QLineEdit.EchoMode.Normal)
            self.bouton_afficher_cacher.setText("Cacher")

        else:
            self.champ_mdp.setEchoMode(QLineEdit.EchoMode.Password)
            self.bouton_afficher_cacher.setText("Afficher")        