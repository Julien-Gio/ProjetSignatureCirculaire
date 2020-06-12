from PermutationNblock import PermutationNblock

from hashlib import blake2b  # pour la fonction de hashage
from hashlib import sha256  # pour l'oracle aléatoire
import struct
import numpy as np

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
    h_out = blake2b(x, digest_size = n//8).digest()
    return bytearray(h_out)


def matrice_mul(M1, M2):
    # M1 et M2 sont des np.array
    mul = np.matmul(M1, M2)  # type np.matrix
    mul = np.asarray(mul)  # type np.array

    for ix, iy in np.ndindex(mul.shape):
        mul[ix, iy] = mul[ix, iy] % 2
    return mul


def float2bytearray(f):
    b = bytearray(struct.pack(">d", f))
    return b


def bytearray2float(b):
    if len(b) != 8:
        # Un float est sur 8 octets
        raise Exception("b ne correspond pas a un float!", len(b))

    f = struct.unpack(">d", b[:])  # Tuple avec 1 element
    return f[0]


def calc_C1(n, Sigma_seed, c1):
    # C1 = h(Sigma | c1[0] | ... | c1[N-1])
    # Sigma_seed est un float définissant la permutation de Sigma
    # c1 est une liste des tous les c1_i
    concat = float2bytearray(Sigma_seed)  # Type bytearray
    for c in c1:
        concat += c
    C1 = hachage(n, concat)
    return C1


def calc_C2(n, Sigma, c2):
    # C2 = h(Sigma(c2[0], ... , c2[N-1]))
    # Sigma est une permutation
    # c2 est une liste des tous les c2_i
    permu = Sigma.apply(c2)
    concat = bytearray()
    for c2 in permu:
        concat += c2
        
    C2 = hachage(n, concat)
    return C2


def calc_C3(n, Sigma, c3):
    # C3 = h(Sigma(c3[0], ... , c3[N-1]))
    # Sigma est une permutation
    # c3 est une liste des tous les c3_i
    permu = Sigma.apply(c3)
    concat = bytearray()
    for c3 in permu:
        concat += c3
        
    C3 = hachage(n, concat)
    return C3


def decompser_Pi(graine_Pi, n, N):
    # Retourne Sigma et les sigma a partir de Pi
    Sigma = PermutationNblock(N, bytearray2float(graine_Pi[0:8]))
    
    sigma = []
    for i in range(N):
        sigma.append(PermutationNblock(n, bytearray2float(graine_Pi[(i+1)*8 : (i+2)*8])))

    return Sigma, sigma
