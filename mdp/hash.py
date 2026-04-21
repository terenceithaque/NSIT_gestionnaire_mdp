"""Ce script contient plusieurs fonctions liées aux hashs"""
from argon2 import PasswordHasher
import json

def obtenir_hashs_maitres() -> dict:
    """Renvoie le dictionnaire des hashs de mots de passe maîtres stockés dans un fichiers hashes.json"""

    contenu = {
        "hashes": []
    }
    
    try:
        with open("hashes.json", "r") as f:
            contenu = json.load(f)

            # Vérifier que la clé hashes est bien présente dans le fichier
            assert "hashes" in contenu
            assert type(contenu["hashes"]).__name__ == "list"
            return contenu
    
    except Exception as e:
        print(e)
        return contenu


def enregistrer_hashs_maitres(contenu:dict) -> None:
    """Met à jour le fichier hashes.json en écrivant le contenu fourni."""

    with open("hashes.json", "w") as f:
        json.dump(contenu, f, indent=4)



def verifier_mdp(mdp:str, hashes:list) -> bool:
    """Compare le hash du mot de passe donné avec la liste de hashs donnée et renvoie True s'il y a une correspondance, False sinon."""
    
    print("Mot de passe saisi:", mdp)
    h = hash_mdp(mdp)
    print("Hash du mot de passe:", h)
    print("Hashs disponibles:", hashes)
    
    ph = PasswordHasher()
    for h in hashes:
        try:
            if ph.verify(h, mdp):
                print("Mot de passe correct !")
                return True
        except Exception as e:
            print(e)
            continue
    
    print("Mot de passe incorrect !")
    return False            


def hash_mdp(mdp:str) -> str:
    """Renvoie le hash du mot de passe donné en utilisant Argon2."""

    ph = PasswordHasher()

    # Hasher le mot de passe en Argon2
    mdp_hash = ph.hash(mdp)

    return mdp_hash
