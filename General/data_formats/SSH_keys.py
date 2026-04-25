from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Đường dẫn tới file pubkey
file_path = "bruce_rsa.pub"

with open(file_path, 'r') as f:
    ssh_pub_key_data = f.readline().encode('utf-8')

# Đọc và phân tích cấu trúc SSH
public_key = serialization.load_ssh_public_key(ssh_pub_key_data, default_backend())

# Lấy modulo từ RSA
rsa_numbers = public_key.public_numbers()
print(f"FLAG: {rsa_numbers.n}")