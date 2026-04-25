import socket
import json
import random
import math
import sympy
from sympy.ntheory import factorint

N = 56135841374488684373258694423292882709478511628224823806418810596720294684253418942704418179091997825551647866062286502441190115027708222460662070779175994701788428003909010382045613207284532791741873673703066633119446610400693458529100429608337219231960657953091738271259191554117313396642763210860060639141073846574854063639566514714132858435468712515314075072939175199679898398182825994936320483610198366472677612791756619011108922142762239138617449089169337289850195216113264566855267751924532728815955224322883877527042705441652709430700299472818705784229370198468215837020914928178388248878021890768324401897370624585349884198333555859109919450686780542004499282760223378846810870449633398616669951505955844529109916358388422428604135236531474213891506793466625402941248015834590154103947822771207939622459156386080305634677080506350249632630514863938445888806223951124355094468682539815309458151531117637927820629042605402188751144912274644498695897277
phi = 56135841374488684373258694423292882709478511628224823806413974550086974518248002462797814062141189227167574137989180030483816863197632033192968896065500768938801786598807509315219962138010136188406833851300860971268861927441791178122071599752664078796430411769850033154303492519678490546174370674967628006608839214466433919286766123091889446305984360469651656535210598491300297553925477655348454404698555949086705347702081589881912691966015661120478477658546912972227759596328813124229023736041312940514530600515818452405627696302497023443025538858283667214796256764291946208723335591637425256171690058543567732003198060253836008672492455078544449442472712365127628629283773126365094146350156810594082935996208856669620333251443999075757034938614748482073575647862178964169142739719302502938881912008485968506720505975584527371889195388169228947911184166286132699532715673539451471005969465570624431658644322366653686517908000327238974943675848531974674382848
g = 986762276114520220801525811758560961667498483061127810099097

def factor_N_with_phi(n, phi_n):
    t = phi_n
    s = 0
    while t % 2 == 0:
        t //= 2
        s += 1
        
    def factorize(num):
        if sympy.isprime(num): return [num]
        while True:
            a = random.randint(2, num - 1)
            x = pow(a, t, num)
            if x == 1 or x == num - 1: continue
            for _ in range(s - 1):
                y = pow(x, 2, num)
                if y == 1:
                    p = math.gcd(x - 1, num)
                    return factorize(p) + factorize(num // p)
                if y == num - 1: break
                x = y
    return factorize(n)

primes = factorint(N)
print(f"N được tạo từ {len(primes)} số nguyên tố")

# dấu Legendre của g trên từng prime
legs_g = [sympy.jacobi_symbol(g, p) for p in primes]

def is_in_subgroup(c):
    '''
    Kiem tra so c co nam trong subgroup khong
    '''
    legs_c = [sympy.jacobi_symbol(c, p) for p in primes]
    
    non_residue_indices = []
    for i in range(len(primes)):
        if legs_g[i] == 1:
            # Luật 1: Nếu g là thặng dư, c bắt buộc phải là thặng dư
            if legs_c[i] == -1: return False 
        else:
            non_residue_indices.append(i)
            
    # Luật 2: Trên các prime mà g không phải thặng dư, dấu của c phải đồng điệu 100%
    if len(non_residue_indices) > 1:
        first_idx = non_residue_indices[0]
        first_val = legs_c[first_idx]
        for idx in non_residue_indices[1:]:
            if legs_c[idx] != first_val: return False
            
    return True

# Kết nối tới server
HOST = 'socket.cryptohack.org' 
PORT = 13398

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
sock_file = s.makefile('r')
sock_file.readline()

def query_bit(i):
    payload = {"option": "get_bit", "i": i}
    s.sendall((json.dumps(payload) + "\n").encode())
    resp = sock_file.readline().strip()
    data = json.loads(resp)
    if "error" in data: return None
    return int(data["bit"], 16)

flag = ""
bit_idx = 0
num_tests = 1

while True:
    char_val = 0
    for b in range(8):
        is_bit_one = True
        for _ in range(num_tests):
            c = query_bit(bit_idx)
            if c is None: break

            if not is_in_subgroup(c):
                is_bit_one = False
                break
                
        if is_bit_one:
            char_val |= (1 << b) 
            
        bit_idx += 1
    
    if c is None: break
        
    flag += chr(char_val)
    print(f"\rFLAG= {flag}", end="", flush=True)

s.close()