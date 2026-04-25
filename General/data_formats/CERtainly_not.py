from cryptography import x509
from cryptography.hazmat.backends import default_backend

file_path = "2048b-rsa-example-cert.der" # Path to DER File

with open(file_path, "rb") as f:
    der_data = f.read()

# 2. Phân tích X.509 từ dữ liệu DER
cert = x509.load_der_x509_certificate(der_data, default_backend())

public_key = cert.public_key()

rsa_numbers = public_key.public_numbers()
modulus = rsa_numbers.n

print("Flag=",modulus)