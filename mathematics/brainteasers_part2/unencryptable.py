from Crypto.Util.number import bytes_to_long, inverse, long_to_bytes
import math
info = {}

with open("unencryptable.txt", "r") as f:
    for line in f:
        sp = line.split('=')
        if (len(sp) > 1):
            key, value = sp[0].strip(), sp[1].strip()
            info[key] = value


N = int(info["N"], 16)
e = int(info["e"], 16)
c = int(info["c"], 16)

DATA = bytes.fromhex("372f0e88f6f7189da7c06ed49e87e0664b988ecbee583586dfd1c6af99bf20345ae7442012c6807b3493d8936f5b48e553f614754deb3da6230fa1e16a8d5953a94c886699fc2bf409556264d5dced76a1780a90fd22f3701fdbcb183ddab4046affdc4dc6379090f79f4cd50673b24d0b08458cdbe509d60a4ad88a7b4e2921")
FLAG = b'crypto{??????????????????????????????????????}'

data = bytes_to_long(DATA)

pw = e - 1
x = data

print(math.gcd(x - 1, N))

while(pw > 1):
    x = (x * x) % N
    if (x != 1 and x != N - 1):
        try:
            p = math.gcd(x - 1, N)

            if (p > 1):
                q = N // p
                phi = (p - 1) * (q - 1)
                d = inverse(e, phi)
                flag = pow(c, d, N)
                fl = long_to_bytes(flag).decode('utf-8')

                print(fl)
                break
        except Exception as e:
            pass


