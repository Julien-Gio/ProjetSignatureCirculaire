#! python3

# Thomas Casadevall, Ophélie Deschaux, Julien Giovinazzo - June 2020
# Projet Cryptographie : Threshold Ring Signatures
# Proof of concept


from F2n import F2n
from Signataire import Signataire, NonSignataire
from PermutationNblock import PermutationNblock
import FonctionsUtiles as FU

import random


def main():
    #######################################################
    #
    # 1. Générer la signature de l'anneau
    # 2. Utiliser un oracle aléatoire pour transformer le
    #       schéma d'identification de Stern en signature
    #   A. Commitment [alpha]
    #   B. Challenge (avec l'oracle) [beta]
    #   C. Réponse [gamma and gamma']
    # 3. Verification de la signature
    #
    #######################################################
    
    N = 8  # Nombre de personnes dans l'anneau
    t = 3  # Nombre de signataires
    M  = b'pomme de terre'  # Message à signer par l'anneau

    # Générer la signature #
    n = 32  # Longueur d'un mot. Doit etre un multiple de 8
    k = 10  # k quoi
    w = 15  # Poid du secret s des signataires

    # Creer les membres de l'anneau
    membres_anneau = []
    for i in range(N):
        if N <= t:
            s = 1  #TODO génerer la clé secrète
            signataire = Signataire(n, k, w)
        else:
            signataire = NonSignataire(n, k)
        membres_anneau.append(signataire)


    Sig = []  # Signature. Ex pour 2 rounds : [alpha1, gamma1, gamma'1, alpha2, gamma2, gamma'2]
    
    nbr_rounds = 1 # Nombre de rondes
    for r in range(nbr_rounds):
        # Commitment step #
        y = []  # des nombres dans F2n
        sigma = []  # des PermtationNblock
        for i in range(len(membres_anneau)):
            y[i], sigma[i] = membres_annean[i].gen_ysigma()
            
        # Calcul des c1, c2, et c3
        c1 = []  # list de bytearray
        c2 = []  # list de bytearray
        c3 = []  # list de bytearray
        for i in range(len(membres_anneau)):
            c1[i], c2[i], c3[i] = membres_anneau[i].get_c1c2c3()
        
        # Générer Sigma
        Sigma = PermutationNblock(N)
        
        # Calcul de C1, C2, et C3 (les 'master commitments')
        C1 = FU.calc_C1(Sigma.seed, c1)  # C1 = h(Sigma | c1[0] | ... | c1[N-1])
        C2 = FU.calc_C2(Sigma.seed, c2)  # C2 = h(Sigma(c2[0], ... , c2[N-1]))
        C3 = FU.calc_C3(Sigma.seed, c3)  # C3 = h(Sigma(c3[0], ... , c3[N-1]))

        alpha = C1 + C2 + C3  # De type bytearray
        
        # Challenge step #
        # Utiliser une fonction de hachage semblable a un oracle aléatoire
        beta = FU.random_oracle(alpha, M)

        # Response step #
        Pi = Sigma.apply(sigma)
        if beta == 0:
            gamma = y # y
            gamma_p = Pi # Pi
        elif beta == 1:
            gamma = [] # (y XOR s)
            for P in membres_anneau:
                gamma.append(P.y ^ P.s)
            gamma_p = Pi # Pi
        elif beta == 2:
            gamma = [] # Pi(y)
            for i in range(N):
                gamma.append(Pi[i].apply(y[i]))
            gamma_p = [] # Pi(s)
            for i in range(N):
                gamma_p.append(Pi[i].apply(s[i]))
        else:
            raise Exception("L'oracle a donnée une valeur impossible pour beta :", beta)

        Sig.append(alpha)
        Sig.append(gamma)
        Sig.append(gamma_p)

    print(Sig)
    # Verify step #
    # TODO


def verify(beta, param1, param2):
    if beta == 0:
        return True
    elif beta == 1:
        return True
    elif beta == 2:
        return True
    else:
        raise Exception("L'oracle a donné une valeur impossible pour beta :", beta)



if __name__ == "__main__":
    main()
