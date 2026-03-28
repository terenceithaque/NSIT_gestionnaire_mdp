"""Ce script contient une fonction hash_mdp qui permet de calculer le hash d'un mot de passe."""
from argon2 import PasswordHasher


def hash_mdp(mdp:str) -> str:
    """Renvoie le hash du mot de passe donné en utilisant Argon2."""

    ph = PasswordHasher()

    # Hasher le mot de passe en Argon2
    mdp_hash = ph.hash(mdp)

    return mdp_hash
