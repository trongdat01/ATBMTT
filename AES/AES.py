import numpy as np
import os
import io
import sys

# AES S-box
sbox = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

# Round constants for key expansion
rcon = [
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36
]

# Matrix for MixColumns
mix_columns_matrix = [
    [0x02, 0x03, 0x01, 0x01],
    [0x01, 0x02, 0x03, 0x01],
    [0x01, 0x01, 0x02, 0x03],
    [0x03, 0x01, 0x01, 0x02]
]

def bytes_to_matrix(bytes_array):
    """Convert a 16-byte array into a 4x4 matrix (column-major order)"""
    return [list(bytes_array[i:i+4]) for i in range(0, len(bytes_array), 4)]

def matrix_to_bytes(matrix):
    """Convert a 4x4 matrix into a 16-byte array (column-major order)"""
    result = []
    for i in range(4):
        for row in matrix:
            result.append(row[i])
    return bytes(result)

def matrix_to_hex(matrix):
    """Convert a matrix to a hex string representation"""
    result = ""
    for i in range(4):
        for row in matrix:
            result += f"{row[i]:02X}"
    return result

def hex_to_bytes(hex_string):
    """Convert a hex string to a byte array"""
    return bytes.fromhex(hex_string)

def xor_bytes(a, b):
    """XOR two byte arrays"""
    return bytes(x ^ y for x, y in zip(a, b))

def rot_word(word):
    """Circular left shift of a word (4 bytes)"""
    return word[1:] + word[:1]

def sub_word(word):
    """Apply S-box substitution to each byte in a word"""
    return bytes(sbox[b] for b in word)

def xor_with_rcon(word, round_index):
    """XOR word with round constant"""
    result = bytearray(word)
    result[0] ^= rcon[round_index]
    return bytes(result)

