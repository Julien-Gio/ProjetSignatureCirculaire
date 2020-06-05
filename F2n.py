# Classe pour facilement manipuler les nombres dans F2-n alias
# un vecteur de n bits

import random

class F2n:
    def __init__(self, n_):
        self.n = n_  # Nombre de bits
        self.bits = []  # Les bits
    
        # Initialiser tous les bits à 0
        for i in range(self.n):
            self.bits.append(0)


    # Met des bits aléatoires
    def randomize(self):
        for i in range(self.n):
            self.bits[i] = random.randint(0,1)
    
    
    # Retourne le poids de notre objet
    def get_poids(self):
        return sum(self.bits)


    # Oppéraiton : self ^ other
    def __xor__(self, other):
        # Vérifier que nos deux objets ont la même taille
        if self.n != other.n:
            raise Exception("Erreur, dimentions incompatibles")
        out = F2n(self.n)
        for i in range(self.n):
            out.bits[i] = self.bits[i] ^ other.bits[i]
        return out


    # Methode d'affichage => pour print(F2n)
    def __str__(self):
        out = ""
        for i in range(self.n):
            if self.bits[i] == 0:
                out += "0"
            else:
                out += "1"
        return out


# Petit tests
if __name__ == "__main__":
    y = F2n(6)
    y.randomize()
    x = F2n(6)
    x.randomize()
    print(y, "^", x, "=", y^x)
