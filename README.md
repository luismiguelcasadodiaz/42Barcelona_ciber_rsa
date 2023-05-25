# 42 Barcelona Cybersecurity bootcamp - RSA asymetric key study.

The aim of this exercise is to introduced the bootcamper inside RSA and make me aware of
the importance of entropy in primes generation.

I have to proof that it is posible break RSA security when we use weak random generation.


Please execute the files in this order:


1.- rsa___encryp_msg.py    # generates real e,n,p,q,d of RSA asymetric keys.

2.- Inside of folder files   # select ps and qs

```
    Bash $ cat salida_encryp.txt | cut -d ',' -f4  | sed  's/p=//g' > theps.txt
    Bash $ cat salida_encryp.txt | cut -d ',' -f5  | sed  's/q=//g' > theqs.txt
```

3.- Crypto_generate_fake_key.py  # creates RSA asymetric keys with low entropy and ciphers messages

4.- Crypto_find_gcd.py           # detects common ps

5.- Crypto_deencryp_msg.py       # creates private kesy form public keys

# Approach **ONE**
## corsair.py

After studing RSA mathematics i learnt that is mathemattically possible obtaing a private key
from a public key.

Given p & q positive big primes.

Being e (exponent) = 65537 and n (modulus) = p * q.

n is the open secret (Ellis - 1970).

encryption : C = pow(M,e) mod n   
decryption : M = pow(C,d) mod n

From public key we con go to private key with this formula:
d = modular inverse of (e, λ(n))

λ(n) is the Carmichael totien function.

a ** k congruent with 1  (mod n)
meaning that for every **a**, smaller than **n**, and coprime with **n**, **k** is the smallest number that pow(a, k) % n = 1.

d is de **modular multiplier inverse** of e and λ(n).

```
def modinv(a,m):
    g, x, y = egcd(a,m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m
```


```
def carmichael(n):
    coprimes = [x for x in range(1, n) if gcd(x, n) == 1]
    k = 1
    while not all(pow(x, k, n) == 1 for x in coprimes):
        k += 1
    return k
```

egcd is the  extended euclidean algoritm. this algorithm, aside calculate
the gcd thru the remainders of the division, it takes into consiseration
the quiotiens of such division.

```
def egcd(a,b):
    """
    Extended euclidean ALgorithm
    """
    if a == 0:
        return(b, 0, 1)
    g, y, x = egcd(b%a, a)
    return (g, x - (b//a) * y , y)
```

Althoug it is mathematically possible to infer private key from public key, computationally
is not possible nowadays.

I timeit the algorithm with these results:


|len(n)  |(secs)| n            | e   |λ(n)     |d
|--------|------|:------------:|-----|---------|-----
| 16 bits|  000 |  n=0000055189|65537| 4560    | 833|
| 17 bits|  000 |  n=0000049163|65537| 24360   | 19913|
| 18 bits|  000 |  n=0000166493|65537| 82830   | 28643|
| 19 bits|  000 |  n=0000142859|65537| 71052   | 2873|
| 20 bits|  003 |  n=0000711197|65537| 354750  | 276473|
| 21 bits|  001 |  n=0000637253|65537| 45402   | 21719|
| 22 bits|  012 |  n=0003330841|65537| 831796  | 394861|
| 23 bits|  007 |  n=0002630651|65537| 262740  | 192173|
| 24 bits|  030 |  n=0009554689|65537| 367250  | 135223|
| 25 bits|  045 |  n=0009027989|65537| 4510950 | 2032223|
| 26 bits|  195 |  n=0050975047|65537| 8493456 | 8041937 |
| 27 bits|  142 |  n=0038412643|65537| 6400008 | 4579721 |
| 28 bits|  793 |  n=0178359197|65537| 44583120| 32650433|
| 29 bits|  993 |  n=0178371139|65537| 89172212| 31403553|
| 30 bits| 2628 |  n=0573445219|65537| 95566020| 45780173|
| 31 bits| 2690 |  n=0615414277|65537| 51280368| 37485521|
|512 bits| ???? |  n=10198396198775561957312427155980896031621481057689583114412695093823692869122007487913250993135767612909846550167087384856500083695811014490975969639561161|65537|?|?|


