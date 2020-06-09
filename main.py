#! python3
# Thomas Casadevall, Ophélie Deschaux, Julien Giovinazzo - June 2020
# Projet Cryptographie : Ring Signatures

from F2n import F2n
from Signataire import Signataire, NonSignataire
import random

def main():
    #################################################
    #
    # 1. Générer la signature de l'anneau
    # 2. Utiliser un oracle aléatoire pour transformer le
    #       schéma d'identification de Stern en signature
    #   A. Commitment
    #   B. Challenge (avec l'oracle)
    #   C. Réponse
    # 3. Verification de la signature
    #
    #################################################
    
    N = 8  # Nombre de personnes dans l'anneau
    t = 3  # Nombre de signataires
    m  = "pomme de terre"  # Message a signer par l'anneau

    # Générer la signature #
    n = 10  # Longueur d'un mot
    k = 4  # k quoi

    # Les membres de l'anneau
    P = []
    for i in range(N):
        if N <= t:
            s = 1  #TODO génerer la clé secrète
            signataire = Signataire(n, s)
        else:
            signataire = NonSignataire(n)
        P.append(signataire)


    nbr_rounds = 10  # Nombre de rondes
    for r in range(nbr_rounds):
        # Commitment step #
                
        # Générer Sigma
        # TODO
        
        # Calcul de C1, C2, et C3 (les 'master commitments')
        # TODO

        # Challenge step #
        # Utiliser une fonction de hachage semblable a un oracle aléatoire
        beta = random_oracle(alpha, M)

        # Response step #
        if beta == 0:
            reveal1 = 0 # y
            reveal2 = 0 # Pi
        elif beta == 1:
            reveal1 = 0 # (y XOR s)
            reveal2 = 0 # Pi
        elif beta == 2:
            reveal1 = 0 # Pi(y)
            reveal2 = 0 # Pi(s)
        else
            raise Exception("L'oracle a donnée une valeur impossible pour beta :", beta)

        # Verify step #
        if verify(beta, reveal1, reveal2) == True:
            print("Signature verifiée")
        else
            print("Signature falsifiée !")
            break


def calc_H(Hn):
    pass


def setup():
    pass


def generer_y():
    pass


def random_oracle(alpha, m):
    # TODO => SHA ou MD5
    return random.choice([0, 1, 2])
        

def verify(beta, param1, param2):
    if beta == 0:
        return True
    elif beta == 1:
        return True
    elif beta == 2:
        return True
    else
        raise Exception("L'oracle a donnée une valeur impossible pour beta :", beta)



if __name__ == "__main__":
    main()
