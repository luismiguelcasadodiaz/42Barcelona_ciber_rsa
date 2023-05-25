#!/usr/local/bin/python3

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

import os
import datetime
import random


# save file helper
def save_file(filename, content):
    f = open(filename, "wb")
    f.write(content)
    f.close()


plaintext = "42Barcelona"

homedir = os.path.join(os.environ['HOME'], "Documents/42/cyber/corsair/files")

# Read the ps
theqspathfile = os.path.join(homedir, "theqs.txt")
theqs = []
with open(theqspathfile, 'r') as f:
    for line in f:
        theqs.append(int(line.strip()))
print(f"qs len {len(theqs)}")

# read the qs
thepspathfile = os.path.join(homedir, "theps.txt")
theps = []
with open(thepspathfile, 'r') as f:
    for line in f:
        theps.append(int(line.strip()))
print(f"Ps len {len(theqs)}")

for num in range(len(theqs)):
    stamp = f"p_q_{num:0>3}"  # prefix file name wiht p_q tells me is fake
    fileNamePub = stamp + "_public.pem"
    fileNameEnc = stamp + "_message.enc"

    pathPub = os.path.join(homedir, fileNamePub)
    pathEnc = os.path.join(homedir, fileNameEnc)

    # generate a fake public key
    idx1 = random.randrange(0, 24)
    idx2 = random.randrange(0, 24)
    p = theps[idx1]
    q = theqs[idx2]
    n = p*q
    e = 65537
    rsa_components = (n, e)
    print(stamp)
    print(f"{idx1} p= {p}")
    print(f"{idx2} q= {q}")
    print(f"n= {n}")

    rsa_key = RSA.construct(rsa_components, consistency_check=True)
    fake_public_key = rsa_key.publickey().export_key(format='PEM', pkcs=1)

    # save the publick key
    with open(pathPub, 'wb') as f:
        f.write(fake_public_key)

    # Read the public key
    with open(pathPub, 'rb') as f:
        data = f.read()
    fake_public_key = RSA.importKey(data)

    # create an encrypter
    cipher = PKCS1_OAEP.new(fake_public_key)

    thisplaintext = plaintext + f"_message_{num:0>3}"
    ciphertext = cipher.encrypt(thisplaintext.encode())

    with open(pathEnc, 'wb') as f:
        f.write(ciphertext)
