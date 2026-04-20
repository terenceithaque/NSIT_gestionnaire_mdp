"""creation_groupe.py permet la création d'un nouveau groupe dans une base de données."""
from PyQt6.QtWidgets import QDialog, QLineEdit, QGridLayout, QPushButton, QWidget, QLabel, QMessageBox


class DemandeCreerGroupe(QDialog):
    """Popup permettant à l'utilisateur de saisir le nom d'un nouveau groupe et de le créer."""
    def __init__(self) -> None:
        self.setWindowTitle("Création d'un groupe")

        self.parentLayout = QGridLayout()

        self.champ_nom_groupe = QLineEdit()
        self.champ_nom_groupe.setPlaceholderText("Nom du groupe...")

        self.nom_groupe_valide = False

        self.bouton_valider = QPushButton("OK")
        self.bouton_annuler = QPushButton("Annuler")


    def fermer(self, validation=True) -> None:
        """Ferme la popup.
        - validation: booléen indiquant si le nom de groupe saisit doit être validé (non vide)."""

        if validation:
            if len(self.champ_nom_groupe.text()) > 0:
                self.nom_groupe_valide = True
                self.accept()

            else:
                self.nom_groupe_valide = False
                QMessageBox.warning(self, "Saisissez un nom de groupe", "Veuillez saisir un nom de groupe non vide.", QMessageBox.StandardButton.Ok)
                self.reject()

        else:
            self.nom_groupe_valide = False
            self.accept()        



    