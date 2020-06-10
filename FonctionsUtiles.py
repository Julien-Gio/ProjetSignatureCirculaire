from hashlib import blake2b  # pour la fonction de hashage
from hashlib import sha256  # pour l'oracle aléatoire


def calc_H(Hn):
    # Hn est une liste des matrices publiques H
    pass


def random_oracle(alpha, m):
    h_out = sha256(alpha + m).digest()
    # Extraire le dernier octet
    octet = int.from_bytes(h_out[-1:], "little")
    return octet % 3


def hachage(n, x):
    # n est la taille de sortie du hashage
    # x est de type bytearray
    # retourne h(x) de type bytearray
    h_out = blake2b(x, digest_size=8).digest()
    return bytearray(h_out)
