import re
from Crypto.Hash import SHA256
from Crypto.Util.number import bytes_to_long, long_to_bytes
from pkcs1 import emsa_pkcs1_v15
import socket
import json
from Crypto.Util.number import long_to_bytes
class CryptoHackSocket:
    def __init__(self, host, port):
        """Khởi tạo và kết nối đến Server"""
        print(f"[*] Đang móc nối tới {host}:{port}...")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        
        # Dùng makefile để đọc dữ liệu theo từng dòng (cực kỳ hiệu quả với CryptoHack)
        self.f = self.s.makefile('r')
        
        # Hút cạn câu chào mừng mặc định của CryptoHack để làm sạch bộ đệm
        welcome_msg = self.f.readline().strip()
        print(f"[+] Đã vào trong! Server chào: {welcome_msg}")

    def send_payload(self, payload_dict):
        """
        Hàm nã đạn: Nhận vào một Dictionary, tự biến thành JSON và gửi đi.
        Sau đó tự động chờ và bóc tách JSON trả về từ Server.
        """
        # 1. Đóng gói Payload thành JSON và thêm \n (bắt buộc với CryptoHack)
        data_to_send = json.dumps(payload_dict) + "\n"
        self.s.sendall(data_to_send.encode('utf-8'))
        
        # 2. Hứng dữ liệu trả về
        response_str = self.f.readline().strip()
        # Nếu server ngắt kết nối đột ngột
        if not response_str:
            print("[-] Server đã ngắt kết nối vô cớ!")
            return None
            
        # 3. Dịch ngược JSON thành Dictionary cho bạn dễ thao tác
        return json.loads(response_str)

    def close(self):
        """Dọn dẹp chiến trường"""
        self.s.close()
        print("[*] Đã rút êm. Socket đóng!")

def H(msg):
    return emsa_pkcs1_v15.encode(msg.encode(), 256)
    
if __name__ == "__main__":
    HOST = 'socket.cryptohack.org'
    PORT = 13391

    conn = CryptoHackSocket(HOST, PORT)

    # Get signature and key
    payload = {
        'option': 'get_signature'
    }
    result = conn.send_payload(payload)
    N = int(result["N"], 16)
    e = int(result["e"], 16)
    signature = int(result["signature"], 16)

    msg = "I am Mallory. I own CryptoHack.org"

    # H(msg) = Signature (mod k)
    # H(msg) = H(msg) + x (mod k)
    # k = Signature - H(msg)

    mod = signature - bytes_to_long(H(msg))
    e = 1

    payload = {
        'option': 'verify',
        'msg': msg,
        'N': hex(mod),
        'e': hex(e),
    }

    result = conn.send_payload(payload)
    print(result)

    conn.close()

