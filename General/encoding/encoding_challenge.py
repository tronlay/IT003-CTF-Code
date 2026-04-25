import socket
import json
import base64
import codecs
from Crypto.Util.number import long_to_bytes

class CryptoHackSocket:
    def __init__(self, host, port):
        """Khởi tạo và kết nối đến Server"""
        print(f"[*] Đang móc nối tới {host}:{port}...")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        
        self.f = self.s.makefile('r')
        
        # SỬA NHẸ Ở ĐÂY: Lưu lại dòng đầu tiên vào self.first_line
        # Vì với bài này, dòng đầu tiên chính là đề bài JSON của Level 1
        self.first_line = self.f.readline().strip()
        print("[+] Đã vào trong! Lấy được đề bài đầu tiên.")

    def send_payload(self, payload_dict):
        """Đóng gói JSON, gửi đi và hứng kết quả trả về"""
        data_to_send = json.dumps(payload_dict) + "\n"
        self.s.sendall(data_to_send.encode('utf-8'))
        
        response_str = self.f.readline().strip()
        if not response_str:
            print("[-] Server đã ngắt kết nối vô cớ!")
            return None
            
        return json.loads(response_str)

    def close(self):
        """Dọn dẹp chiến trường"""
        self.s.close()
        print("[*] Đã rút êm. Socket đóng!")


def decode_crypto(enc_type, enc_data):
    if enc_type == "base64":

        return base64.b64decode(enc_data).decode('utf-8')
    
    elif enc_type == "hex":

        return bytes.fromhex(enc_data).decode('utf-8')
    
    elif enc_type == "rot13":

        return codecs.decode(enc_data, 'rot_13')
    
    elif enc_type == "bigint":
        return long_to_bytes(int(enc_data, 16)).decode('utf-8')
    
    elif enc_type == "utf-8":
        return "".join(chr(b) for b in enc_data)
    
    else:
        raise ValueError(f"[-] Gặp chuẩn mã hóa lạ: {enc_type}")


# --- LUỒNG THỰC THI CHÍNH ---
if __name__ == "__main__":
    # Kết nối tới server
    conn = CryptoHackSocket('socket.cryptohack.org', 13377)
    
    # Bóc tách JSON từ dòng đầu tiên mà ta đã lưu lại
    received = json.loads(conn.first_line)
    
    # Vòng lặp chạy qua 100 levels
    for i in range(101):
        # Nếu server mệt và nhả flag thì tóm lấy ngay
        if "flag" in received:
            print("\nFLAG=", received["flag"])
            break
            
        enc_type = received["type"]
        enc_data = received["encoded"]
        
        print(f"Level: {i+1:03d} - Mã hóa: {enc_type}")
        
        # Giải mã
        decoded_word = decode_crypto(enc_type, enc_data)
        
        # Nã đạn: Gửi đáp án lên server để nhận level tiếp theo
        received = conn.send_payload({"decoded": decoded_word})
        
    conn.close()