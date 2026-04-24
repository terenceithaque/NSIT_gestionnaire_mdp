"edition_mdp.py contient une classe EditeMdp, représentant une popup permettant d'éditer une entrée dans une base de données."
import popups.nouveau_mdp

class EditeMdp(popups.nouveau_mdp.DemandeNouveauMdp):
    """Une popup permettant d'éditer une entrée de mot de passe dans la base de données.
    Cette classe hérite de la classe DemandeNouveauMdp définie dans popups/nouveau_mdp.py"""

    def __init__(self):
        super().__init__() # Hériter de l'ensemble des attributs de la classe DemandeNouveauMdp