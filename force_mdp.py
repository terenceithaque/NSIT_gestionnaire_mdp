"""Ce script permet de calculer la force d'un mot de passe en bits"""
import math


def taille_alphabet(mdp:str) -> int:
    """Renvoie la taille de l'alphabet utilisé dans le mot de passe donné"""
    taille_alphabet = 0 # Taille de l'alphabet présent dans le mot de passe
    
    # Série de booléens pour savoir quels types de caractères sont présents dans le mot de passe
    lettres_presentes = False
    nombres_presents = False
    speciaux_presents = False
    
    # Parcourir les caractères du mot de passe
    for caractere in mdp:
        # Si des lettres n'ont pas déjà été détectées dans le mot de passe
        if not lettres_presentes:
            if caractere.is_alpha():
                taille_alphabet += 26
                lettres_presentes = True
                continue
        
        # Si des nombres n'ont pas déjà été détectés dans le mot de passe
        if not nombres_presents:  
            if caractere.isdigit():
                taille_alphabet += 10
                nombres_presents = True
                continue
            
        # Si des caractères spéciaux n'ont pas été déjà détectés dans le mot de passe
        if not speciaux_presents:
            if caractere.isalnum():
                taille_alphabet += 32
                speciaux_presents = True
                continue
    
     return taille_alphabet


def force(mdp:str) -> float:
    """Renvoie la force du mot de passe donné en bits, en calculant l'entropie"""
    pass
    