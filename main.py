# Programme principal de l'application
from PyQt6.QtWidgets import QApplication, QMainWindow


class FenetreAppli(QMainWindow):
    """Une instance de fenêtre de l'application"""
    def __init__(self):
        # Hériter des attributs du parent QMainWindow
        super().__init__()
        
        # Dimensions minimales de la fenêtre
        self.setMinimumSize(800,600)
        
        # Titre de la fenêtre
        self.setWindowTitle("Gestionnaire de mots de passe")



# Créer l'application
app = QApplication([])
fenetre = FenetreAppli()
fenetre.show()
app.exec()