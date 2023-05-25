#!/usr/local/bin/python3

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

import os
import datetime


def lcm(a, b):
    if a > b:
        greater = a
    else:
        greater = b
    while (True):
        if ((greater % a == 0) and (greater % b == 0)):
            lcm = greater
            break
        greater += 1
    return lcm


def egcd(a, b):
    """
    Extended euclidean ALgorithm
    """
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b//a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x % m


plaintext = "42Barcelona"

homedir = os.path.join(os.environ['HOME'], "Documents/42/cyber/corsair/files")
pathfactors = os.path.join(homedir, "common_factors.txt")

factorcount = 0
paircount = 0

with open(pathfactors, 'r') as f:
    for line in f:
        factor, key_list = line.strip().split(":")
        factorcount += 1
        p = int(factor)
        for elem in eval(key_list):  # eval cause i read str

            # elem has a tuple with two numbers
            # Each number for each fake public key from pari that shares p
            paircount += 1
            print(f"p_q_{elem[0]:0>3} - p_q_{elem[1]:0>3}")

            # import first public key for which p was a common factor
            stamp1 = f"p_q_{elem[0]:0>3}"  # p_q tells me is fake
            fileNamePub1 = stamp1 + "_public.pem"
            pathPub1 = os.path.join(homedir, fileNamePub1)
            with open(pathPub1, 'rb') as publicfile1:
                publickey1 = RSA.import_key(publicfile1.read())

            # Construct first private key

            n1 = publickey1.n
            exp1 = publickey1.e
            q1 = n1 // p
            try:
                T = (p - 1) * (q1 - 1)
                d1 = modinv(exp1, T)
            except Exception:
                d1 = None
            rsa_components1 = (n1, exp1, d1, p, q1)

            privatekey1 = RSA.construct(rsa_components1,
                                        consistency_check=True)

            # import second public key for which p was a common factor
            stamp2 = f"p_q_{elem[1]:0>3}"
            fileNamePub2 = stamp2 + "_public.pem"
            pathPub2 = os.path.join(homedir, fileNamePub2)
            with open(pathPub2, 'rb') as publicfile2:
                publickey2 = RSA.import_key(publicfile2.read())

            # Construct first private key
            n2 = publickey2.n
            exp2 = publickey2.e
            q2 = n2 // p
            try:
                T = (p - 1) * (q2 - 1)
                d2 = modinv(exp2, T)
            except Exception:
                d2 = None
            rsa_components2 = (n2, exp2, d2, p, q2)

            privatekey2 = RSA.construct(rsa_components2,
                                        consistency_check=True)

            # ciphered text with the first public key
            fileNameEnc1 = stamp1 + "_message.enc"
            pathEnc1 = os.path.join(homedir, fileNameEnc1)
            with open(pathEnc1, 'rb') as f:
                ciphertext1 = f.read()

            # ciphered text with the second public key
            fileNameEnc2 = stamp2 + "_message.enc"
            pathEnc2 = os.path.join(homedir, fileNameEnc2)
            with open(pathEnc2, 'rb') as f:
                ciphertext2 = f.read()

            # create an encrypter for first private key
            cipher1 = PKCS1_OAEP.new(privatekey1)

            plaintext1 = cipher1.decrypt(ciphertext1)
            line1 = f"Msg {fileNameEnc1}, cifrado con la clave pública "
            line2 = f"{fileNamePub1} is {plaintext1.decode()}"
            print(line1 + line2)

            # create an encrypter for second private key
            cipher1 = PKCS1_OAEP.new(privatekey2)

            plaintext2 = cipher1.decrypt(ciphertext2)
            line1 = f"Msg {fileNameEnc2}, cifrado con la clave pública "
            line2 = f"{fileNamePub2} is {plaintext2.decode()}"
            print(line1 + line2)

    print("factorcount =", factorcount)
    print("paircount =", paircount)
