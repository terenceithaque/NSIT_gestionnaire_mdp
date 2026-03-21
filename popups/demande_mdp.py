"""Ce scritp définit une classe DemandeMdp représentant une popup demandant mot de passe maître d'une base de données."""
from PyQt6.QtWidgets import QDialog, QLineEdit, QGridLayout, QPushButton, QWidget, QLabel

class DemandeMdp(QDialog):
    """Une instance de popup demandant un mot de passe maître."""
    def __init__(self, titre_fenetre:str="Mot de passe maître"):
        super().__init__()

        self.setWindowTitle(titre_fenetre)

        self.parentLayout = QGridLayout() # Disposition des widgets en grille

        self.labelMdp = QLabel("Saisir le mot de passe maître:")
        self.champMdp = QLineEdit()
        self.champMdp.setPlaceholderText("Mot de passe maître...")
        self.champMdp.setEchoMode(QLineEdit.EchoMode.Password) # Cacher la saisie du mot de passe

        self.bouton_afficher_cacher = QPushButton("Afficher") # Bouton pour afficher ou cacher le mot de passe

        self.bouton_valider = QPushButton("OK") # Bouton pour valider la saisie


        # Ajouter les widgets à la disposition en grille
        self.parentLayout.addWidget(self.labelMdp, 0, 0)
        self.parentLayout.addWidget(self.champMdp, 0, 1)
        self.parentLayout.addWidget(self.bouton_afficher_cacher, 0, 2)
        self.parentLayout.addWidget(self.bouton_valider, 1, 0)

        self.setLayout(self.parentLayout)