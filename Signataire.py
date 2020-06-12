# Classes représentant un signataire ou un non-signataire

from F2n import F2n
from PermutationNblock import PermutationNblock
import FonctionsUtiles as FU

import random
import numpy as np

class Signataire:
    def __init__(self, n_, k_, w_, non_signataire=False):
        self.n = n_  # Taille
        self.k = k_
        self.w = w_  # Poids de s (0 pour un non signataire)
        
        self.gen_Hs()  # H et s

        if non_signataire:  # Dans le cas d'un non signataire, s = 0
            self.s = F2n(self.n)
            
        self.gen_ysigma()  # y et sigma (calcul c1, c2 et c3 au passage)
        

    def gen_Hs(self):
        # Algo de KeyGen (calcul de H et s)
        #   1. choose s a random vector of weight w
        #   2. generate k-1 random vectors that make a G of rank k
        #   3. Calculate Gsys
        #   4. Build H

        G_carre_inv = np.zeros(1)
        while not G_carre_inv.any():
            # 1. choose s a random vector of weight w
            self.s = F2n(self.n)
            while self.s.get_poids() != self.w:
                self.s = F2n(self.n)
                self.s.randomize()

            # 2. generate k-1 random vectors that make a G of rank k
            while True:
                rowS = []
                for i in self.s.bits:
                    rowS.append(i)
                G = np.array(rowS)
                for i in range(self.k-1):
                    newrow = F2n(self.n)
                    newrow.randomize()                
                    row = []
                    for i in newrow.bits:
                        row.append(i)
                    G = np.vstack([G, row])
                
                if np.linalg.matrix_rank(G) == self.k:
                    # Le rang de notre G est bon. Sinon on recommence
                    break
            
            # 3. Calculate Gsys
            # Pivot de Gauss sur G
            G_carre = G[:, 0:self.k]  # k par k
            G_sys = []
            try:
                G_carre_inv = np.linalg.inv(G_carre)
            except np.linalg.LinAlgError:
                pass # Recommencer
        
        G_sys = G_carre_inv.dot(G)
        G_sys = np.matrix(G_sys, dtype=int)  # Passer la matrice en int

        # Passer la matrice d'entiers en matrice binaire
        for ligne in range(self.k):
            for col in range(self.n):
                G_sys[ligne, col] = G_sys[ligne, col] % 2

        # 4. Build H
        G_droite = G_sys[:, self.k:]  # Les n-k colonnes de droite
        I = np.identity(self.n - self.k, dtype=int)  # Matrice identité
        self.H = np.concatenate((np.transpose(G_droite), I), axis=1)  # H = [G_droite | I]


        
    def gen_ysigma(self):
        # Generer le y_i aléatoire de ce signataire
        self.y = F2n(self.n)
        self.y.randomize()

        # Generer le sigma (permutation aléatoire de (1, ..., n))
        self.sigma = PermutationNblock(self.n)

        # Calculer c1, c2, et c3
        mul = FU.matrice_mul(self.H, self.y.to_np_array())[0, :]  # type np.array
        mul_ba = mul.tobytes()
        concat = FU.float2bytearray(self.sigma.seed) + mul_ba
        self.c1 = FU.hachage(self.n, concat)  # c1 = h(sigma | Hy')
        self.c2 = FU.hachage(self.n, self.sigma.apply(self.y).to_bytearray())  # c2 = h(sigma(y))
        self.c3 = FU.hachage(self.n, self.sigma.apply(self.y ^ self.s).to_bytearray())  # c3 = h(sigma(y XOR s))

        return self.y, self.sigma


    def get_ysigma(self):
        return self.y, self.sigma

    
    def get_c1c2c3(self):
        return self.c1, self.c2, self.c3
        


# Une personne non-signataire est comme une personne signataire, mais
# avec une clé privée s = 0
class NonSignataire(Signataire):  # NonSignataire hérite de Signataire
    def __init__(self, n_, k_, w_):
        super().__init__(n_, k_, w_, True)  # Constructeur de Signataire (la classe parent)
        # Le reste est identique


if __name__ == "__main__":
    s = Signataire(10, 4, 4)

