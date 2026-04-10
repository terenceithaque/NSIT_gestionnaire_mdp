"nouveau_mdp.py contient une classe DemandeNouveauMdp représentant une popup d'ajout d'un mot de passe"
from PyQt6.QtWidgets import QDialog, QLineEdit, QGridLayout, QPushButton, QWidget, QLabel, QMessageBox
import mdp.force_mdp


class DemandeNouveauMdp(QDialog):
    """Popup permettant à l'utilisateur de créer une nouvelle entrée dans la base de données de mots de passe.
    Les champs à spécifier sont: titre, nom de l'utilisateur ou adresse email, mot de passe. """
    
    def __init__(self) -> None:

        super().__init__()
        
        self.parentLayout = QGridLayout() # Disposer les widgets en grille

        self.setWindowTitle("Nouvelle entrée")

        self.labelTitre = QLabel("Titre de l'entrée:")
        self.champ_titre = QLineEdit()
        self.champ_titre.setPlaceholderText("Titre (page web / autre)")


        self.labelNomUtil = QLabel("Nom d'utilisateur ou email:")
        self.champ_nom_util = QLineEdit()
        self.champ_nom_util.setPlaceholderText("prenom.nom@example.com")

        self.labelMdp = QLabel("Mot de passe:")
        self.champ_mdp = QLineEdit()
        self.champ_mdp.setPlaceholderText("Mot de passe")
        self.champ_mdp.setEchoMode(QLineEdit.EchoMode.Password)
        self.bouton_afficher_cacher = QPushButton("Afficher")
        self.bouton_afficher_cacher.clicked.connect(self.modifier_affichage_mdp)

        self.labelForce = QLabel(f"Force du mot de passe: 0 bits")

        self.champ_mdp.textChanged.connect(self.actualiser_force_mdp)


        # Disposition des widgets dans la popup
        self.parentLayout.addWidget(self.labelTitre, 0, 0)
        self.parentLayout.addWidget(self.champ_titre, 0, 1)

        self.parentLayout.addWidget(self.labelNomUtil, 1,0)
        self.parentLayout.addWidget(self.champ_nom_util, 1,1)

        self.parentLayout.addWidget(self.labelMdp, 2,0)
        self.parentLayout.addWidget(self.champ_mdp, 2,1)
        self.parentLayout.addWidget(self.bouton_afficher_cacher, 2,2)

        self.parentLayout.addWidget(self.labelForce, 3,0)

        self.setLayout(self.parentLayout)




    def actualiser_force_mdp(self) -> None:
        """Actualise la force de mot de passe affichée pour refléter le mot de passe actuellement saisi."""

        mot_de_passe = self.champ_mdp.text()
        
        if len(mot_de_passe) > 0:
            self.labelForce.setText(f"Force du mot de passe : {mdp.force_mdp.force(self.champ_mdp.text())} bits")

        else:
            self.labelForce.setText(f"Force du mot de passe: 0 bits")
    
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