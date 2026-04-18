"generer_mdp.py permet de générer des mots de passe forts de façon automatisée."
import secrets
import random
import string
import force_mdp


def generer_mdp(taille_min:int, inclus:list) -> str:
    """Génère un mot de passe fort en utilisant la base de caractères fournie.
    - taille_min: la taille minimale du mot de passe. Tant que celle-cit n'est pas respectée, le mot de passe est re-généré.
    - inclus: liste contenant les caractères pouvant être utilisés pour la génération du mot de passe."""

    assert taille_min > 0, "La taille minimale du mot de passe à générer doit être positive."

    mdp = []

    for groupe in inclus:
        mdp.append(secrets.choice(groupe))


    tous_les_caracteres = "".join(inclus)

    while len(mdp) < taille_min:
        mdp.append(secrets.choice(tous_les_caracteres))

    # Mélanger pour éviter un ordre prévisible
    random.shuffle(mdp)

    return "".join(mdp)



if __name__ == "__main__":

    while True:
        taille_min = int(input("Taille minimale du mot de passe à générer:"))
        inclus = [string.ascii_lowercase, string.ascii_uppercase, string.digits, string.punctuation]
        mot_de_passe = generer_mdp(taille_min, inclus)
        print()
        
        print(f"{mot_de_passe} (force:{force_mdp.force(mot_de_passe)} bits)")