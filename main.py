# Programme principal de l'application
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt6.QtWidgets import QWidget, QMenuBar
from PyQt6.QtGui import QAction
import popups.demande_mdp_maitre

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
        self.menu_fichier.addAction(ouvrir_base)
        
        quitter_app = QAction("Quitter", self)
        quitter_app.setShortcut("Ctrl+Q")
        quitter_app.triggered.connect(self.close)
        self.menu_fichier.addAction(quitter_app)
        
        
        # Widget central de la fenêtre
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.parentLayout)
        self.setCentralWidget(self.centralWidget)


    def creer_base(self) -> None:
        """Crée une nouvelle base de données de mots de passe."""

        popup_mdp_maitre = popups.demande_mdp_maitre.DemandeMdp()

        popup_mdp_maitre.exec()
        



# Créer l'application
app = QApplication([])
fenetre = FenetreAppli()
fenetre.show()
app.exec()