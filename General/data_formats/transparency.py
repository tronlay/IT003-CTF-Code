from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import hashlib
import requests

# 1. Đọc nội dung file PEM (Hãy đổi tên file cho khớp với file đề bài cấp)
file_path = "transparency.pem"

with open(file_path, "rb") as f:
    pem_data = f.read()

# Load khóa công khai
public_key = serialization.load_pem_public_key(pem_data, default_backend())

print(public_key)
# 2. Trích xuất dữ liệu SPKI (Subject Public Key Info) dạng nhị phân (DER)
spki_der = public_key.public_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# 3. Tính mã băm SHA-256 của SPKI
spki_sha256 = hashlib.sha256(spki_der).hexdigest()
print(f"[*] Dấu vân tay SPKI SHA-256: {spki_sha256}")

## Sau đó, tìm mã spki_sha256 này ở crt.sh, ta sẽ thấy 2 id, click 
## bất kì vào trường id của một hàng, và lướt xuống ta sẽ thấy đường dẫn 
## đến trang có flag.