All this you can find it in corsair.py.
It is mathematically feasible but computationally impracticable.
# Approach **TWO**
## openssl_generate_key.py & rsa_generate_key.py

I need different approach.

I need pairs of keys with open secret that have common factors. This is only possible if the
rsa random generator is weak,  with low entropy.

It is quite relevant to me that imported library matters.

I uncovered that
```
import rsa
(publickey, privateKey)  rsa.newkeys(keylength,True,4)  

```

allows keylenght starting in 16 Bits, but 

```
from cryptography.hazmat.primitives.asymmetric import rsa 

private_key = rsa.generate_private_key(  
    public_exponent=65537,  
    key_size=keylength,  
    backend=default_backend()  
)

```

raises ValueError: key_size must be at least 512-bits.

Additionally i uncover that 

```
import rsa
plaintext="4"
(publickey, privateKey) = rsa.newkeys(keylength,True,4)
cypheredtext = rsa.encrypt(plaintext.encode('ascii'),publickey)
```

works with keylenght >= 90 bits

if we add one more letter to the plaintext

```
import rsa
plaintext="42"
(publickey, privateKey) = rsa.newkeys(keylength,True,4)
cypheredtext = rsa.encrypt(plaintext.encode('ascii'),publickey)
```

works with keylenght >= 98 bits




|To encryp      |keylenght >=  |-----BEGIN RSA PUBLIC KEY-----
|---------      |:-----------: |--------------------------------------------
|"4"            |>=  90 bits   |MBMCDAOPHm2kz6tYv+tCCwIDAQAB
|"42"           |>=  98 bits   |MBQCDQLdTVvzDOKJQOOcQL0CAwEAAQ==
|"42B"          |>= 106 bits   |MBUCDgL+FzV3A+pDocXNCmMpAgMBAAE=
|"42Ba"         |>= 114 bits   |MBYCDwIQZLre60pgkhdw3DbZ6QIDAQAB
|"42Bar"        |>= 122 bits   |MBcCEAMS0QDTwtxLRpZJcGvhCxkCAwEAAQ==
|"42Barc"       |>= 130 bits   |MBgCEQIny18a4Vn/LCGRgZBf9cRHAgMBAAE=
|"42Barce"      |>= 138 bits   |MBkCEgIxB1y1LNZQIPA+sN/+P9cCkwIDAQAB
|"42Barcel"     |>= 146 bits   |MBoCEwMjAA9Q97ISXi2o2Mk3ICW2JssCAwEAAQ==
|"42Barcelo"    |>= 154 bits   |MBsCFAIaRDbXdW29NmXte7BBI07nHg4rAgMBAAE=
|"42Barcelon"   |>= 162 bits   |MBwCFQNtXHe4G4RCQwSdYhhR/EJjGRd+AwIDAQAB
|"42Barcelona"  |>= 170 bits   |MB0CFgOd9wlBGunhTRvI5GQzi+7rMOT1LR8CAwEAAQ==

According to this i will use pairs of public-private keys w a modulus of n
that fits in 170 bits.

plaintext lenght has to be no longer than k-11 bytes, being k the lenght in bytes
required to hold n

```

```

Another learning is about decoding. 
I have to encrypt a bytes array, so i encode the plaintext
I have to decode the encrypted token as it is.

I tryed otherwise and i got errors.
```
cypheredtext = rsa.encrypt(plaintext.encode(),pubkey,)
deciferedtext = rsa.decrypt(cypheredtext,privkey)
  
```
## rsa_find_gcd.py
I generated 100 pairs of public-private RSA keys with a modulus(n) of length of 170 bits
After calculate 9900 gdc between all diferente 99 pairs i concluded that rsa uses a
strong primes generator, despite deal wiht 170 bits.

I repeated the experiment wiht a modulus of lenth 90 getting same results.

# APPROACH **THREE**
## Crypto_generate_key.py
My final approach is generate the pairs of public and private keys using primes not generated randomly.
## rsa___encryp_msg.py
1.- wiht rsa i generate 100 pairs of keys wiht 2048 bits for the moduls and save all parameters

