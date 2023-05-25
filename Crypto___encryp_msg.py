#!/usr/local/bin/python3

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

import os
import datetime

plaintext = "42Barcelona"

homedir = os.environ['HOME']
theqspathfile = os.path.join(homedir, "Documents/42/cyber/corsair/theqs.txt")
theqs = []
with open(theqspathfile, 'r') as f:
    for line in f:
        theqs.append(int(line.strip()))
print(f"len {len(theqs)}")

for num in range(len(theqs)):
    stamp = f"p_q_{num:0>3}"
    fileNamePub = stamp + "_public.pem"
    fileNameEnc = stamp + "_message.enc"

    pathPub = os.path.join(homedir, ".ssh", fileNamePub)
    pathEnc = os.path.join(homedir, ".ssh", fileNameEnc)

    # reading public key
    with open(pathPub, 'r') as publicfile:
        publickey = RSA.import_key(publicfile.read())
        print(publickey.n)

    # create an encrypter
    cipher = PKCS1_OAEP.new(publickey)

    ciphertext = cipher.encrypt(plaintext.encode())

    with open(pathEnc, 'wb') as f:
        f.write(ciphertext)
