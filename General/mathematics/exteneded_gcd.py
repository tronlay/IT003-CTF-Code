def extended_gcd(a, b):
    """
    Tính GCD và các hệ số x, y thỏa mãn phương trình: a*x + b*y = gcd(a, b)
    Trả về một tuple: (gcd, x, y)
    """
    x0, x1, y0, y1 = 1, 0, 0, 1
    
    while b != 0:
        # q là thương số, r là phần dư
        q = a // b
        a, b = b, a % b
        
        # Cập nhật lại các hệ số x và y
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
        
    return a, x0, y0

# --- Ví dụ cách sử dụng ---
if __name__ == "__main__":
 
    p=26513
    q=32321

    gcd, x, y = extended_gcd(p, q)
    print("FLAG:",min(x, y))
    