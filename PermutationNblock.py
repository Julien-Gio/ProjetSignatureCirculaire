# Classe représentant une premutation de N blocks

from F2n import F2n

import random
import copy

class PermutationNblock:
    def __init__(self, N_, seed_=0):
        if seed_ == 0:
            self.seed = random.random()
        else:
            self.seed = seed_
        self.N = N_

    def apply(self, vect_ref):
        if type(vect_ref) == F2n:
            return self.applyF2n(vect_ref)
        elif type(vect_ref) == list:
            return self.applyList(vect_ref)
        else:
            raise Exception("Type pas permutable !")


    def applyF2n(self, vect_ref):
        # vect_ref est de type F2n
        vect = copy.deepcopy(vect_ref)  # Evite les problèmes liés au fait que les paramettres sont passées par 
        random.seed(self.seed)

        # Appliquer le mélange de Fisher-Yates : https://fr.wikipedia.org/wiki/M%C3%A9lange_de_Fisher-Yates
        for i in range(self.N, 0, -1):
            j = random.randint(0, self.N-1)
            # Permuter vect[i-1] et vect[j]
            temp = vect.bits[i-1]
            vect.bits[i-1] = vect.bits[j]
            vect.bits[j] = temp

        random.seed()  # Remet une graine aléaoire dans le RNG
        return vect


    def applyList(self, vect_ref):
        # vect_ref est de type list
        vect = copy.deepcopy(vect_ref)  # Evite les problèmes liés au fait que les paramettres sont passées par 
        random.seed(self.seed)

        # Appliquer le mélange de Fisher-Yates : https://fr.wikipedia.org/wiki/M%C3%A9lange_de_Fisher-Yates
        for i in range(self.N, 0, -1):
            j = random.randint(0, self.N-1)
            # Permuter vect[i-1] et vect[j]
            temp = vect[i-1]
            vect[i-1] = vect[j]
            vect[j] = temp

        random.seed()  # Remet une graine aléaoire dans le RNG
        return vect


