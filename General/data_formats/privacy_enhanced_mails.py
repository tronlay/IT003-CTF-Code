from Crypto.PublicKey import RSA

with open('privacy_enhanced_mail.pem', 'r') as f:
    data = f.readlines()
    key = "".join(data)

    public_value = RSA.importKey(key)
    print("FLAG:",public_value.d)