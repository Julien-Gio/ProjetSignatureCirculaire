# Classes représentant un signataire ou un non-signataire

from F2n import F2n
from PermutationNblock import PermutationNblock
import FonctionsUtiles as FU

import random

class Signataire:
    def __init__(self, n_, w_):
        self.n = n_  # Taille
        self.w = w_  # Poids de s (0 pour un non signataire)
        # Générer H et s
        # TODO
        self.s = F2n(self.n)
        

    def gen_ysigma(self):
        # Generer le y_i aléatoire de ce signataire
        self.y = F2n(self.n)
        self.y.randomize()

        # Generer le sigma (permutation aléatoire de (1, ..., n))
        self.sigma = PermutationNblock(self.n)

        # Calculer c1, c2, et c3
        # TODO
        concat = self.sigma.seed
        self.c1 = FU.hachage(self.n, concat)  # c1 = h(sigma | Hy')
        
        self.c2 = FU.hachage(self.n, self.sigma.apply(self.y))  # c2 = h(sigma(y))

        self.c3 = FU.hachage(self.n, self.sigma.apply(self.y ^ self.s))  # c3 = h(sigma(y XOR s))
        
        return self.y, self.sigma


    def get_c1c2c3(self):
        return self.c1, self.c2, self.c3
        


# Une personne non-signataire est comme une personne signataire, mais
# avec une clé privée s = 0
class NonSignataire(Signataire):  # NonSignataire hérite de Signataire
    def __init__(self, n_):
        super().__init__(n_, 0)  # Constructeur de Signataire, la classe parent
        # Le reste est identique
