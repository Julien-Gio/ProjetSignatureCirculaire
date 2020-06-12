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

    # Remarque : Si 'falsifier' est vrai, alors le code de verification risque de crasher (desfois)
        
    # PARAMETRES DE LA SIGNATURE
    falsifier = False  # Si True, la signature sera modifiée avant d'etre verifié. Sinon la signature sera authentique
    N = 21  # Nombre de personnes dans l'anneau
    t = 3  # Nombre de signataires
    M = b'Le chat est sur le canape.'  # Message à signer par l'anneau (pas d'accents, merci)

    n = 8  # Longueur d'un mot. Doit etre un multiple de 8
    k = 4  # k quoi
    w = 4  # Poid du secret s des signataires


    # Générer la signature #
    print("Message à signer par", t,"parmi", N, "personnes:", M, "\n")

    
    # Creer les membres de l'anneau
    membres_anneau = []
    for i in range(N):
        if i < t:
            signataire = Signataire(n, k, w)
        else:
            signataire = NonSignataire(n, k, w)
        membres_anneau.append(signataire)


    Sig = []  # Signature. Ex pour 2 rounds : [alpha1, gamma1, gamma'1, alpha2, gamma2, gamma'2]
    
    nbr_rounds = 10 # Nombre de rondes
    for r in range(nbr_rounds):
        # Commitment step #
        y = [None]*N  # des nombres dans F2n
        sigma = [None]*N  # des PermtationNblock
        for i in range(len(membres_anneau)):
            y[i], sigma[i] = membres_anneau[i].get_ysigma()
            
        # Calcul des c1, c2, et c3
        c1 = [None]*N  # list de bytearray
        c2 = [None]*N  # list de bytearray
        c3 = [None]*N  # list de bytearray
        for i in range(len(membres_anneau)):
            c1[i], c2[i], c3[i] = membres_anneau[i].get_c1c2c3()
        
        # Générer Sigma
        Sigma = PermutationNblock(N)
        
        # Calcul de C1, C2, et C3 (les 'master commitments')
        C1 = FU.calc_C1(n, Sigma.seed, c1)  # C1 = h(Sigma | c1[0] | ... | c1[N-1])
        C2 = FU.calc_C2(n, Sigma, c2)  # C2 = h(Sigma(c2[0], ... , c2[N-1]))
        C3 = FU.calc_C3(n, Sigma, c3)  # C3 = h(Sigma(c3[0], ... , c3[N-1]))

        alpha = C1 + C2 + C3  # De type bytearray
        
        # Challenge step #
        # Utiliser une fonction de hachage semblable a un oracle aléatoire
        beta = FU.random_oracle(alpha, M)

        # Response step #
        # Pi est composé de la graine de Sigma et de Sigma(graines des sigma)
        Pi = Sigma.apply(sigma)
        graine_Pi = FU.float2bytearray(Sigma.seed) # Graine de Pi : graine des composantes
        for i in sigma:
            graine_Pi += FU.float2bytearray(i.seed)
        s = []
        for P in membres_anneau:
            s.append(P.s)
            
        if beta == 0:
            gamma = y  # y
            gamma_p = graine_Pi  # Pi
        elif beta == 1:
            gamma = []  # (y XOR s)
            for P in membres_anneau:
                gamma.append(P.y ^ P.s)
            gamma_p = graine_Pi  # Pi
        elif beta == 2:
            gamma = []  # Pi(y) = Sigma(sigma(y))
            y_permu = Sigma.apply(y)
            for i in range(N):
                gamma.append(Pi[i].apply(y_permu[i]))
                
            gamma_p = []  # Pi(s) = Sigma(sigma(s))
            s_permu = Sigma.apply(s)
            for i in range(N):
                gamma_p.append(Pi[i].apply(s_permu[i]))
        else:
            raise Exception("L'oracle a donnée une valeur impossible pour beta :", beta)


        Sig.append(alpha)
        Sig.append(gamma)
        Sig.append(gamma_p)

    # Récuperer la clé publique H
    H = []
    for P in membres_anneau:
        H.append(P.H)

    if falsifier:
        # Modifier un octet aléatoire dans la signature
        Sig[random.randint(0, len(Sig)-1)][0] = random.randint(0, 255)
    
    print("Signature: ", Sig)
    # Verify step #
    verify(Sig, M, H)


