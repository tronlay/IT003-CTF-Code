import socket
import json
from Crypto.Util.number import long_to_bytes

HOST = 'socket.cryptohack.org'
PORT = 13386

def get_data_from_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    sock_file = s.makefile('r')
    sock_file.readline() # Bỏ qua câu chào
    
    payload = {"option": "get_flag"}
    s.sendall((json.dumps(payload) + "\n").encode())
    data1 = json.loads(sock_file.readline().strip())

    s.sendall((json.dumps(payload) + "\n").encode())
    data2 = json.loads(sock_file.readline().strip())
    s.close()
    return data1, data2

data1, data2 = get_data_from_server()


print("\n" + "="*50)
print("👇 COPY TOÀN BỘ ĐOẠN DƯỚI ĐÂY ĐỂ DÁN VÀO SAGEMATH 👇")
print("="*50)

N1 = data1["modulus"]
c1 = data1['encrypted_flag']
a1 = data1['padding'][0]
b1 = data1['padding'][1]

N2 = data1["modulus"]
c2 = data2['encrypted_flag']
a2 = data2['padding'][0]
b2 = data2['padding'][1]
e = 11



def solve_franklin_reiter(c1, c2, a1, b1, a2, b2, e, N):
    # Khai báo vành đa thức modulo N
    R.<x> = PolynomialRing(Zmod(N))
    
    # Tạo 2 đa thức
    f1 = (a1*x + b1)^e - c1
    f2 = (a2*x + b2)^e - c2
    
    # Hàm tính GCD cho đa thức modulo hợp số N (Euclid algorithm)
    def poly_gcd(a, b):
        while b:
            a, b = b, a % b
        return a.monic() # Đưa hệ số bậc cao nhất về 1
        
    # Tính đa thức GCD (kết quả có dạng x - m)
    gcd_poly = poly_gcd(f1, f2)
    
    # Nghiệm m chính là trừ của hệ số tự do (bậc 0)
    m = -gcd_poly.coefficients()[0]
    
    return int(m)

m = solve_franklin_reiter(c1, c2, a1, b1, a2, b2, e, N1)
print("FLAG:",long_to_bytes(m))