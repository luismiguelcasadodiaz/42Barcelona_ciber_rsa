#!/usr/local/bin/python3

import os
import rsa
import pprint


def gcd(a, b):  # Greatest Common Divisor Generator (Euclidean Algorithm)
    while b != 0:  # While remainder exists
        t = b  # Initially r[k-1]
        b = a % t  # Initially r[k] = r[k-2] mod r[k-1] (where r[k-2] is a)
        a = t  # Predecessor of remainder (b)
    return a


homedir = os.environ['HOME']
plaintext = "42Barcelona"
keylength = 170
plaintext = "4"
keylength = 90
gcd_dict = {}
allcount = 0
primescoutn = 0

for num in range(100):  # i generated 100 keys to play with them

    stamp = f"{keylength:0>3}_{num:0>3}"
    fileNamePub = stamp + "_public.pem"
    fileNamePri = stamp + "_private.pem"
    fileNameEnc = stamp + "_message.enc"

    pathPub = os.path.join(homedir, ".ssh", fileNamePub)
    pathPri = os.path.join(homedir, ".ssh", fileNamePri)
    pathEnc = os.path.join(homedir, ".ssh", fileNameEnc)

    # reading first public key

    with open(pathPub, 'rb') as publicfile:
        keydata = publicfile.read()
    pubkey1 = rsa.PublicKey.load_pkcs1(keydata, 'PEM')

    for num2 in range(100):  # i generated 100 keys to play with them
        allcount += 1
        stamp = f"{keylength:0>3}_{num2:0>3}"
        fileNamePub2 = stamp + "_public.pem"
        fileNamePri2 = stamp + "_private.pem"
        fileNameEnc2 = stamp + "_message.enc"

        pathPub2 = os.path.join(homedir, ".ssh", fileNamePub2)
        pathPri2 = os.path.join(homedir, ".ssh", fileNamePri2)
        pathEnc2 = os.path.join(homedir, ".ssh", fileNameEnc2)

        if pathPub != pathPub2:

            # reading first public key

            with open(pathPub2, 'rb') as publicfile2:
                keydata = publicfile2.read()
            pubkey2 = rsa.PublicKey.load_pkcs1(keydata, 'PEM')

            gcd_n1_n2 = gcd(pubkey1.n, pubkey2.n)

            if gcd_n1_n2 != 1:
                primescoutn += 1
                line1 = f"{num:0>3}-{num2:0>3} n1={pubkey1.n}"
                line2 = f" n2={pubkey2.n} p= {gcd_n1_n2}"
                print(line1 + line2)
                if gcd_n1_n2 in gcd_dict.keys():
                    gcd_dict[gcd_n1_n2] += 1
                else:
                    gcd_dict[gcd_n1_n2] = 1
            else:
                print(f"{num:0>3}-{num2:0>3} primes")

print(f"Allcount = {allcount}")
print(f"preimescount = {primescoutn}")
print(f"num factors {len(gcd_dict.keys())}")
for k, v in gcd_dict.items():
    print(v, k)
