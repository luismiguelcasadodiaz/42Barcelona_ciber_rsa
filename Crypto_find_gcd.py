#!/usr/local/bin/python3

import os
from Crypto.PublicKey import RSA


def gcd(a, b):  # Greatest Common Divisor Generator (Euclidean Algorithm)
    while b != 0:  # While remainder exists
        t = b  # Initially r[k-1]
        b = a % t  # Initially r[k] = r[k-2] mod r[k-1] (where r[k-2] is a)
        a = t  # Predecessor of remainder (b)
    return a


homedir = os.path.join(os.environ['HOME'], "Documents/42/cyber/corsair/files")
plaintext = "42Barcelona"

gcd_dict = {}
allcount = 0
foundfactors = 0

key1 = ()
key2 = ()
p = 0

for num in range(0, 100):  # i generated 100 keys to play with them
    stamp = f"p_q_{num:0>3}"
    fileNamePub = stamp + "_public.pem"
    fileNamePri = stamp + "_private.pem"
    fileNameEnc = stamp + "_message.enc"

    pathPub = os.path.join(homedir, fileNamePub)
    pathPri = os.path.join(homedir, fileNamePri)
    pathEnc = os.path.join(homedir, fileNameEnc)

    # reading first public key

    with open(pathPub, 'rb') as publicfile:
        publickey1 = RSA.import_key(publicfile.read())

    for num2 in range(num + 1, 100):  # i generated 100 keys to play with them
        allcount += 1
        stamp2 = f"p_q_{num2:0>3}"
        fileNamePub2 = stamp2 + "_public.pem"
        fileNamePri2 = stamp2 + "_private.pem"
        fileNameEnc2 = stamp2 + "_message.enc"

        pathPub2 = os.path.join(homedir, fileNamePub2)
        pathPri2 = os.path.join(homedir, fileNamePri2)
        pathEnc2 = os.path.join(homedir, fileNameEnc2)

        if pathPub != pathPub2:  # check if compare different fake public keys

            # reading first public key

            with open(pathPub2, 'rb') as publicfile2:
                publickey2 = RSA.import_key(publicfile2.read())

            if publickey1.n != publickey2.n:
                gcd_n1_n2 = gcd(publickey1.n, publickey2.n)
                if gcd_n1_n2 != 1:
                    foundfactors += 1
                    line1 = f"{num:0>3}-{num2:0>3} n1={publickey1.n} "
                    line2 = f"n2={publickey2.n} p= {gcd_n1_n2}\n"
                    print(line1 + line2)
                    if gcd_n1_n2 in gcd_dict.keys():
                        gcd_dict[gcd_n1_n2].append((num, num2))
                    else:
                        gcd_dict[gcd_n1_n2] = [(num, num2)]
                else:
                    pass
                    # print(f"{num:0>3}-{num2:0>3} primes")
            else:  # Both public keys have same modulus
                pass
                # print(f"{num:0>3}-{num2:0>3} tienen igual n\n")

print(f"Allcount = {allcount}")
print(f"Pairs with common factors = {foundfactors}")
print(f"Num factors {len(gcd_dict.keys())}")

pathfactors = os.path.join(homedir, "common_factors.txt")

with open(pathfactors, 'w') as f:
    for k, v in gcd_dict.items():
        f.write(f"{k}:{v}\n")