def key_expansion(key, collector=None):
    """Expand the key into round keys"""
    # Convert the key to a list of words (4-byte chunks)
    key_bytes = hex_to_bytes(key)
    key_words = [key_bytes[i:i+4] for i in range(0, len(key_bytes), 4)]
    
    # Initialize expanded key with original key
    expanded_key = key_words.copy()
    
    # Print initial words
    print("\nPHẦN 1: SINH 10 KHÓA Ki từ khóa K, i = 1, 2, ..., 10.")
    print("\n1. Chia khóa K (128 bit) thành 4 word (32 bit)")
    print(f"Input: K = {key}")
    
    for i, word in enumerate(key_words):
        word_hex = ''.join([f"{b:02X}" for b in word])
        print(f"Output: w{i} = {word_hex}", end=", " if i < 3 else "\n")
    
    # Generate 40 more words for round keys (10 rounds * 4 words per round)
    for i in range(4, 44):
        temp = expanded_key[i-1]
        
        if i % 4 == 0:
            # If we're starting a new round key
            # Print rotation step
            print(f"\n2. Dịch vòng trái 1 byte đối với w{i-1} (32 bit)")
            temp_hex = ''.join([f"{b:02X}" for b in temp])
            print(f"Input: w{i-1} = {temp_hex}")
            
            temp = rot_word(temp)
            temp_hex = ''.join([f"{b:02X}" for b in temp])
            print(f"Output: rw = RotWord(w{i-1}) = {temp_hex}")
            
            # Print substitution step
            print(f"\n3. Thay thế từng byte trong rw bằng bảng S-box SubWord")
            print(f"Input: rw = {temp_hex}")
            
            temp = sub_word(temp)
            temp_hex = ''.join([f"{b:02X}" for b in temp])
            print(f"Output: sw = SubWord(rw) = {temp_hex}")
            
            # Print XOR with round constant step
            print(f"\n4. sw XORbit với Rcon[{i//4-1}]")
            print(f"Input: sw = {temp_hex}; RC[{i//4}] = {rcon[i//4-1]:02X}000000")
            
            temp = xor_with_rcon(temp, i//4-1)
            temp_hex = ''.join([f"{b:02X}" for b in temp])
            print(f"Output: xcsw = XorRcon(sw, RC[{i//4}]) = {temp_hex}")
            
            # Print key generation
            round_num = i // 4
            print(f"\n5. Tính khóa K{round_num} = (w{i}, w{i+1}, w{i+2}, w{i+3})")
            w_prev_hex = ''.join([f"{b:02X}" for b in expanded_key[i-4]])
            print(f"Input: xcsw = {temp_hex}; w0, w1, w2, w3 (kết quả bài 1);")
        
        new_word = xor_bytes(expanded_key[i-4], temp)
        expanded_key.append(new_word)
        
        # Print word generation
        new_word_hex = ''.join([f"{b:02X}" for b in new_word])
        if i % 4 == 0:
            print(f"Output: w{i} = XORbit(xcsw, w{i-4}) = {new_word_hex}")
        else:
            w_prev_hex = ''.join([f"{b:02X}" for b in expanded_key[i-1]])
            w_4back_hex = ''.join([f"{b:02X}" for b in expanded_key[i-4]])
            print(f"w{i} = XORbit(w{i-1}, w{i-4}) = {new_word_hex}")
            
        # Print lặp lại message after every key is generated
        if i % 4 == 3 and i < 43:
            print("\nLẶP LẠI từ Bài 2 đến Bài 5 để tạo các khóa tiếp theo")
    
    # Convert expanded key words to round keys
    round_keys = []
    for i in range(11):  # 11 because we need the initial key plus 10 round keys
        round_key = b''.join(expanded_key[i*4:(i+1)*4])
        round_keys.append(round_key)
    
    return round_keys

def sub_bytes(state):
    """Apply S-box substitution to each byte in the state"""
    for i in range(4):
        for j in range(4):
            state[i][j] = sbox[state[i][j]]
    return state

def shift_rows(state):
    """Shift rows of the state matrix"""
    state[1] = state[1][1:] + state[1][:1]  # Shift row 1 by 1
    state[2] = state[2][2:] + state[2][:2]  # Shift row 2 by 2
    state[3] = state[3][3:] + state[3][:3]  # Shift row 3 by 3
    return state

def galois_multiply(a, b):
    """Galois field multiplication for MixColumns"""
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        high_bit_set = a & 0x80
        a <<= 1
        if high_bit_set:
            a ^= 0x1B  # XOR with the reduction polynomial x^8 + x^4 + x^3 + x + 1
        b >>= 1
    return p & 0xFF

def mix_columns(state):
    """Mix columns of the state matrix"""
    result = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                result[i][j] ^= galois_multiply(mix_columns_matrix[i][k], state[k][j])
    return result

def add_round_key(state, round_key):
    """XOR state with round key"""
    key_matrix = bytes_to_matrix(round_key)
    for i in range(4):
        for j in range(4):
            state[i][j] ^= key_matrix[i][j]
    return state

def aes_encrypt(message, key, collector=None):
    """AES encryption function"""
    # Convert message and key to bytes
    message_bytes = hex_to_bytes(message)
    
    # Generate round keys
    round_keys = key_expansion(key)
    
    # Convert message to state matrix (column-major order)
    state = bytes_to_matrix(message_bytes)
    
    # Print initial state and key
    print("\nPHẦN 2: MÃ HÓA")
    print("\n6. Tính kết quả AddRoundKey")
    print(f"Input: M = {message}")
    print(f"K = {key}")
    
    # Initial AddRoundKey
    state = add_round_key(state, round_keys[0])
    state_hex = matrix_to_hex(state)
    print(f"Output: state = AddRoundKey(M, K) = {state_hex}")
    
    # 9 rounds of transformation
    for i in range(1, 10):
        print(f"\n======================== VÒNG LẶP THỨ {i} ===========")
        
        # SubBytes
        print(f"\n7. Thay thế từng byte trong state bằng bảng S-box SubByte")
        print(f"Input: state = {state_hex}")
        state = sub_bytes(state)
        state_hex = matrix_to_hex(state)
        print(f"Output: state = SubByte(state) = {state_hex}")
        
        # ShiftRows
        print(f"\n8. Dịch vòng trái các byte trong state ShiftRows")
        print(f"Input: state = {state_hex}")
        state = shift_rows(state)
        state_hex = matrix_to_hex(state)
        print(f"Output: state = ShiftRows(state) = {state_hex}")
        
        # MixColumns
        print(f"\n9. Trộn các byte trong state MixColumns")
        print(f"Input: state = {state_hex}")
        state = mix_columns(state)
        state_hex = matrix_to_hex(state)
        print(f"Output: state = MixColumns(state) = {state_hex}")
        
        # AddRoundKey
        print(f"\n10. Thêm khóa vào state AddRoundKey")
        print(f"Input: state = {state_hex}")
        key_hex = ''.join([f"{b:02X}" for b in round_keys[i]])
        print(f"Ki = {key_hex}")
        state = add_round_key(state, round_keys[i])
        state_hex = matrix_to_hex(state)
        print(f"Output: state = AddRoundKey(state, Ki) = {state_hex}")
    
    # Final round (no MixColumns)
    print(f"\n===================== VÒNG LẶP THỨ 10 ===========")
    print(f"\n11. Vòng lặp cuối (lần lặp 10)")
    print(f"Input: state = {state_hex}")
    key_hex = ''.join([f"{b:02X}" for b in round_keys[10]])
    print(f"K10 = {key_hex}")
    
    # Perform SubBytes
    state = sub_bytes(state)
    state_sub_hex = matrix_to_hex(state)
    
    # Perform ShiftRows
    state = shift_rows(state)
    state_shift_hex = matrix_to_hex(state)
    
    # Perform AddRoundKey
    state = add_round_key(state, round_keys[10])
    
    # Convert state back to bytes
    ciphertext = matrix_to_hex(state)
    print(f"Output: C = state = AddRoundKey(ShiftRows(SubByte(state)), K10) = {ciphertext}")
    
    return ciphertext

def get_file_path(filename):
    """Return full path for a file in the AES directory"""
    base_dir = "d:/Download/CODE/AES/"
    return os.path.join(base_dir, filename)

def create_template_input_file():
    """Create a template input file if it doesn't exist"""
    filename = get_file_path("inputAES.txt")
    template_content = "18DC9095F9149EDB7323F20E4E462D92\nCFD61D489E7C48BC46C9F875C1F04E1B"
    
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

def read_from_file():
    """Read message and key from input file"""
    filename = get_file_path("inputAES.txt")
    try:
        print(f"Đang tìm file: {filename}")
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            print(f"Đã đọc {len(lines)} dòng từ file.")
            if len(lines) < 2:
                print(f"File {filename} không đúng định dạng. Cần có ít nhất 2 dòng (message và key).")
                return "", ""
                
            # Bỏ qua các dòng comment
            cleaned_lines = [line for line in lines if not line.strip().startswith("//")]
            
            if len(cleaned_lines) < 2:
                print(f"File {filename} không đúng định dạng. Cần có ít nhất 2 dòng (message và key).")
                return "", ""
                
            message = cleaned_lines[0].strip()
            key = cleaned_lines[1].strip()
            return message, key
    except FileNotFoundError:
        print(f"File {filename} không tìm thấy. Tạo file mẫu mới.")
        if create_template_input_file():
            # Đọc lại file sau khi tạo
            return read_from_file()
        return "", ""
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
        return "", ""

def write_to_file(content):
    """Write output to a file"""
    filename = get_file_path("outputAES.txt")
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

class OutputCollector:
    """Class to collect output that would normally go to stdout"""
    def __init__(self):
        self.buffer = io.StringIO()
        self.old_stdout = None
        
    def start(self):
        self.old_stdout = sys.stdout
        sys.stdout = self.buffer
        
    def stop(self):
        sys.stdout = self.old_stdout
        
    def get_output(self):
        return self.buffer.getvalue()

def main():
    # Tạo collector để thu thập output
    collector = OutputCollector()
    collector.start()
    
    print("BÀI TẬP NHÓM 1")
    print("NỘI DUNG MÃ HÓA BÀI TẬP AES-128")
    
    # Sử dụng giá trị từ đề bài 
    message = "18DC9095F9149EDB7323F20E4E462D92"
    key = "CFD61D489E7C48BC46C9F875C1F04E1B"
    
    # Kiểm tra và tạo file input nếu chưa có
    input_path = get_file_path("inputAES.txt")
    if not os.path.exists(input_path):
        print("Tạo file input với giá trị từ đề bài...")
        with open(input_path, 'w') as file:
            file.write(f"{message}\n{key}")
        print(f"Đã tạo file input tại: {input_path}")
    else:
        # Đọc dữ liệu từ file nếu có
        message_from_file, key_from_file = read_from_file()
        if message_from_file and key_from_file:
            message = message_from_file
            key = key_from_file
    
    print(f"M = {message}")
    print(f"K = {key}")
    
    # Encrypt
    ciphertext = aes_encrypt(message, key)
    
    print("\nKết quả cuối cùng:")
    print(f"C = {ciphertext}")
    
    # Lấy toàn bộ output đã thu thập
    collector.stop()
    full_output = collector.get_output()
    
    # Ghi kết quả ra file
    write_to_file(full_output)
    
    print(f"\nQuá trình mã hóa hoàn tất.")
    print(f"Kết quả đã được ghi vào: {get_file_path('outputAES.txt')}")

if __name__ == "__main__":
    main()