```

keylength=2048  # I choose this length as it is the minimun to encrypt 42Barcelona

for num in range(100):  #  i generate 100 keys to play with them
    # Key generation
    (publickey, privateKey) = rsa.newkeys(keylength)
     with open("salida_encryp.txt", 'a') as f:

        line = f"e={pubkey.e}, n={pubkey.n:>52},d={privkey.d:>52}, p={privkey.p:>28}, q={privkey.q:>25},{plaintext}==>{cypheredtext}\n"
        f.write(line)

```

An example of the output is this:

---
e=65537, 

n=17328941834950607110733842651814716676475769238334612209056527755073956524294507416009044547582351732337081195250619421218451671406480616277823417768900642551813473392868185811223980348066848104151064128298019922172429656833486422735413208138547962617717838173933196789105174005992408005611727938985636343060263990145339427014243006058039716477207624098215078777482996114331903098031267522316161824116127029834578075395776946305156738449860576040139092315457448596005624180884527997289368750872051640946903139303661980103441119300931067579242714037814905675890840016912470091219671005990997422904657974711740027171889,

d=6095286131182101639022789276433661120071401383677761884785252266810577929994308328941521505574993852843956783388273477545932037311170654232515760965694151580090699736826486096713844011529929390983571574614736030729494002614180219065516353724000299590515763699673589764292727332440254960484998367281211387265598667040423184074928138206451373992674576959662315100335016201592923584587227709526911518904137896779476555101118408967514029363901356966649501945574122910871452474185278301139452000994196688369818347591687390696012600642965162922284014261396541572647412994140555478998793682507380203447882230608246468433777,

p=2438593310261074657282043163376290856047222440000419075612452801035390644758889499482865075970053142986916368260984858690118496306023036284680524966770279394068431807148336577519722485636930557224182394703700065632044053829756756845734485338498233667494865837330182593896052648121623458208640331155181192046654120922889117408243, 

q=7106122108198262348522407478614701756903907760914086476746983907364481778251431024879716532839231532537338659994546536609077608469996401195324704067631102143259157263411944667072123556656545310258351456012224748216378364932703949312438531510368391333781777972803199738627758553181605506123,

4==>b'_\x13+\x03\xdb\xae\x94\xd8\xcb>k\x89U\x83\xe7fg\xa3^\xbd\x94\x96\x84o\xdc\xcf\x13\xc2\x19\x08B\xf5gy\x90\xabI`\xc5g2\x9a\xc1^#S\xf0t\xe6\x8f6\xa1&\x98\x91\xf9\xbbk\xe4\xee\xe2\xa6\x87w\xef\x0f\xe1*\x9en\xc3$]\xbd\xc8\xcd\x98v\x0b\xac\x99 \x00\x97m\xbev3k\x0eXT5\x0fj$\xfc\xaeC\x1b\xaa\xa0\xb0\xaa%\xc9\xba8@\x05\xfd\xc0q\x14\xb1\xef\xcb\\\xf6\xdc#\xe0\x8eX\xed\xc0\x9b\xf3\xb1\xeb\x837v"_t\x0b\xb8\xe2\xd3\xee\x87\x04\xb5\r`p\x1b\x15\xbf\xbf\x1a#\xc0\x07\xbc\x8f/\xbc\x0f\xd7+\xe7\xa3\xb0\xcd\x1e\xd9\xd4\x06D\x8d\x98w\'\x89\xb5\xaf9\xb0I\xb7\x12D\x08,9D|\xac\x1dE\x8f\xe3;\xfa+\xe8\xa9\xc7\x9e\r\xcf\xb0"\x92=\xdc<T\x89Y\xb7\x86\x8dbU\xa5\xe8f\xfa\x1b\x9d\xc3\xe5\xce\x1d"e!\xa8\xbb\x15\xd7P#\xae\x9a9\xad"\xa8\x12K~m\xcd\xf7r\xcb$\xeb\xd8- \x1d'

---

2.- I collect the qs in a file. I collect the ps in a file. All qs and the P are prime positive integers

