from Crypto.Util.number import inverse, bytes_to_long, long_to_bytes

FLAG = b"crypto{???????????????????????????????????}"
info = {}

with open("pad_encrypt.txt", "r") as f:
    data = f.readlines()
    for line in data:
        line = line.strip()
        components = line.split('=')
        key, value = components[0].strip(), components[1].strip()
        info[key] = int(value)

n = info["n"]
e = info["e"]
c = info["c"]

m3 = (c * inverse(pow(256, 171, n), n)) % n

def check_cube(x):
    lo, hi = 0, x
    while(lo <= hi):
        mid = (lo + hi) // 2
        if (mid ** 3 == x):
            return mid
        elif (mid ** 3 < x):
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

cnt = 0
while(True):
    rt3 = check_cube(m3)
    cnt += 1
    if (cnt % 100 == 0): print(cnt)
    if (rt3 != -1):
        print(f"Found root 3: {rt3}")
        message = long_to_bytes(rt3)
        print(f"Tìm thấy Flag ở lần chạy thứ {cnt}: {message}")
        break
    m3 += n


        
