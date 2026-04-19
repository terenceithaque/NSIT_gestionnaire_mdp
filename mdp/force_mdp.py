"""Ce script permet de calculer la force d'un mot de passe en bits"""
import math
import string

def taille_alphabet(mdp:str) -> int:
    """Renvoie la taille de l'alphabet utilisé dans le mot de passe donné"""
    
    
    if not mdp:
        return 0
    
    min_presentes = any(c in string.ascii_lowercase for c in mdp)
    maj_presentes = any(c in string.ascii_uppercase for c in mdp)
    nombres_presents = any(c in string.digits for c in mdp)
    speciaux_presents = any(c in string.punctuation for c in mdp)

    taille = 0

    if min_presentes:
        taille += 26

    if maj_presentes:
        taille += 26

    if nombres_presents:
        taille += 10

    if speciaux_presents:
        taille += len(string.punctuation)

    return taille        

    
   


def force(mdp:str) -> int:
    """Renvoie la force du mot de passe donné en bits, en calculant l'entropie"""
    
    # Calculer la taille de l'alphabet du mot de passe
    S = taille_alphabet(mdp)
    print(S)
    
    # Calcul de l'entropie du mot de passe
    L = len(mdp)
    entropie = L*math.log2(S)
    
    return round(entropie)
    


if __name__=="__main__":
    mdp = input("Saisissez un mot de passe:")
    print("Force du mot de passe:", force(mdp), "bits")
    
    