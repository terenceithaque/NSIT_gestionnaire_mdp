"edition_mdp.py contient une classe EditeMdp, représentant une popup permettant d'éditer une entrée dans une base de données."
import popups.nouveau_mdp

class EditeMdp(popups.nouveau_mdp.DemandeNouveauMdp):
    """Une popup permettant d'éditer une entrée de mot de passe dans la base de données.
    Cette classe hérite de la classe DemandeNouveauMdp définie dans popups/nouveau_mdp.py"""

    def __init__(self, donnees_entree:dict) -> None:
        super().__init__() # Hériter de l'ensemble des attributs de la classe DemandeNouveauMdp

        self.setWindowTitle("Éditer l'entrée")

        self.donnees_entree = donnees_entree # Dictionnaire contenant l'ensemble de données de l'entrée (nom d'utilisateur, mot de passe, etc).

        # Récupérer les textes saisis dans les différents champs de l'entrée
        self.titre_entree = self.donnees_entree["titreEntree"]
        self.nom_util = self.donnees_entree["nomUtil"]
        self.mdp = self.donnees_entree["mdp"]

        # Placer les textes dans les différents champs
        self.champ_titre.setText(self.titre_entree)
        self.champ_nom_util.setText(self.nom_util)
        self.champ_mdp.setText(self.mdp)