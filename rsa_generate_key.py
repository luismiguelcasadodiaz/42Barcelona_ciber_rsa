#!/usr/local/bin/python3

import rsa
import os
import datetime
t = datetime.datetime.now()
stamp = f"{t.year:4d}{t.month:0>2}{t.day:0>2}_{t.hour}{t.minute}{t.second}"
# 2015 5 6 8 53 40

plaintext = "42Barcelona"
homedir = os.path.join(os.environ['HOME'], "Documents/42/cyber/corsair/files")
for keylength in range(16, 180):
    stamp = f"{keylength:0>3}"
    fileNamePub = stamp + "_public.pem"
    fileNamePri = stamp + "_private.pem"

    pathPub = os.path.join(homedir, fileNamePub)
    pathPri = os.path.join(homedir, fileNamePri)

    (publickey, privateKey) = rsa.newkeys(keylength)

    pubkeypem = publickey.save_pkcs1('PEM')
    prikeypem = privateKey.save_pkcs1('PEM')

    with open(pathPri, 'wb') as f:
        f.write(prikeypem)
    with open(pathPub, 'wb') as f:
        f.write(pubkeypem)
