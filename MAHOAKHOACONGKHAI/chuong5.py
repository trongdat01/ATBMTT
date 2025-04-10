import os
import math

def mod_pow(base, exponent, modulus):
    """Efficient modular exponentiation function"""
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

def extended_gcd(a, b):
    """Extended Euclidean Algorithm to find gcd and coefficients"""
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def mod_inverse(a, m):
    """Modular multiplicative inverse using Extended Euclidean Algorithm"""
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def diffie_hellman(q, a, x_a, x_b):
    """Solve the Diffie-Hellman key exchange problem"""
    # Calculate public keys
    y_a = mod_pow(a, x_a, q)
    y_b = mod_pow(a, x_b, q)
    
    # Calculate shared session key
    k_a = mod_pow(y_b, x_a, q)
    k_b = mod_pow(y_a, x_b, q)
    
    return {
        'y_a': y_a,
        'y_b': y_b,
        'k': k_a  # k_a == k_b if algorithm is correct
    }

def rsa_key_generation(p, q, e):
    """Generate RSA public and private keys"""
    n = p * q
    phi_n = (p - 1) * (q - 1)
    
    # Verify e is valid
    if math.gcd(e, phi_n) != 1:
        raise ValueError("e must be coprime to φ(n)")
    
    # Calculate private key d
    d = mod_inverse(e, phi_n)
    
    return {
        'public_key': {'e': e, 'n': n},
        'private_key': {'d': d, 'n': n}
    }

def rsa_encrypt(message, public_key):
    """RSA encryption: C = M^e mod n"""
    return mod_pow(message, public_key['e'], public_key['n'])

def rsa_decrypt(ciphertext, private_key):
    """RSA decryption: M = C^d mod n"""
    return mod_pow(ciphertext, private_key['d'], private_key['n'])

def elgamal_key_generation(q, a, x_a):
    """Generate ElGamal public key"""
    y_a = mod_pow(a, x_a, q)
    return {
        'public_key': {'q': q, 'a': a, 'y_a': y_a},
        'private_key': {'x_a': x_a}
    }

def elgamal_encrypt(message, public_key, k):
    """ElGamal encryption: C1 = a^k mod q, C2 = M * y_a^k mod q"""
    q = public_key['q']
    a = public_key['a']
    y_a = public_key['y_a']
    
    c1 = mod_pow(a, k, q)
    c2 = (message * mod_pow(y_a, k, q)) % q
    
    return (c1, c2)

def elgamal_decrypt(ciphertext, private_key, q):
    """ElGamal decryption: M = C2 * (C1^x_a)^(-1) mod q"""
    c1, c2 = ciphertext
    x_a = private_key['x_a']
    
    s = mod_pow(c1, x_a, q)
    s_inv = mod_inverse(s, q)
    
    m = (c2 * s_inv) % q
    
    return m

