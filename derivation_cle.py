"""derivation_cle.py permet d'utiliser la dérivation de clé afin de permettre le chiffrement d'une base de données à partir d'un mot de passe."""
import os
import base64
from cryptography.fernet import Fernet
from argon2.low_level import hash_secret_raw, Type

