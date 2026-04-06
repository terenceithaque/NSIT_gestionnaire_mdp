"nouveau_mdp.py contient une classe DemandeNouveauMdp représentant une popup d'ajout d'un mot de passe"
from PyQt6.QtWidgets import QDialog, QLineEdit, QGridLayout, QPushButton, QWidget, QLabel, QMessageBox
import mdp.force_mdp


class DemandeNouveauMdp(QDialog):
    """Popup permettant à l'utilisateur de créer une nouvelle entrée dans la base de données de mots de passe.
    Les champs à spécifier sont: titre, nom de l'utilisateur, adresse email. """
    
    def __init__(self) -> None:
        pass