```
Bash $ cat salida_encryp.txt | cut -d ',' -f4  | sed  's/p=//g' > theps.txt
Bash $ cat salida_encryp.txt | cut -d ',' -f5  | sed  's/q=//g' > theqs.txt

```
# Crypto_generate_fake_key.py
3.- My prime generator with low entropy will use random.randrange(0,24) for selecting from a 25 size small subset of ps and qs.
    I generate 100 *fake* public keys.


```
    from Crypto.PublicKey import RSA
    #generate a fake public key
    idx = random.randrange(0,24)
    p = theps[idx]
    q = theqs[idx]
    n = p*q
    e = 65537
    rsa_components = (n,e)
   
    rsa_key= RSA.construct(rsa_components,consistency_check=True,)
    fake_public_key  = rsa_key.export_key(format='PEM',pkcs=1)

```
# Crypto___encryp_msg.py
4.- Ciper plaintext wiht the different 100 fake public keys in this way.

```
    from Crypto.Cipher import PKCS1_OAEP
    from Crypto.PublicKey import RSA
    # reading public key
    with open(pathPub,'r') as publicfile:
        publickey = RSA.import_key(publicfile.read())
    
    
    # create an encrypter    
    cipher = PKCS1_OAEP.new(publickey)

    ciphertext = cipher.encrypt(plaintext.encode())

    with open(pathEnc, 'wb') as f:
        f.write(ciphertext)

```
# Crypto_find_gcd.py
5.- Uncover common factors between ns from the 100 fake public keys.

As i have created 100 public keys, for each one of them i try to find commond divisor wiht other 99 public keys

```

for num in range(0, 100):  #  i generated 100 keys to play with them
    # reading first public key
    # ...... more code here
    with open(pathPub,'rb') as publicfile:
        publickey1 = RSA.import_key(publicfile.read())

    for num2 in range(num + 1, 100):  #  i generated 100 keys to play with them
    # ...... more code here
        if pathPub != pathPub2:

            # reading first public key
            with open(pathPub2,'rb') as publicfile2:
                publickey2 = RSA.import_key(publicfile2.read())

            gcd_n1_n2 = gcd(publickey1.n, publickey2.n)

            if gcd_n1_n2 != 1:  # figure out how to track this factor
                if gcd_n1_n2 in gcd_dict.keys():
                    gcd_dict[gcd_n1_n2].append((num, num2))
                else:
                    gcd_dict[gcd_n1_n2] = [(num, num2)]

```
i use a dictionary for registering common factors and pairs of fake public keys

181772......22875527:[(61, 81)]
199546......13919607:[(69, 75)]
262964......95484463:[(76, 93)]

Found commond factores are saved in file common_factors.txt

Playing wiht my level of entropy i created this table that show entropy importance.


|entropy               |   |% collisions|
|----------------------|---|:----------:|
|random.randrange(0,99)| 46|0,93%|
|random.randrange(0,49)|111|2,24%|
|random.randrange(0,24)|207|4.18%|
|random.randrange(0,12)|426|8,60%|

# Crypto_deencryp_msg.py

Previous gcd_n1_n2 is a p in n1 = p * q1 and n2 = p * q2

At this point it is possible to calculate q1 as n1 // p  and q2 as n2 // p, construct a private key and uncipher the message.

To do that we recover de function used in the first approach. egdc and modinv.

1.- From common_factors.txt i read P and a list of tuples that share p as common factor


```
            p = int(factor)
            n = publickey.n
            exp = publickey.e
            q = n // p
            try:
                T = (p - 1) * (q - 1)
                d = modinv(exp, T)
            except:
                d = None
            rsa_components = (n,exp,d,p,q)

            privatekey= rsa_key= RSA.construct(rsa_components,consistency_check=True)

```



# Files

p_q_nnn_public.pem    100 fake public keys with n of 2048 bits length
2048_nnn_public.pem   100 public keys with n of 2048 bits length
2048_nnn_private.pem  100 private keys with n of 2048 bits length
2048_nnn_mesagge.enc  100 encryptions of plaintext "42Barcelona" wiht 100 different 2048_nnn_public.pem keys
nnn_public.pem        one public key with n of nnn bits length   nnn= 016..179       
nnn_private.pem       one Prvate key with n of nnn bits length   nnn= 016..179