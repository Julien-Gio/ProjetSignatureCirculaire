# Julien Giovinazzo - June 2020
# Projet Cryptographie : Ring Signatures

from F2n import F2n

def main():
    N = 8  # Nombre de personnes dans l'anneau
    t = 3  # Nombre de signataires

    n = 10  # Longueur d'un mot
    k = 4  # k quoi

    # Commitment step #
    # Créer les t signataires et N - t autres personnes
    P = []
    for i in range(N):
        if N <= t:
            s = 1  #TODO génerer la signature
            signataire = Signataire(n, s)
        else:
            signataire = NonSignataire(n)
        P.append(signataire)

    # Générer Sigma
    # TODO
    
    # Calcul de C1, C2, et C3 (les 'master commitments')
    # TODO

    return
    ## Trash ##
    
    Hn = []  # Liste des Hi publiques
    H = calc_H(Hn)  # Clé publique maitre

    # l : parametre de sécurité
    # n et n-k : dimentions des H
    # t : nombre de signataires
    # w : poids de la clé secrète
    l,n,k,t,w = setup()
    
    sn = []  # Liste des clés privés

    
    
    N = 5  # Nbr de gens dans l'anneau
    t = 3  # Nbr de gens qui doivent signer
    y = generer_y()  # y a n elements dans F-2


def calc_H(Hn):
    pass


def setup():
    pass


def generer_y():
    pass


if __name__ == "__main__":
    main()
