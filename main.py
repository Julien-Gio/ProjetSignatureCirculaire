#! python3
# Thomas Casadevall, Ophélie Deschaux, Julien Giovinazzo - June 2020
# Projet Cryptographie : Ring Signatures

from F2n import F2n
from Signataire import Signataire, NonSignataire
import FonctionsUtiles as FU

import random


def main():
    ###################################################
    #
    # 1. Générer la signature de l'anneau
    # 2. Utiliser un oracle aléatoire pour transformer le
    #       schéma d'identification de Stern en signature
    #   A. Commitment
    #   B. Challenge (avec l'oracle)
    #   C. Réponse
    # 3. Verification de la signature
    #
    ###################################################
    
    N = 8  # Nombre de personnes dans l'anneau
    t = 3  # Nombre de signataires
    m  = "pomme de terre"  # Message à signer par l'anneau

    # Générer la signature #
    n = 10  # Longueur d'un mot
    k = 4  # k quoi

    # Creer les membres de l'anneau
    membres_anneau = []
    for i in range(N):
        if N <= t:
            s = 1  #TODO génerer la clé secrète
            signataire = Signataire(n, s)
        else:
            signataire = NonSignataire(n)
        membres_anneau.append(signataire)


    nbr_rounds = 10  # Nombre de rondes
    for r in range(nbr_rounds):
        # Commitment step #
        y = []  # Dans F2n
        sigma = []  # permutation de [1, ..., n]
        for i in range(len(membres_anneau)):
            y[i], sigma[i] = membres_annean[i].gen_ysigma()
            
        # Calcul des c1, c2, et c3
        c1 = []
        c2 = []
        c3 = []
        for i in range(len(membres_anneau)):
            c1[i], c2[i], c3[i] = membres_annean[i].get_c1c2c3()
        
        # Générer Sigma
        # TODO
        
        # Calcul de C1, C2, et C3 (les 'master commitments')
        # TODO

        # Challenge step #
        # Utiliser une fonction de hachage semblable a un oracle aléatoire
        beta = FU.random_oracle(alpha, M)

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
