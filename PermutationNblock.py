# Classe représentant une premutation de N blocks

import random
import copy

class PermutationNblock:
    def __init__(self, N_):
        self.seed = random.random()
        self.N = N_

    def apply(self, vect_ref):
        vect = copy.deepcopy(vect_ref)  # Evite les problèmes liés au fait que les listes sont passée par références
        random.seed(self.seed)

        # Appliquer le mélange de Fisher-Yates : https://fr.wikipedia.org/wiki/M%C3%A9lange_de_Fisher-Yates
        for i in range(self.N - 1, 1, -1):
            j = random.randint(0, N-1)
            # Permuter vect[i] et vect[j]
            temp = vect[i]
            vect[i] = vect[j]
            vect[j] = temp

        random.seed()  # Remet une graine aléaoire dans le RNG
        return vect
