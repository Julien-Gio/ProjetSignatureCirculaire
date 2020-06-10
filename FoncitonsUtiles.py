from hashlib import blake2b  # pour la fonction de hashage
from hashlib import sha256  # pour l'oracle aléatoire


def calc_H(Hn):
    # Hn est une liste des matrices publiques H
    pass


def random_oracle(alpha, m):
    # TODO => SHA ou MD5
    return random.choice([0, 1, 2])


def hachage(n, x):
    # n est la taille de sortie du hashage
    # x est de type bytearray
    # retourne h(x) de type bytearray
    h_out = blake2b(x, digest_size=8).digest()
    return bytearray(h_out)
