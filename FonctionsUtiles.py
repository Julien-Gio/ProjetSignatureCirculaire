from hashlib import blake2b  # pour la fonction de hashage
from hashlib import sha256  # pour l'oracle aléatoire
import struct

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


def float2bytearray(f):
    b = bytearray(struct.pack(">f", f))
    return b


def bytearray2float(b):
    if len(b) != 4:
        # Un float est sur 4 octets
        raise Exception("b ne correspond pas a un float!")

    f = struct.unpack(">f", b[:])  # Tuple avec 1 element
    return f[0]


def calc_C1(Sigma_seed, c1):
    # C1 = h(Sigma | c1[0] | ... | c1[N-1])
    # Sigma_seed est un float définissant la permutation de Sigma
    # c1 est une liste des tous les c1_i
    concat = float2bytearray(Sigma_seed)  # Type bytearray
    for c in c1:
        concat += c
    C1 = hachage(concat)
    return C1


def calc_C2(Sigma_seed, c2):
    # C2 = h(Sigma(c2[0], ... , c2[N-1]))
    # Sigma est une permutation
    # c2 est une liste des tous les c2_i
    C2 = hachage(Sigma.apply(c2))
    return C2


def calc_C3(Sigma_seed, c3):
    # C3 = h(Sigma(c3[0], ... , c3[N-1]))
    # Sigma est une permutation
    # c3 est une liste des tous les c3_i
    C3 = hachage(Sigma.apply(c3))
    return C3
