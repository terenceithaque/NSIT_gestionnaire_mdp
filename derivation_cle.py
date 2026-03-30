"""derivation_cle.py permet d'utiliser la dérivation de clé afin de permettre le chiffrement d'une base de données à partir d'un mot de passe."""
import os
import base64
from cryptography.fernet import Fernet
from argon2.low_level import hash_secret_raw, Type

def deriver_cle(mdp:str, sel:bytes) -> bytes:
    """Dérive le mot de passe donné en paramètre en une clé sous forme d'octets."""
    
    # Générer la clé à partir du mot de passe et du sel
    cle = hash_secret_raw(
        secret=mdp.encode(),
        salt=sel,
        time_cost=3,
        memory_cost=65536,
        parallelism=1,
        hash_len=32,
        type=Type.ID)
    
    # Formater la clé en base64
    return base64.urlsafe_b64encode(cle)

