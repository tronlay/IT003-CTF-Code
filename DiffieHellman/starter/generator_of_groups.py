def get_prime_factors(n):
    """Hàm phụ trợ: Phân tích một số ra các thừa số nguyên tố"""
    factors = set()
    # Tách các thừa số 2
    while n % 2 == 0:
        factors.add(2)
        n //= 2
        
    # Tách các thừa số lẻ
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.add(i)
            n //= i
        i += 2
        
    # Nếu phần còn lại là số nguyên tố lớn hơn 2
    if n > 2:
        factors.add(n)
    return factors

def find_primitive_root(p):
    """Hàm chính: Tìm căn nguyên thủy nhỏ nhất modulo p"""
    if p == 2:
        return 1
        
    phi = p - 1
    factors = get_prime_factors(phi)
    
    # Thử các ứng cử viên g từ 2 đến p-1
    for g in range(2, p):
        is_primitive = True
        
        # Kiểm tra điều kiện g^((p-1)/q) != 1 (mod p)
        for q in factors:
            if pow(g, phi // q, p) == 1:
                is_primitive = False
                break # Gãy, thử số g tiếp theo
                
        if is_primitive:
            return g # Trả về ngay số g nhỏ nhất thỏa mãn
            
    return None

p = 28151
g = find_primitive_root(p)
print(f"Căn nguyên thủy của {p} là: {g}")