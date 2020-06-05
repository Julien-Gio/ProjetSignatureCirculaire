# Classes représentant un signataire ou un non-signataire

from F2n import F2n

class Signataire:
    def __init__(self, n_, s_):
        self.n = n_
        self.s = s_

        # Generer le y_i aléatoire de ce signataire
        self.y = F2n(self.n)
        self.y.randomize()

        # Generer le sigma (permutation aléatoire de (1, ..., n))
        self.sigma = list(range(1, n + 1))
        random.shuffle(self.sigma)  # Permutations

        # Calculer c1, c2, et c3
        


# Une personne non-signataire est comme une personne signataire, mais
# avec une clé privée s = 0
class NonSignataire(Signataire):  # NonSignataire hérite de Signataire
    def __init__(self, n_):
        super().__init__(n_, 0)  # Constructeur de Signataire, la classe parent
        # Le reste est identique
