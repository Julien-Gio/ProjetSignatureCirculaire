# Classe pour facilement manipuler les nombres dans F2-n alias
# un vecteur de n bits

import random
import numpy as np

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


    # Opérateur ==
    def __eq__(self, obj):
        if not isinstance(obj, F2n):
            return False
        return self.bits == obj.bits


    def to_np_array(self):
        # Convert F2n to np.array
        out = np.array([])
        for b in self.bits:
            out = np.concatenate((out, np.array([b])))
            
        return out
    
    def to_bytearray(self):
        # Convert F2n to bytearray
        out = bytearray(self.bits)
        return out
    

    def from_bytearray(self, b):
        # Read bytearray of length n and store it
        for i in range(self.n):
            self.bits[i] = b[i]


# Petit tests
if __name__ == "__main__":
    y = F2n(6)
    y.randomize()
    x = F2n(6)
    x.randomize()
    print(y, "^", x, "=", y^x)
    yba = y.to_bytearray()
    y2 = F2n(6)
    y2.from_bytearray(yba)
    print(yba)
    print(y2)
    print(y.to_np_array())
    
