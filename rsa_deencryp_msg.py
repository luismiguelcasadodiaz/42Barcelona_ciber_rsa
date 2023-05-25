#!/usr/local/bin/python3

import os
import rsa

homedir = os.environ['HOME']
plaintext = "42Barcelona"
keylength = 170
for num in range(100):  # i generated 100 keys to play with them

    stamp = f"{keylength:0>3}_{num:0>3}"
    fileNamePub = stamp + "_public.pem"
    fileNamePri = stamp + "_private.pem"
    fileNameEnc = stamp + "_message.enc"

    pathPub = os.path.join(homedir, ".ssh", fileNamePub)
    pathPri = os.path.join(homedir, ".ssh", fileNamePri)
    pathEnc = os.path.join(homedir, ".ssh", fileNameEnc)

    # reading private key

    with open(pathPri, 'rb') as privatefile:
        keydata = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata, 'PEM')

    # print(f"Private Gey Exponent = {privkey.e}")
    # print(f"Private Key monule   = {privkey.n}")

    with open(pathEnc, 'rb') as f:
        cypheredtext = f.read()

    deciferedtext = rsa.decrypt(cypheredtext, privkey)
    print(deciferedtext.decode())
