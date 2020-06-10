# Classes représentant un signataire ou un non-signataire

from F2n import F2n
from PermutationNblock import PermutationNblock
import FonctionsUtiles as FU

import random

class Signataire:
    def __init__(self, n_, s_):
        self.n = n_
        self.s = s_

    def gen_ysigma(self):
        # Generer le y_i aléatoire de ce signataire
        self.y = F2n(self.n)
        self.y.randomize()

        # Generer le sigma (permutation aléatoire de (1, ..., n))
        self.sigma = PermutationNblock(self.n)        
        
        return self.y, self.sigma

    def get_c1c2c3(self):
        # Calcule et retourne c1, c2, et c3
        # TODO
        concat = self.sigma
        self.c1 = FU.hachage(self.n, self.sigma)  # c1 = h(sigma | Hy')
        
        self.c2 = FU.hachage(self.n, self.sigma.apply(self.y))  # c2 = h(sigma(y))

        self.c3 = FU.hachage()  # c3 = h(sigma(y XOR s))
        return self.c1, self.c2, self.c3
        


# Une personne non-signataire est comme une personne signataire, mais
# avec une clé privée s = 0
class NonSignataire(Signataire):  # NonSignataire hérite de Signataire
    def __init__(self, n_):
        super().__init__(n_, 0)  # Constructeur de Signataire, la classe parent
        # Le reste est identique
