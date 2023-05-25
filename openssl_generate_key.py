#!/usr/local/bin/python3

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


import os
import datetime


# save file helper
def save_file(filename, content):
    f = open(filename, "wb")
    f.write(content)
    f.close()


t = datetime.datetime.now()
stamp = f"{t.year:4d}{t.month:0>2}{t.day:0>2}_{t.hour}{t.minute}{t.second}"
# 2015 5 6 8 53 40


homedir = os.environ['HOME']
for keylength in range(512, 513):
    stamp = f"{keylength:0>3}_512"
    fileNamePub = stamp + "_public.pem"
    fileNamePri = stamp + "_private.pem"

    pathPub = os.path.join(homedir, ".ssh", fileNamePub)
    pathPri = os.path.join(homedir, ".ssh", fileNamePri)

    # generate private key & write to disk
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=keylength,
        backend=default_backend()
    )
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    save_file(pathPri, pem)

    # generate public key
    public_key = private_key.public_key()
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    save_file(pathPub, pem)
