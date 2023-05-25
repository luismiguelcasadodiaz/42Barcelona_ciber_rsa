#!/usr/local/bin/python3

import os
import rsa
import time

homedir = os.path.join(os.environ['HOME'], "Documents/42/cyber/corsair/files")
plaintext = "42Barcelona"
keylength = 170  # length minimun to encrypt 42Barcelona

keylength = 2048

for num in range(100):  # i generate 100 keys to play with them

    stamp = f"{keylength:0>3}_{num:0>3}"
    fileNamePub = stamp + "_public.pem"
    fileNamePri = stamp + "_private.pem"
    fileNameEnc = stamp + "_message.enc"

    pathPub = os.path.join(homedir, fileNamePub)
    pathPri = os.path.join(homedir, fileNamePri)
    pathEnc = os.path.join(homedir, fileNameEnc)

    # Key generation
    (publickey, privateKey) = rsa.newkeys(keylength)

    # saving keys
    pubkeypem = publickey.save_pkcs1('PEM')
    prikeypem = privateKey.save_pkcs1('PEM')

    with open(pathPri, 'wb') as f:
        f.write(prikeypem)
    with open(pathPub, 'wb') as f:
        f.write(pubkeypem)

    # reading public key

    with open(pathPub, 'rb') as publicfile:
        keydata = publicfile.read()

    pubkey = rsa.PublicKey._load_pkcs1_pem(keydata)

    # print(f"Public Gey Exponent  = {pubkey.e}")
    # print(f"Public Key monule    = {pubkey.n}")

    with open(pathPri, 'rb') as privatefile:
        keydata = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata, 'PEM')

    # print(f"Private Gey Exponent = {privkey.e}")
    # print(f"Private Key monule   = {privkey.n}")

    cypheredtext = rsa.encrypt(plaintext.encode(), pubkey)
    pathsalida = os.path.join(homedir, "salida_encryp.txt")
    with open(pathsalida, 'a') as f:
        line1 = f"{num:0>3}-e={pubkey.e}, n={pubkey.n:>52},d={privkey.d:>52},"
        line2 = f"p={privkey.p:>28}, q={privkey.q:>25},"
        line3 = f"{plaintext}==>{cypheredtext}\n"
        f.write(line1 + line2 + line3)

    print(line1 + line2 + line3)

    with open(pathEnc, 'wb') as f:
        f.write(cypheredtext)