def dsa_key_generation(p, q, h, x_a):
    """Generate DSA keys"""
    # Calculate g = h^((p-1)/q) mod p
    g = mod_pow(h, (p-1)//q, p)
    
    # Calculate public key y_a = g^x_a mod p
    y_a = mod_pow(g, x_a, p)
    
    return {
        'public_key': {'y_a': y_a, 'g': g, 'p': p, 'q': q},
        'private_key': {'x_a': x_a}
    }

def dsa_sign(h_m, private_key, public_params, k):
    """DSA signature generation"""
    x_a = private_key['x_a']
    g = public_params['g']
    p = public_params['p']
    q = public_params['q']
    
    # Calculate r = (g^k mod p) mod q
    r = mod_pow(g, k, p) % q
    
    # Calculate s = k^(-1)(H(M) + x_a * r) mod q
    k_inv = mod_inverse(k, q)
    s = (k_inv * (h_m + x_a * r)) % q
    
    return (r, s)

def dsa_verify(h_m, signature, public_key):
    """DSA signature verification"""
    r, s = signature
    y_a = public_key['y_a']
    g = public_key['g']
    p = public_key['p']
    q = public_key['q']
    
    # Calculate w = s^(-1) mod q
    w = mod_inverse(s, q)
    
    # Calculate u1 = H(M) * w mod q
    u1 = (h_m * w) % q
    
    # Calculate u2 = r * w mod q
    u2 = (r * w) % q
    
    # Calculate v = (g^u1 * y_a^u2 mod p) mod q
    v = (mod_pow(g, u1, p) * mod_pow(y_a, u2, p)) % p % q
    
    # Verify if v == r
    return v == r

def get_file_path(filename):
    """Return full path for a file in the MAHOAKHOACONGKHAI directory"""
    base_dir = "d:/Download/CODE/MAHOAKHOACONGKHAI/"
    return os.path.join(base_dir, filename)

def create_template_input_file():
    """Create a template input file if it doesn't exist"""
    filename = get_file_path("input.txt")
    template_content = """# Diffie-Hellman parameters
7523 5 387 247
# RSA parameters (p, q, e, M)
47 71 61 59
# ElGamal parameters (q, a, xA, k, M)
7433 3 341 872 403
# DSA parameters (p, q, h, xA, k, H(M))
47 23 34 2 10 8"""
    
    try:
        # Ensure directory exists
        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(template_content)
        print(f"Created template file {filename} with content:")
        print(template_content)
        return True
    except Exception as e:
        print(f"Error creating template file: {e}")
        return False

def read_parameters():
    """Read parameters from input file"""
    filename = get_file_path("input.txt")
    try:
        if not os.path.exists(filename):
            print(f"Input file {filename} not found. Creating template...")
            create_template_input_file()
            print("Please modify the input file with your values and run the program again.")
            return None
            
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
        params = {}
        
        # Parse Diffie-Hellman parameters
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            if 'diffie_hellman' not in params:
                q, a, x_a, x_b = map(int, line.split())
                params['diffie_hellman'] = {'q': q, 'a': a, 'x_a': x_a, 'x_b': x_b}
            elif 'rsa' not in params:
                p, q, e, m = map(int, line.split())
                params['rsa'] = {'p': p, 'q': q, 'e': e, 'm': m}
            elif 'elgamal' not in params:
                q, a, x_a, k, m = map(int, line.split())
                params['elgamal'] = {'q': q, 'a': a, 'x_a': x_a, 'k': k, 'm': m}
            elif 'dsa' not in params:
                p, q, h, x_a, k, h_m = map(int, line.split())
                params['dsa'] = {'p': p, 'q': q, 'h': h, 'x_a': x_a, 'k': k, 'h_m': h_m}
        
        return params
    except Exception as e:
        print(f"Error reading input file: {e}")
        return None

def write_results(results):
    """Write results to output file"""
    filename = get_file_path("output.txt")
    try:
        # Ensure directory exists
        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(results)
        print(f"Results written to {filename}")
    except Exception as e:
        print(f"Error writing to output file: {e}")

def main():
    # Read parameters
    params = read_parameters()
    if not params:
        return
    
    # Initialize output text
    output = "NHÓM 1\nMÃ HÓA KHÓA CÔNG KHAI\n\n"
    
    # 1. Diffie-Hellman key exchange
    dh_params = params['diffie_hellman']
    dh_result = diffie_hellman(dh_params['q'], dh_params['a'], dh_params['x_a'], dh_params['x_b'])
    
    output += "1. Trao đổi khóa Diffie-Hellman\n"
    output += f"q = {dh_params['q']}, a = {dh_params['a']}\n"
    output += f"An chọn khóa riêng xA = {dh_params['x_a']}\n"
    output += f"Ba chọn khóa riêng xB = {dh_params['x_b']}\n\n"
    
    output += "a) Cách An tính ra khóa công khai yA và khóa phiên K:\n"
    output += f"   yA = a^xA mod q = {dh_params['a']}^{dh_params['x_a']} mod {dh_params['q']} = {dh_result['y_a']}\n"
    output += f"   K = yB^xA mod q = {dh_result['y_b']}^{dh_params['x_a']} mod {dh_params['q']} = {dh_result['k']}\n\n"
    
    output += "b) Cách Ba tính ra khóa công khai yB và khóa phiên K:\n"
    output += f"   yB = a^xB mod q = {dh_params['a']}^{dh_params['x_b']} mod {dh_params['q']} = {dh_result['y_b']}\n"
    output += f"   K = yA^xB mod q = {dh_result['y_a']}^{dh_params['x_b']} mod {dh_params['q']} = {dh_result['k']}\n\n"
    
    # 2. RSA algorithm - Problem 1
    rsa_params = params['rsa']
    rsa_keys = rsa_key_generation(rsa_params['p'], rsa_params['q'], rsa_params['e'])
    ciphertext = rsa_encrypt(rsa_params['m'], rsa_keys['public_key'])
    decrypted = rsa_decrypt(ciphertext, rsa_keys['private_key'])
    
    output += "2. Thuật toán RSA - Bài toán 1\n"
    output += f"p = {rsa_params['p']}, q = {rsa_params['q']}, e = {rsa_params['e']}\n\n"
    
    output += "a) Khóa công khai của An:\n"
    output += f"   PU = {{e, n}} = {{{rsa_keys['public_key']['e']}, {rsa_keys['public_key']['n']}}}\n\n"
    
    output += "b) Cách An tạo ra khóa riêng:\n"
    output += f"   Tính φ(n) = (p-1)(q-1) = ({rsa_params['p']}-1)({rsa_params['q']}-1) = {(rsa_params['p']-1)*(rsa_params['q']-1)}\n"
    output += f"   Tìm d sao cho e*d ≡ 1 (mod φ(n)): {rsa_params['e']}*d ≡ 1 (mod {(rsa_params['p']-1)*(rsa_params['q']-1)})\n"
    output += f"   d = {rsa_keys['private_key']['d']}\n"
    output += f"   PR = {{d, n}} = {{{rsa_keys['private_key']['d']}, {rsa_keys['private_key']['n']}}}\n\n"
    
    output += "c) Cách An tạo bản mã hóa thông điệp M = 59:\n"
    output += f"   C = M^e mod n = {rsa_params['m']}^{rsa_keys['public_key']['e']} mod {rsa_keys['public_key']['n']} = {ciphertext}\n\n"
    
    output += "d) Cách người nhận giải mã bản mã C:\n"
    output += f"   M = C^d mod n = {ciphertext}^{rsa_keys['private_key']['d']} mod {rsa_keys['private_key']['n']} = {decrypted}\n\n"
    
    output += "e) Việc mã hóa ở câu c) thực hiện nhiệm vụ chữ ký số.\n"
    output += "   Khi người gửi (An) dùng khóa riêng để mã hóa, đây là quá trình tạo chữ ký số.\n\n"
    
    # 3. RSA algorithm - Problem 2
    output += "3. Thuật toán RSA - Bài toán 2:\n"
    output += f"p = {rsa_params['p']}, q = {rsa_params['q']}, e = {rsa_params['e']}\n\n"
    
    output += "a) Khóa công khai của An:\n"
    output += f"   PU = {{e, n}} = {{{rsa_keys['public_key']['e']}, {rsa_keys['public_key']['n']}}}\n\n"
    
    output += "b) Cách An tạo ra khóa riêng:\n"
    output += f"   Tính φ(n) = (p-1)(q-1) = ({rsa_params['p']}-1)({rsa_params['q']}-1) = {(rsa_params['p']-1)*(rsa_params['q']-1)}\n"
    output += f"   Tìm d sao cho e*d ≡ 1 (mod φ(n)): {rsa_params['e']}*d ≡ 1 (mod {(rsa_params['p']-1)*(rsa_params['q']-1)})\n"
    output += f"   d = {rsa_keys['private_key']['d']}\n"
    output += f"   PR = {{d, n}} = {{{rsa_keys['private_key']['d']}, {rsa_keys['private_key']['n']}}}\n\n"
    
    output += "c) Cách người gửi (Ba) mã hóa thông điệp M = 59 để gửi cho An:\n"
    output += f"   C = M^e mod n = {rsa_params['m']}^{rsa_keys['public_key']['e']} mod {rsa_keys['public_key']['n']} = {ciphertext}\n\n"
    
    output += "d) Cách An giải mã bản mã C:\n"
    output += f"   M = C^d mod n = {ciphertext}^{rsa_keys['private_key']['d']} mod {rsa_keys['private_key']['n']} = {decrypted}\n\n"
    
    output += "e) Việc mã hóa ở câu c) thực hiện nhiệm vụ bảo mật.\n"
    output += "   Khi người gửi dùng khóa công khai của người nhận để mã hóa, đây là quá trình bảo mật thông điệp.\n\n"
    
    # 4. ElGamal encryption
    eg_params = params['elgamal']
    eg_keys = elgamal_key_generation(eg_params['q'], eg_params['a'], eg_params['x_a'])
    eg_cipher = elgamal_encrypt(eg_params['m'], eg_keys['public_key'], eg_params['k'])
    eg_decrypted = elgamal_decrypt(eg_cipher, eg_keys['private_key'], eg_params['q'])
    
    output += "4. Mật mã ElGamal\n"
    output += f"q = {eg_params['q']}, a = {eg_params['a']}, xA = {eg_params['x_a']}\n\n"
    
    output += "a) Khóa công khai của An:\n"
    output += f"   yA = a^xA mod q = {eg_params['a']}^{eg_params['x_a']} mod {eg_params['q']} = {eg_keys['public_key']['y_a']}\n"
    output += f"   PU = {{q, a, yA}} = {{{eg_keys['public_key']['q']}, {eg_keys['public_key']['a']}, {eg_keys['public_key']['y_a']}}}\n\n"
    
    output += "b) Ba chọn số k = 872 để mã hóa bản tin M = 403 gửi cho An. Bản mã là:\n"
    output += f"   C1 = a^k mod q = {eg_params['a']}^{eg_params['k']} mod {eg_params['q']} = {eg_cipher[0]}\n"
    output += f"   C2 = M * yA^k mod q = {eg_params['m']} * {eg_keys['public_key']['y_a']}^{eg_params['k']} mod {eg_params['q']} = {eg_cipher[1]}\n"
    output += f"   (C1, C2) = ({eg_cipher[0]}, {eg_cipher[1]})\n\n"
    
    output += "c) Cách An giải bản mã (C1, C2):\n"
    output += f"   Tính s = C1^xA mod q = {eg_cipher[0]}^{eg_params['x_a']} mod {eg_params['q']} = {mod_pow(eg_cipher[0], eg_params['x_a'], eg_params['q'])}\n"
    output += f"   Tính s^(-1) mod q = {mod_inverse(mod_pow(eg_cipher[0], eg_params['x_a'], eg_params['q']), eg_params['q'])}\n"
    output += f"   M = C2 * s^(-1) mod q = {eg_cipher[1]} * {mod_inverse(mod_pow(eg_cipher[0], eg_params['x_a'], eg_params['q']), eg_params['q'])} mod {eg_params['q']} = {eg_decrypted}\n\n"
    
    # 5. DSA signature
    dsa_params = params['dsa']
    g = mod_pow(dsa_params['h'], (dsa_params['p']-1)//dsa_params['q'], dsa_params['p'])
    dsa_keys = dsa_key_generation(dsa_params['p'], dsa_params['q'], dsa_params['h'], dsa_params['x_a'])
    public_params = {'g': g, 'p': dsa_params['p'], 'q': dsa_params['q']}
    signature = dsa_sign(dsa_params['h_m'], dsa_keys['private_key'], public_params, dsa_params['k'])
    verification = dsa_verify(dsa_params['h_m'], signature, dsa_keys['public_key'])
    
    output += "5. CHỮ KÝ ĐIỆN TỬ DSA\n"
    output += f"p = {dsa_params['p']}, q = {dsa_params['q']}, h = {dsa_params['h']}, xA = {dsa_params['x_a']}, k = {dsa_params['k']}, H(M) = {dsa_params['h_m']}\n\n"
    
    output += "a) Khóa công khai của An:\n"
    output += f"   g = h^((p-1)/q) mod p = {dsa_params['h']}^(({dsa_params['p']}-1)/{dsa_params['q']}) mod {dsa_params['p']} = {g}\n"
    output += f"   yA = g^xA mod p = {g}^{dsa_params['x_a']} mod {dsa_params['p']} = {dsa_keys['public_key']['y_a']}\n\n"
    
    output += "b) Chữ ký số của An cho bản tin M:\n"
    output += f"   r = (g^k mod p) mod q = ({g}^{dsa_params['k']} mod {dsa_params['p']}) mod {dsa_params['q']} = {signature[0]}\n"
    output += f"   s = k^(-1)(H(M) + xA * r) mod q = {mod_inverse(dsa_params['k'], dsa_params['q'])}*({dsa_params['h_m']} + {dsa_params['x_a']}*{signature[0]}) mod {dsa_params['q']} = {signature[1]}\n"
    output += f"   (r, s) = ({signature[0]}, {signature[1]})\n\n"
    
    output += "c) Cách Ba xác minh chữ ký số được đính kèm với bản tin M:\n"
    output += f"   w = s^(-1) mod q = {signature[1]}^(-1) mod {dsa_params['q']} = {mod_inverse(signature[1], dsa_params['q'])}\n"
    w = mod_inverse(signature[1], dsa_params['q'])
    u1 = (dsa_params['h_m'] * w) % dsa_params['q']
    u2 = (signature[0] * w) % dsa_params['q']
    output += f"   u1 = H(M) * w mod q = {dsa_params['h_m']} * {w} mod {dsa_params['q']} = {u1}\n"
    output += f"   u2 = r * w mod q = {signature[0]} * {w} mod {dsa_params['q']} = {u2}\n"
    v = (mod_pow(g, u1, dsa_params['p']) * mod_pow(dsa_keys['public_key']['y_a'], u2, dsa_params['p'])) % dsa_params['p'] % dsa_params['q']
    output += f"   v = (g^u1 * yA^u2 mod p) mod q = ({g}^{u1} * {dsa_keys['public_key']['y_a']}^{u2} mod {dsa_params['p']}) mod {dsa_params['q']} = {v}\n"
    output += f"   Kiểm tra: v = {v}, r = {signature[0]}\n"
    output += f"   {'Chữ ký đúng' if verification else 'Chữ ký sai'}: v == r\n"
    
    # Write results to file
    write_results(output)
    
    print("Computation complete!")

if __name__ == "__main__":
    main()
