from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import *
from hashlib import sha1
import random
import os
from sympy.ntheory import discrete_log
from collections import namedtuple
from sympy import factorint
# Create a simple Point class to represent the affine points.
Point = namedtuple("Point", "x y")

def point_addition(P, Q):
    Rx = (P.x*Q.x + D*P.y*Q.y) % p
    Ry = (P.x*Q.y + P.y*Q.x) % p
    return Point(Rx, Ry)


def scalar_multiplication(P, n): 
    Q = Point(1, 0)
    while n > 0:
        if n % 2 == 1:
            Q = point_addition(Q, P)
        P = point_addition(P, P)
        n = n//2
    return Q


def gen_keypair():
    private = random.randint(1, p-1)
    public = scalar_multiplication(G, private)
    return (public, private)


def gen_shared_secret(P, d):
    return scalar_multiplication(P, d).x

def encrypt_flag(shared_secret: int, flag: bytes):
    # Derive AES key from shared secret
    key = sha1(str(shared_secret).encode('ascii')).digest()[:16]
    # Encrypt flag
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(flag, 16))
    # Prepare data to send
    data = {}
    data['iv'] = iv.hex()
    data['encrypted_flag'] = ciphertext.hex()
    return data

def decrypt_flag(shared_secret: int, iv: int, ct: int):
    key = sha1(str(shared_secret).encode('ascii')).digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    message = unpad(cipher.decrypt(ct), 16)
    
    return message

#Parameters
p = 173754216895752892448109692432341061254596347285717132408796456167143559

#Check if p là số nguyên tố trơn
print(factorint(p - 1))

D = 529
G = Point(29394812077144852405795385333766317269085018265469771684226884125940148,
          94108086667844986046802106544375316173742538919949485639896613738390948)

A = Point(x=155781055760279718382374741001148850818103179141959728567110540865590463, 
          y=73794785561346677848810778233901832813072697504335306937799336126503714)
B = Point(x=171226959585314864221294077932510094779925634276949970785138593200069419,
          y=54353971839516652938533335476115503436865545966356461292708042305317630)

iv = bytes.fromhex('64bc75c8b38017e1397c46f85d4e332b')
ct = bytes.fromhex('13e4d200708b786d8f7c3bd2dc5de0201f0d7879192e6603d7c5d6b963e1df2943e3ff75f7fda9c30a92171bbbc5acbf')

g = G.x + 23 * G.y

a = A.x + 23 * A.y

n_a = discrete_log(p, a, g)

shared_secret = gen_shared_secret(B, n_a)

print("\nFLAG: decrypt_flag(shared_secret, iv, ct)")