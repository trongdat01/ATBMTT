import numpy as np
import os

def caesar(text, shift):
    cipher_text = ""
    for c in text.upper():
        cipher_text += chr(((ord(c) - ord('A') + shift) % 26) + ord('A'))
    return cipher_text

def caesar_decrypt(text, shift):
    return caesar(text, -shift)

def repeat_key(text, key):
    return (key * (len(text) // len(key))) + key[:len(text) % len(key)]

def auto_key(text, key):
    return key + text[:len(text) - len(key)]

def vigenere_encrypt(text, key, is_auto_key=False):
    extended_key = auto_key(text, key) if is_auto_key else repeat_key(text, key)
    cipher_text = ""
    for i in range(len(text)):
        cipher_text += chr(((ord(text[i]) - ord('A') + ord(extended_key[i]) - ord('A')) % 26) + ord('A'))
    return cipher_text

def vigenere_decrypt(text, key, is_auto_key=False):
    if is_auto_key:
        plain_text = ""
        for i in range(len(text)):
            if i < len(key):
                shift = ord(key[i]) - ord('A')
            else:
                shift = ord(plain_text[i - len(key)]) - ord('A')
            plain_char = chr(((ord(text[i]) - ord('A') - shift) % 26) + ord('A'))
            plain_text += plain_char
        return plain_text
    else:
        extended_key = repeat_key(text, key)
        plain_text = ""
        for i in range(len(text)):
            plain_text += chr(((ord(text[i]) - ord('A') - (ord(extended_key[i]) - ord('A'))) % 26) + ord('A'))
        return plain_text

def generate_substitution_map(key):
    return {chr(ord('A') + i): key[i] for i in range(26)}

def monoalphabetic_encrypt(text, key):
    sub_map = generate_substitution_map(key)
    return "".join(sub_map[c] for c in text.upper())

def monoalphabetic_decrypt(text, key):
    sub_map = generate_substitution_map(key)
    reverse_map = {v: k for k, v in sub_map.items()}
    return "".join(reverse_map[c] for c in text.upper())

def prepare_key(key):
    key = key.upper().replace("J", "I")
    new_key = "".join(sorted(set(key), key=key.index))
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    return new_key + "".join(c for c in alphabet if c not in new_key)

def create_playfair_matrix(key):
    processed_key = prepare_key(key)
    matrix = np.array(list(processed_key)).reshape(5, 5)
    letter_pos = {matrix[i, j]: (i, j) for i in range(5) for j in range(5)}
    return matrix, letter_pos

def prepare_text(text):
    text = text.upper().replace("J", "I")
    pairs = []
    i = 0
    while i < len(text):
        first = text[i]
        second = text[i + 1] if i + 1 < len(text) else 'X'
        if first == second:
            second = 'X'
            i += 1
        else:
            i += 2
        pairs.append((first, second))
    return pairs

def playfair_encrypt(text, key):
    matrix, letter_pos = create_playfair_matrix(key)
    pairs = prepare_text(text)
    cipher_text = ""
    for a, b in pairs:
        r1, c1 = letter_pos[a]
        r2, c2 = letter_pos[b]
        if r1 == r2:
            cipher_text += matrix[r1, (c1 + 1) % 5] + matrix[r2, (c2 + 1) % 5]
        elif c1 == c2:
            cipher_text += matrix[(r1 + 1) % 5, c1] + matrix[(r2 + 1) % 5, c2]
        else:
            cipher_text += matrix[r1, c2] + matrix[r2, c1]
    return cipher_text

def playfair_decrypt(text, key):
    matrix, letter_pos = create_playfair_matrix(key)
    pairs = [(text[i], text[i+1]) for i in range(0, len(text), 2)]
    plain_text = ""
    for a, b in pairs:
        r1, c1 = letter_pos[a]
        r2, c2 = letter_pos[b]
        if r1 == r2:
            plain_text += matrix[r1, (c1 - 1) % 5] + matrix[r2, (c2 - 1) % 5]
        elif c1 == c2:
            plain_text += matrix[(r1 - 1) % 5, c1] + matrix[(r2 - 1) % 5, c2]
        else:
            plain_text += matrix[r1, c2] + matrix[r2, c1]
    return plain_text

def rail_fence_cipher(message, key):
    """Mã hóa Rail Fence sử dụng phương pháp modulo như trong C++"""
    if key <= 1:
        return message
    
    # Loại bỏ khoảng trắng nếu cần
    processed_text = ''.join(c for c in message if c != ' ')
    
    # Tạo rails
    fence = ["" for _ in range(key)]
    
    # Phân phối ký tự vào các rail bằng phương pháp modulo
    for i in range(len(processed_text)):
        rail = i % key
        fence[rail] += processed_text[i]
    
    # Nối các rail để tạo bản mã
    result = ''.join(fence)
    
    return result

def rail_fence_decrypt(cipher, key):
    """Giải mã Rail Fence sử dụng phương pháp modulo như trong C++"""
    if key <= 1 or not cipher:
        return cipher
    
    text_length = len(cipher)
    
    # Tính độ dài của mỗi rail
    rail_lengths = [0] * key
    for i in range(text_length):
        rail_lengths[i % key] += 1
    
    # Chia bản mã thành các rail
    fence = []
    current_pos = 0
    for i in range(key):
        fence.append(cipher[current_pos:current_pos + rail_lengths[i]])
        current_pos += rail_lengths[i]
    
    # Tái tạo văn bản gốc từ các rail
    result = ""
    indices = [0] * key
    
    for i in range(text_length):
        rail = i % key
        result += fence[rail][indices[rail]]
        indices[rail] += 1
    
    return result

def get_method_name(mode):
    """Return the name of the encryption method based on mode number"""
    method_names = {
        1: "Caesar",
        2: "Vigenere",
        3: "AutoVigenere",
        4: "Monoalphabetic",
        5: "Playfair",
        6: "RailFence"
    }
    return method_names.get(mode, "Unknown")

def get_file_path(filename):
    """Return full path for a file in the MAHOACODIEN directory"""
    base_dir = "d:/Download/CODE/MAHOACODIEN/"
    return os.path.join(base_dir, filename)

def create_template_input_file(method_name):
    """Create a template input file for the given encryption method"""
    filename = get_file_path(f"input{method_name}.txt")
    templates = {
        "Caesar": "HELLOWORLD\n3",
        "Vigenere": "ATTACKATDAWN\nKEY",
        "AutoVigenere": "ATTACKATDAWN\nKEY",
        "Monoalphabetic": "HELLOWORLD\nZYXWVUTSRQPONMLKJIHGFEDCBA",
        "Playfair": "HELLOWORLD\nMONARCHY",
        "RailFence": "HELLOWORLD\n3"
    }
    
    template_content = templates.get(method_name, "PLAINTEXT\nKEY")
    
    try:
        # Đảm bảo thư mục tồn tại
        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(filename, 'w') as file:
            file.write(template_content)
        print(f"Đã tạo file mẫu {filename} với nội dung:")
        print(template_content)
        return True
    except Exception as e:
        print(f"Lỗi khi tạo file mẫu: {e}")
        return False

def read_from_file(method_name):
    """Read input from a file based on method name"""
    filename = get_file_path(f"input{method_name}.txt")
    try:
        print(f"Đang tìm file: {filename}")
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            print(f"Đã đọc {len(lines)} dòng từ file.")
            if len(lines) == 0:
                print(f"File {filename} trống.")
                return "", ""
                
            # Bỏ qua các dòng comment (bắt đầu bằng //)
            cleaned_lines = [line for line in lines if not line.strip().startswith("//")]
            
            if len(cleaned_lines) < 2:
                print(f"File {filename} không đúng định dạng. Cần có ít nhất 2 dòng (văn bản và khóa).")
                print(f"Nội dung file hiện tại: {lines}")
                return "", ""
                
            text = cleaned_lines[0].strip().upper()
            key = cleaned_lines[1].strip().upper()
            return text, key
    except FileNotFoundError:
        print(f"File {filename} không tìm thấy. Tạo file mẫu mới.")
        if create_template_input_file(method_name):
            # Đọc lại file sau khi tạo
            return read_from_file(method_name)
        return "", ""
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
        print(f"Đường dẫn đầy đủ: {filename}")
        return "", ""

def write_to_file(method_name, content):
    """Write output to a file based on method name"""
    filename = get_file_path(f"output{method_name}.txt")
    try:
        # Đảm bảo thư mục tồn tại
        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Kết quả đã được ghi vào file {filename}")
    except Exception as e:
        print(f"Lỗi khi ghi file: {e}")
        print(f"Đường dẫn đã thử: {filename}")

def main():
    try:
        print("Chọn chế độ:")
        print("1. Mã hóa")
        print("2. Giải mã")
        print("3. Hướng dẫn định dạng file input")
        
        try:
            operation = int(input("Nhập lựa chọn: "))
            
            if operation == 3:
                print("\nHƯỚNG DẪN ĐỊNH DẠNG FILE INPUT:")
                print("Mỗi file input cần có ít nhất 2 dòng:")
                print("- Dòng 1: Văn bản cần mã hóa/giải mã")
                print("- Dòng 2: Khóa (số nguyên hoặc chuỗi tùy thuộc vào phương pháp)")
                print("\nVí dụ cho inputCaesar.txt:")
                print("HELLOWORLD")
                print("3")
                print("\nVí dụ cho inputVigenere.txt:")
                print("ATTACKATDAWN")
                print("KEY")
                return
            
            if operation not in [1, 2]:
                print("Chế độ không hợp lệ! Vui lòng chọn 1, 2 hoặc 3.")
                return
                
            print("Chọn phương pháp:")
            print("1. Caesar")
            print("2. Vigenere cơ bản")
            print("3. Vigenere Auto-key")
            print("4. Thay thế đơn")
            print("5. Playfair")
            print("6. Rail Fence")
            
            mode = int(input("Nhập lựa chọn: "))
            
            if mode not in range(1, 7):
                print("Phương pháp không hợp lệ! Vui lòng chọn từ 1 đến 6.")
                return
            
            method_name = get_method_name(mode)
            
            if operation == 1:  # Mã hóa
                text, key_str = read_from_file(method_name)
                if not text:
                    text = input("Nhập văn bản cần mã hóa: ").upper()
                    key_str = ""  # Reset key since we're inputting manually
                else:
                    text = text.upper()
                    print(f"Đã đọc văn bản từ file: {text}")
                    print(f"Đã đọc khóa từ file: {key_str}")
                
                res = ""
                if mode == 1:
                    k = int(key_str) if key_str and key_str.isdigit() else int(input("Nhập khóa k (số nguyên): "))
                    res = caesar(text, k)
                elif mode == 2:
                    key = key_str if key_str else input("Nhập khóa (chuỗi): ").upper()
                    res = vigenere_encrypt(text, key, False)
                elif mode == 3:
                    key = key_str if key_str else input("Nhập khóa (chuỗi): ").upper()
                    res = vigenere_encrypt(text, key, True)
                elif mode == 4:
                    key = key_str if key_str and len(key_str) == 26 else input("Nhập bảng thay thế (26 ký tự): ").upper()
                    res = monoalphabetic_encrypt(text, key)
                elif mode == 5:
                    key = key_str if key_str else input("Nhập khóa Playfair: ").upper()
                    res = playfair_encrypt(text, key)
                elif mode == 6:
                    k = int(key_str) if key_str and key_str.isdigit() else int(input("Nhập số hàng (số nguyên): "))
                    res = rail_fence_cipher(text, k)
                
                print("Kết quả mã hóa:", res)
                write_to_file(method_name, res)
            
            else:  # Giải mã
                text, key_str = read_from_file(method_name)
                if not text:
                    text = input("Nhập văn bản cần giải mã: ").upper()
                    key_str = ""  # Reset key since we're inputting manually
                else:
                    text = text.upper()
                    print(f"Đã đọc văn bản từ file: {text}")
                    print(f"Đã đọc khóa từ file: {key_str}")
                
                res = ""
                if mode == 1:
                    k = int(key_str) if key_str and key_str.isdigit() else int(input("Nhập khóa k (số nguyên): "))
                    res = caesar_decrypt(text, k)
                elif mode == 2:
                    key = key_str if key_str else input("Nhập khóa (chuỗi): ").upper()
                    res = vigenere_decrypt(text, key, False)
                elif mode == 3:
                    key = key_str if key_str else input("Nhập khóa (chuỗi): ").upper()
                    res = vigenere_decrypt(text, key, True)
                elif mode == 4:
                    key = key_str if key_str and len(key_str) == 26 else input("Nhập bảng thay thế (26 ký tự): ").upper()
                    res = monoalphabetic_decrypt(text, key)
                elif mode == 5:
                    key = key_str if key_str else input("Nhập khóa Playfair: ").upper()
                    res = playfair_decrypt(text, key)
                elif mode == 6:
                    k = int(key_str) if key_str and key_str.isdigit() else int(input("Nhập số hàng (số nguyên): "))
                    res = rail_fence_decrypt(text, k)
                
                print("Kết quả giải mã:", res)
                write_to_file(method_name, res)
                
        except ValueError as e:
            print("Lỗi nhập liệu: Vui lòng nhập số nguyên cho các lựa chọn và khóa số.")
            print(f"Chi tiết lỗi: {e}")
            
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
        print("Vui lòng thử lại.")

if __name__ == "__main__":
    main()

