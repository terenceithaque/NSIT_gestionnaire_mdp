"""Ce script permet de calculer la force d'un mot de passe en bits"""
import math


def taille_alphabet(mdp:str) -> int:
    """Renvoie la taille de l'alphabet utilisé dans le mot de passe donné"""
    taille_alphabet = 0 # Taille de l'alphabet présent dans le mot de passe
    
    # Série de booléens pour savoir quels types de caractères sont présents dans le mot de passe
    min_presentes = False
    maj_presentes = False
    nombres_presents = False
    speciaux_presents = False
    
    # Parcourir les caractères du mot de passe
    for caractere in mdp:
        # Si des lettres minuscules n'ont pas déjà été détectées dans le mot de passe
        if not min_presentes:
            if caractere.isalpha() and caractere.lower()==caractere:
                taille_alphabet += 26
                min_presentes = True
                continue
        
        # Si des lettres majuscules n'ont pas déjà été détectées dans le mot de passe
        if not maj_presentes:
            if caractere.isalpha() and caractere.upper()==caractere:
                taille_alphabet += 26
                maj_presentes = True
                continue
        
        # Si des nombres n'ont pas déjà été détectés dans le mot de passe
        if not nombres_presents:  
            if caractere.isdigit():
                taille_alphabet += 10
                nombres_presents = True
                continue
            
        # Si des caractères spéciaux n'ont pas été déjà détectés dans le mot de passe
        if not speciaux_presents:
            if not caractere.isalnum():
                taille_alphabet += 32
                speciaux_presents = True
                continue
    
    return taille_alphabet


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
    
    