"nouveau_mdp.py contient une classe DemandeNouveauMdp représentant une popup d'ajout d'un mot de passe"
from PyQt6.QtWidgets import QDialog, QLineEdit, QGridLayout, QPushButton, QWidget, QLabel, QMessageBox
import mdp.force_mdp
import mdp.generer_mdp
import string


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

        self.bouton_generer_mdp = QPushButton("Générer un mot de passe fort")
        self.bouton_generer_mdp.clicked.connect(self.generer_mdp_fort)


        self.labelForce = QLabel(f"Force du mot de passe: 0 bits (<b>faible</b>)")

        self.boutonValider = QPushButton("OK")
        self.boutonAnnuler = QPushButton("Annuler")

        self.boutonValider.clicked.connect(lambda:self.fermer(validation=True))
        self.boutonAnnuler.clicked.connect(lambda:self.fermer(validation=False))

        self.champ_mdp.textChanged.connect(self.actualiser_force_mdp)

        self.forcer_fermeture = False
        self.mdp_verifie = False
        self.nom_util_verifie = False


        # Disposition des widgets dans la popup
        self.parentLayout.addWidget(self.labelTitre, 0, 0)
        self.parentLayout.addWidget(self.champ_titre, 0, 1)

        self.parentLayout.addWidget(self.labelNomUtil, 1,0)
        self.parentLayout.addWidget(self.champ_nom_util, 1,1)

        self.parentLayout.addWidget(self.labelMdp, 2,0)
        self.parentLayout.addWidget(self.champ_mdp, 2,1)
        self.parentLayout.addWidget(self.bouton_afficher_cacher, 2,2)

        self.parentLayout.addWidget(self.bouton_generer_mdp, 3,0)

        self.parentLayout.addWidget(self.labelForce, 4, 0)

        self.parentLayout.addWidget(self.boutonValider, 5,0)
        self.parentLayout.addWidget(self.boutonAnnuler, 5,1)

        self.setLayout(self.parentLayout)



    def valider(self) -> bool:
        """Vérifie la validité des champs de saisie en renvoie True si tout est correct, False sinon.
        Un avertissement est affiché dans le cas où les champs sont invalides."""

        if not self.champ_nom_util.text() or not self.champ_mdp.text():
            QMessageBox.warning(self, "Nom d'utilisateur et/ou mot de passe invalide", "Le nom d'utilisateur et/ou le mot de passe sont invalides.", QMessageBox.StandardButton.Ok)
            return False
        
        return True
    

    def obtenir_entrees(self) -> dict:
        """Renvoie le contenu de l'ensemble des entrées de la popup sous forme de dictionnaire."""

        resultat = {
            "titreEntree":self.champ_titre.text(),
            "nomUtil":self.champ_nom_util.text(),
            "mdp":self.champ_mdp.text()
        }

        return resultat
    

    def generer_mdp_fort(self) -> None:
        """Génère un mot de passe fort et met à jour le champ de saisie du mot de passe."""

        mot_de_passe = mdp.generer_mdp.generer_mdp(taille_min=12, inclus=[string.ascii_lowercase, string.ascii_uppercase, string.digits, string.punctuation])
        self.champ_mdp.setText(mot_de_passe)
        self.actualiser_force_mdp()

    def actualiser_force_mdp(self) -> None:
        """Actualise la force de mot de passe affichée pour refléter le mot de passe actuellement saisi."""

        mot_de_passe = self.champ_mdp.text()
        
        if len(mot_de_passe) > 0:
            force_mdp = mdp.force_mdp.force(self.champ_mdp.text())

            if force_mdp < 40:
                self.labelForce.setText(f"Force du mot de passe : {mdp.force_mdp.force(self.champ_mdp.text())} bits (<b>faible</b>)")

            if 40 <= force_mdp <= 60:
                    self.labelForce.setText(f"Force du mot de passe : {mdp.force_mdp.force(self.champ_mdp.text())} bits (<b>moyenne</b>)")

            if force_mdp > 60:
                self.labelForce.setText(f"Force du mot de passe : {mdp.force_mdp.force(self.champ_mdp.text())} bits (<b>élevée</b>)")        



        else:
            self.labelForce.setText(f"Force du mot de passe: 0 bits (<b>faible</b>)")
    
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

      

    def closeEvent(self, event):
        """Méthode appelée lors de la fermeture de la popup. Elle permet de valider le mot de passe et le nom d'utilisateur avant fermeture, ou au contraire de forcer la fermeture sans validation."""

        if self.forcer_fermeture:
            event.accept()
            return
        
        if self.valider():
            self.mdp_verifie, self.nom_util_verifie = True, True
            event.accept()

        else:
            self.mdp_verifie, self.nom_util_verifie = False, False
            event.ignore()  

    def fermer(self, validation=True) -> None:
        """Ferme la popup.
        - validation: booléen ayant True comme valeur par défaut. Indique s'il faut valider le mot de passe et le nom d'utilisateur avant de fermer la popup."""


        if validation:
            if self.valider():
                self.mdp_verifie, self.nom_util_verifie = True, True
                self.forcer_fermeture = False
                self.accept()

        else:
            self.mdp_verifie, self.nom_util_verifie = False, False
            self.forcer_fermeture = True
            self.reject()                         