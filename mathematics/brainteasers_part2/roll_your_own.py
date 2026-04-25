import json
import socket

class CryptoHackSocket:
    def __init__(self, host, port):
        """Khởi tạo và kết nối đến Server"""
        print(f"\n*Kết nối tới server ở {host}:{port}...\n")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        
        # Dùng makefile để đọc dữ liệu theo từng dòng (cực kỳ hiệu quả với CryptoHack)
        self.f = self.s.makefile('r')
        
        # Hút cạn câu chào mừng mặc định của CryptoHack để làm sạch bộ đệm
        self.q = self.f.readline().strip()

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
            print("Disconnected")
            return None
            
        # 3. Dịch ngược JSON thành Dictionary cho bạn dễ thao tác
        return response_str

    def close(self):
        """Dọn dẹp chiến trường"""
        self.s.close()
        print("\n*Close connection\n")

host = 'socket.cryptohack.org'
port = 13403

conn = CryptoHackSocket(host, port)

# Lấy số q được đề bài cho
q = int(conn.q.split('"')[1], 16)

# Xây dựng payload
g = q + 1
n = q ** 2
payload = {"n": hex(n), "g": hex(g)}

#Lấy số h = g^x từ server.
h = int(conn.send_payload(payload).split('"')[1], 16)

#Get the hidden x
x = (h - 1) // q
payload = {"x": hex(x)}
flag = conn.send_payload(payload)

print(flag)
conn.close()