def verify(Signature, M, H):
    # Calcule nombre de roundes
    NBR_RONDES = len(Signature) // 3
    for r in range(NBR_RONDES):
        alpha = Signature[r * 3]
        gamma = Signature[r * 3 + 1]
        gamma_p = Signature[r * 3 + 2]
        
        # Calculer beta avec alpha, M, et l'oracle aléatoire
        beta = FU.random_oracle(alpha, M)
        print("\nRonde numéro", r+1," -> beta:", beta, end=' -> ')

        # Calculs de n et N
        # alpha = C1 | C2 | C3 => len(alpha) = n // 3 * 8
        n = len(alpha) // 3 * 8
        C1 = alpha[0        :  n // 8]
        C2 = alpha[n // 8   :2*n // 8]
        C3 = alpha[2*n // 8 :3*n // 8]
        
        # H = [H_1, ..., H_N] => len(H) = N
        N = len(H)
        
        if beta == 0:
            # gamma = y
            # gamma' = graine de Pi
            Sigma, sigma = FU.decompser_Pi(gamma_p, n, N)

            # C1
            concat = FU.float2bytearray(Sigma.seed)
            for i in range(len(sigma)):
                mul = FU.matrice_mul(H[i], gamma[i].to_np_array())[0, :]  # type np.array
                mul_ba = mul.tobytes()
                hash_in = FU.float2bytearray(sigma[i].seed) + mul_ba
                concat += FU.hachage(n, hash_in)  # = h(sigma_i | H_i * y_i')
            C1_calc = FU.hachage(n, concat)
            
            # C2
            c2_calc = []
            for i in range(len(sigma)):
                permu = sigma[i].apply(gamma[i])  # sigma(y)
                c2_calc.append(permu.to_bytearray())
            for i in range(len(c2_calc)):
                c2_calc[i] = FU.hachage(n, c2_calc[i])  # h(sigma(y))

            c2_calc = Sigma.apply(c2_calc)  # Sigma( liste de s h(sigma(y)) )
            concat = bytearray()
            for c in c2_calc:
                concat += c
            C2_calc = FU.hachage(n, concat)

            if C1 != C1_calc and C2 != C2_calc:
                print("Singature erronée ou falsifiée!")
                return False
            else:
                print("C1 et C2 valides :D")
            
        elif beta == 1:
            # gamma = y ^ s
            # gamma' = graine de Pi
            Sigma, sigma = FU.decompser_Pi(gamma_p, n, N)
            
            # C1
            # Hy = H(y ^ s)
            Hy = []  # type bytes
            c1_calc = []
            for i in range(N):
                mul = FU.matrice_mul(H[i], gamma[i].to_np_array())[0, :] 
                Hy.append(mul.tobytes())
                concat = FU.float2bytearray(sigma[i].seed) + Hy[i]  # sigma | Hy
                c1_calc.append(FU.hachage(n, concat))
            C1_calc = FU.float2bytearray(Sigma.seed)
            for c in c1_calc:
                C1_calc += c
            C1_calc = FU.hachage(n, C1_calc)
            
            # C3
            hachers = []  # c3 calculés
            for i in range(N):
                sxor = sigma[i].apply(gamma[i]) # sigma(y^s)
                hachers.append(FU.hachage(n, sxor.to_bytearray()))  # h(sigma(y^s))
            
            hachers = Sigma.apply(hachers)  # Sigma( hachers )
            concat = bytearray()
            for h in hachers:
                concat += h
            
            C3_calc = FU.hachage(n, concat)
            
            if C1 != C1_calc and C3 != C3_calc:
                print("Singature erronée ou falsifiée!")
                return False
            else:
                print("C1 et C3 valides :D")
        
        elif beta == 2:
            # gamma = Pi(y) = [sigma(y_1), ... , sigma(y_N)] dans le desordre
            # gamma' = Pi(s)
            
            # C2
            concat = bytearray()
            for i in range(N):
                concat += FU.hachage(n, gamma[i].to_bytearray())  # h(Pi(y)_i)
                
            C2_calc = FU.hachage(n, concat)

            # C3
            concat = bytearray()
            for i in range(N):
                xor = gamma[i] ^ gamma_p[i]
                hacher = FU.hachage(n, xor.to_bytearray())
                concat += hacher
            
            C3_calc = FU.hachage(n, concat)
            
            if C2 != C2_calc and C3 != C3_calc:
                print("Singature erronée ou falsifiée!")
                return False
            else:
                print("C2 et C3 valides :D")
        else:
            raise Exception("L'oracle a donné une valeur impossible pour beta :", beta)

    print("Signature valide !")

if __name__ == "__main__":
    main()
