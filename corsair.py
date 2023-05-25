#!/usr/local/bin/python3

import os
import rsa
import time


def egcd(a, b):
    """
    Extended euclidean ALgorithm
    """
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x % m


def gcd(a, b):  # Greatest Common Divisor Generator (Euclidean Algorithm)
    while b != 0:  # While remainder exists
        t = b  # Initially r[k-1]
        b = a % t  # Initially r[k] = r[k-2] mod r[k-1] (where r[k-2] is a)
        a = t  # Predecessor of remainder (b)
    return a


def carmichael(n):
    coprimes = [x for x in range(1, n) if gcd(x, n) == 1]

    k = 1
    while not all(pow(x, k, n) == 1 for x in coprimes):
        k += 1
    return k


homedir = os.path.join(os.environ['HOME'], "Documents/42/cyber/corsair/files")
for keylength in range(32, 1000):
    ti = time.time()
    stamp = stamp = f"{keylength:0>3}"
    fileNamePub = stamp + "_public.pem"
    fileNamePri = stamp + "_private.pem"

    pathPub = os.path.join(homedir, fileNamePub)
    pathPri = os.path.join(homedir, fileNamePri)
    with open(pathPri, 'rb') as privatefile:
        keydata = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata, 'PEM')

    # print(f"Private Gey Exponent = {privkey.e}")
    # print(f"Private Key monule   = {privkey.n}")

    with open(pathPub, 'rb') as publicfile:
        keydata = publicfile.read()

    pubkey = rsa.PublicKey._load_pkcs1_pem(keydata)

    # print(f"Public Gey Exponent  = {pubkey.e}")
    # print(f"Public Key monule    = {pubkey.n}")

    totient = carmichael(pubkey.n)
    d = modinv(pubkey.e, totient)
    tf = time.time()
    duracion = int(tf - ti)

    pathtiempos = os.path.join(homedir, "tiempos.txt")
    with open(pathtiempos, 'a') as f:
        line1 = f"len(n)= {keylength} bits, {duracion:0>3} segundos, "
        line2 = f"n={pubkey.n:0>10}, e={pubkey.e}, "
        line3 = f"λ(n) = {totient}, d = {d}\n"
        f.write(line1 + line2 + line3)
    print(line1 + line2 + line3)

"""
len(n)= 16 bits, 000 segundos, n=0000034579, λ(n) = 5700
len(n)= 17 bits, 000 segundos, n=0000043739, λ(n) = 1140
len(n)= 18 bits, 000 segundos, n=0000134773, λ(n) = 22338
len(n)= 19 bits, 000 segundos, n=0000155647, λ(n) = 77420
len(n)= 20 bits, 001 segundos, n=0000690077, λ(n) = 172104
len(n)= 21 bits, 001 segundos, n=0000697219, λ(n) = 115920
len(n)= 22 bits, 009 segundos, n=0002604851, λ(n) = 1300776
len(n)= 23 bits, 008 segundos, n=0002351777, λ(n) = 1174338
len(n)= 24 bits, 035 segundos, n=0009771331, λ(n) = 4882532
len(n)= 25 bits, 030 segundos, n=0012229999, λ(n) = 185196
len(n)= 26 bits, 082 segundos, n=0033757673, λ(n) = 324480
len(n)= 27 bits, 133 segundos, n=0051295609, λ(n) = 2136720

"""
