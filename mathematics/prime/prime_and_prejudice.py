import socket
import json
from sympy import isprime

def exploit():
    print("Tạo số Giả nguyên tố (Adversarial Strong Pseudoprime)...")
    
    # Tập hợp các cơ số từ 5 đến 61
    primes_basis = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]
    
    P = 1
    for p in primes_basis:
        P *= p

    # Thiết lập hệ phương trình CRT để đánh lừa thuật toán
    # m = 0 mod P, m = 3 mod 9, m = 1 mod 2
    k_9 = (3 * pow(P, -1, 9)) % 9
    m_partial = P * k_9
    
    if m_partial % 2 == 0:
        m0 = m_partial + P * 9
    else:
        m0 = m_partial
        
    M_crt = P * 9 * 2

    # Đẩy m lên kích thước khổng lồ để n > 2^600
    k = 2**130  
    
    while True:
        m = m0 + k * M_crt
        p1 = 2*m + 1
        p2 = 10*m + 1
        
        # Tối ưu: Dùng Fermat test cơ bản trước để lọc
        if pow(2, p1-1, p1) == 1 and pow(2, p2-1, p2) == 1:
            p3 = 18*m + 1
            if pow(2, p3-1, p3) == 1:
                # Vượt qua màng lọc, chốt hạ bằng thuật toán chuẩn
                if isprime(p1) and isprime(p2) and isprime(p3):
                    break
        k += 1

    n = p1 * p2 * p3
    a = p3 # Lợi dụng lỗ hổng không check GCD
    

    print(pow(a, n - 1, n))

    HOST = 'socket.cryptohack.org'
    PORT = 13385
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    sock_file = s.makefile('r')
    
    # Bỏ qua câu chào
    sock_file.readline()
    
    payload = {"prime": n, "base": a}
    s.sendall((json.dumps(payload) + "\n").encode('utf-8'))
    
    response = sock_file.readline().strip()
    print(f"FLAG:\n{response}")
    s.close()

if __name__ == "__main__":
    exploit()