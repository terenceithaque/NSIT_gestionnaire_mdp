"""Ce scritp définit une classe DemandeMdp représentant une popup demandant mot de passe maître d'une base de données."""
from PyQt6.QtWidgets import QDialog, QLineEdit, QGridLayout, QPushButton, QWidget, QLabel, QMessageBox

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
        self.bouton_afficher_cacher.clicked.connect(self.modifier_affichage_mdp)
        
        self.bouton_valider = QPushButton("OK") # Bouton pour valider la saisie
        self.bouton_valider.clicked.connect(self.fermer)


        # Ajouter les widgets à la disposition en grille
        self.parentLayout.addWidget(self.labelMdp, 0, 0)
        self.parentLayout.addWidget(self.champMdp, 0, 1)
        self.parentLayout.addWidget(self.bouton_afficher_cacher, 0, 2)
        self.parentLayout.addWidget(self.bouton_valider, 1, 0)

        self.setLayout(self.parentLayout)


    def modifier_affichage_mdp(self) -> None:
        """Modifie l'affichage du mot de passe dans le champ de saisie."""

        # Si le mot de passe est caché
        if self.champMdp.echoMode() == QLineEdit.EchoMode.Password:
            self.champMdp.setEchoMode(QLineEdit.EchoMode.Normal) # Afficher le mot de passe
            self.bouton_afficher_cacher.setText("Cacher")

        else:
            self.champMdp.setEchoMode(QLineEdit.EchoMode.Password)
            self.bouton_afficher_cacher.setText("Afficher")


    def valider_mdp(self) -> bool:
        """Valide le mot de passe maître entré en vérifiant qu'il ne correspond pas à une chaîne vide. Sinon, une erreur est affichée.
        Renvoie True si le mot de passe est validé, False sinon."""

        # Afficher une erreur si le mot de passe renseigné est vide
        if self.champMdp.text() == "":
            QMessageBox.warning(self, "Renseignez un mot de passe", "Veuillez renseigner un mot de passe maître non vide.", QMessageBox.StandardButton.Ok)
            return False
        
        return True

    def fermer(self):
        """Ferme la popup en vérifiant que le mot de passe maître renseigné est valide."""

        if self.valider_mdp():
            # Fermer la popup seulement si le mot de passe maître renseigné est valide
            self.close()