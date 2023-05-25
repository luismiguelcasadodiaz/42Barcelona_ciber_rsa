#!/usr/local/bin/python3


def my_mod_inv(u: int, v: int):
    u1 = 1
    u3 = u
    v1 = 0
    v3 = v
    iter = 1
    while (v3 != 0):
        # Step X3. Divide and "Subtract"
        q = u3 // v3
        t3 = u3 % v3
        t1 = u1 + q * v1
        # Swap
        u1 = v1
        v1 = t1
        u3 = v3
        v3 = t3
        iter = -iter

    # Make sure u3 = gcd(u,v) == 1
    if (u3 != 1):
        return 0   # Error: No inverse exists

    # Ensure a positive result
    if (iter < 0):
        inv = v - u1
    else:
        inv = u1

    return inv


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


e = 65537
T = 14855328166001940623503692909056920300048344042919675112322980742425878768547828331702720989395476381020701907136700069134991233854750214422574280451523747306003986574152817152866875698233847494004185397060092513292851324396853592652509074915420123622937819404719767756069645811352535026839287340497175624388757233196726181172370368961883087456658730880052668316119953921465897712681602166344762473962375464570123370554545856039307677943704784329098204083581371672224563843000237372763543745836113708850786049970541840680488983932054315406271543569846689809746227301717738647787069994666304330922425944962537239318970
print("d= ", modinv(e, T))
print("-------------")
print("d= ", my_mod_inv(e, T))
