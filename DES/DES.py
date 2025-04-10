import numpy as np
import os
import io
import sys

# DES Tables for permutation and substitution
# Initial Permutation (IP) table
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Inverse Initial Permutation (IP^-1) table
IP_INV = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

# Permutation Choice 1 (PC-1) table for key generation
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

# Permutation Choice 2 (PC-2) table for key generation
PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

# Expansion (E) table
E = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

# Permutation (P) table
P = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]

# S-boxes (substitution boxes)
S = [
    # S1
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    # S2
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    # S3
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    # S4
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    # S5
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    # S6
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    # S7
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    # S8
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

# Number of left shifts for each round
SHIFT_TABLE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

def hex_to_bin(hex_string):
    """Convert a hexadecimal string to a binary string"""
    return ''.join(format(int(hex_char, 16), '04b') for hex_char in hex_string)

def bin_to_hex(binary_string):
    """Convert a binary string to a hexadecimal string"""
    return ''.join(format(int(binary_string[i:i+4], 2), 'X') for i in range(0, len(binary_string), 4))

def permute(input_block, permutation_table):
    """Apply a permutation table to an input block"""
    return ''.join(input_block[i-1] for i in permutation_table)

def shift_left(block, shifts):
    """Circular left shift on a binary string"""
    return block[shifts:] + block[:shifts]

def xor(a, b):
    """XOR two binary strings"""
    return ''.join('1' if a[i] != b[i] else '0' for i in range(len(a)))

def generate_keys(key_hex):
    """Generate 16 subkeys from the main key"""
    # Convert key from hex to binary
    key = hex_to_bin(key_hex)
    
    print("\nPHẦN 1: SINH KHÓA Ki từ khóa K")
    print("1. Tính hoán vị PC1 đối với khóa K:")
    print(f"Input: K = {key_hex}, PC1 (xem tài liệu mục 3.2 DES)")
    
    # Apply PC1 permutation to the key
    key_plus = permute(key, PC1)
    
    # Split key_plus into C0 and D0
    c0 = key_plus[:28]
    d0 = key_plus[28:]
    
    print(f"Output: C0 = {bin_to_hex(c0)}, D0 = {bin_to_hex(d0)}")
    
    # Generate 16 subkeys
    c_values = [c0]
    d_values = [d0]
    subkeys = []
    
    print("\n2. Tính các giá trị dịch vòng Ci, Di:")
    print(f"Input: C0 = {bin_to_hex(c0)}, D0 = {bin_to_hex(d0)}, si (xem tài liệu mục 3.2 DES)")
    
    for i in range(16):
        # Apply left shifts
        c_next = shift_left(c_values[-1], SHIFT_TABLE[i])
        d_next = shift_left(d_values[-1], SHIFT_TABLE[i])
        
        c_values.append(c_next)
        d_values.append(d_next)
        
        # Apply PC2 permutation to Ci+Di
        cd_combined = c_next + d_next
        subkey = permute(cd_combined, PC2)
        subkeys.append(subkey)
        
        print(f"C{i+1} = {bin_to_hex(c_next)}, D{i+1} = {bin_to_hex(d_next)}")
    
    print("\n3. Tính khóa Ki cho vòng lặp thứ i:")
    print("Input: Ci, Di (kết quả bài 2), PC2 (xem tài liệu mục 3.2 DES)")
    
    for i, key in enumerate(subkeys):
        print(f"K{i+1} = {bin_to_hex(key)}")
    
    return subkeys

def s_box_substitution(input_48bit):
    """Apply S-box substitution to the 48-bit input"""
    output_32bit = ""
    
    # Split the 48-bit input into 8 6-bit chunks
    for i in range(8):
        # Extract the 6-bit chunk
        chunk = input_48bit[i*6:(i+1)*6]
        
        # Determine row (first and last bit) and column (middle 4 bits)
        row = int(chunk[0] + chunk[5], 2)
        col = int(chunk[1:5], 2)
        
        # Get the S-box value
        value = S[i][row][col]
        
        # Convert to 4-bit binary and add to output
        output_32bit += format(value, '04b')
    
    return output_32bit

def f_function(right_half, subkey):
    """The Feistel function used in each round of DES"""
    # Expansion E: Expand 32-bit R to 48-bit
    expanded = permute(right_half, E)
    print(f"Output: ER0 = {bin_to_hex(expanded)}")
    
    # XOR with subkey
    xor_result = xor(expanded, subkey)
    print(f"Output: A = {bin_to_hex(xor_result)}")
    
    # S-box substitution: Transform 48-bit to 32-bit
    s_box_output = s_box_substitution(xor_result)
    print(f"Output: B = S(A) = {bin_to_hex(s_box_output)}")
    
    # Permutation P
    p_output = permute(s_box_output, P)
    print(f"Output: F = {bin_to_hex(p_output)}")
    
    return p_output

def des_encrypt(message_hex, key_hex):
    """DES encryption algorithm"""
    # Convert message from hex to binary
    message = hex_to_bin(message_hex)
    
    print("\nPHẦN 2: MÃ HÓA")
    print("4. Tính hoán vị IP đối với bản tin M:")
    print(f"Input: M = {message_hex}, IP (xem tài liệu mục 3.2 DES)")
    
    # Initial Permutation (IP)
    ip_output = permute(message, IP)
    
    # Split into left and right halves
    left_half = ip_output[:32]
    right_half = ip_output[32:]
    
    print(f"Output: L0 = {bin_to_hex(left_half)}, R0 = {bin_to_hex(right_half)}")
    
    # Generate subkeys
    subkeys = generate_keys(key_hex)
    
    # 16 rounds of encryption
    for i in range(16):
        if i == 0:
            print("\n==========  CHI TIẾT VÒNG LẶP THỨ NHẤT ==============")
            print("5. Tính hàm mở rộng nửa phải E[R0]:")
            print(f"Input: R0 = {bin_to_hex(right_half)}, E (xem tài liệu mục 3.2 DES)")
            
            print("\n6. Thực hiên XOR ER0 với khóa K1:")
            print(f"Input: ER0 (kết quả bài 5), K1 = {bin_to_hex(subkeys[0])}")
            
            print("\n7. Thực hiện phép thế S-box đối với B:")
            print(f"Input: A (kết quả bài 6), 8 bảng Si, i = 1, 2, ..., 8 (xem tài liệu mục 3.2 DES)")
            
            print("\n8. Thực hiện hoán vị P đối với SB:")
            print(f"Input: B (kết quả bài 7), P (xem tài liệu mục 3.2 DES)")
            
            # Apply the Feistel function
            f_output = f_function(right_half, subkeys[i])
            
            print("\n========= THỰC HIỆN VÒNG LẶP THỨ NHẤT =================")
            print("9. Thực hiện vòng lặp thứ nhất:")
            print(f"Input: L0 = {bin_to_hex(left_half)}; R0 = {bin_to_hex(right_half)}, F = {bin_to_hex(f_output)}")
            
            # Prepare next round
            new_right = xor(left_half, f_output)
            new_left = right_half
            
            print(f"Output: L1 = R0 = {bin_to_hex(new_left)}; R1 = L0 ⊕ F = {bin_to_hex(new_right)}")
        else:
            print(f"\n========= THỰC HIỆN VÒNG LẶP THỨ {i+1} ==========")
            print(f"10. Thực hiện vòng lặp thứ {i+1}:")
            print(f"Input: L{i} = {bin_to_hex(left_half)}; R{i} = {bin_to_hex(right_half)}")
            
            # Apply the Feistel function
            f_output = f_function(right_half, subkeys[i])
            
            # Prepare next round
            new_right = xor(left_half, f_output)
            new_left = right_half
            
            print(f"Output: L{i+1} = R{i} = {bin_to_hex(new_left)}; R{i+1} = L{i} ⊕ f(R{i},K{i+1}) = {bin_to_hex(new_right)}")
        
        # Update halves for next round
        left_half = new_left
        right_half = new_right
    
    # Final Permutation (IP^-1)
    print("\n========= KẾT THÚC VÒNG LẶP THỨ 16 ======================")
    print("11. Thực hiện hoán vị cuối cùng IP-1:")
    print(f"Input: L16 = {bin_to_hex(left_half)}; R16 = {bin_to_hex(right_half)}, IP-1 (xem tài liệu mục 3.2 DES)")
    
    # Swap left and right halves for the final permutation
    pre_output = right_half + left_half
    
    # Apply inverse initial permutation
    cipher = permute(pre_output, IP_INV)
    cipher_hex = bin_to_hex(cipher)
    
    print(f"Output: C = {cipher_hex}; (bản mã cần tìm)")
    print("\n============ KẾT QUẢ MÃ HÓA ========================")
    
    return cipher_hex

def get_file_path(filename):
    """Return full path for a file in the DES directory"""
    base_dir = "d:/Download/CODE/DES/"
    return os.path.join(base_dir, filename)

def create_template_input_file():
    """Create a template input file if it doesn't exist"""
    filename = get_file_path("inputDES.txt")
    template_content = "FF1C9CA3596B7D48\n3FF81CDA5F417784"
    
    try:
        # Đảm bảo thư mục tồn tại
        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(template_content)
        print(f"Đã tạo file mẫu {filename} với nội dung:")
        print(template_content)
        return True
    except Exception as e:
        print(f"Lỗi khi tạo file mẫu: {e}")
        return False

def read_from_file():
    """Read message and key from input file"""
    filename = get_file_path("inputDES.txt")
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

def write_to_file(content):
    """Write output to a file"""
    filename = get_file_path("outputDES.txt")
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
    # Tạo collector để thu thập output
    collector = OutputCollector()
    collector.start()
    
    print("BÀI TẬP MÃ HÓA DES")
    print("NHÓM 1")
    
    # Mặc định sử dụng giá trị từ đề bài
    message_hex = "FF1C9CA3596B7D48"
    key_hex = "3FF81CDA5F417784"
    
    # Kiểm tra và tạo file input nếu chưa có
    input_path = get_file_path("inputDES.txt")
    if not os.path.exists(input_path):
        print("File input không tồn tại. Đang tạo file mẫu...")
        create_template_input_file()
        print(f"Đã tạo file input tại: {input_path}")
    
    # Đọc dữ liệu từ file nếu có
    message_from_file, key_from_file = read_from_file()
    if message_from_file and key_from_file:
        message_hex = message_from_file
        key_hex = key_from_file
    
    print(f"INPUT:    K = {key_hex};")
    print(f"          M = {message_hex};")
    
    # Encrypt the message
    cipher_hex = des_encrypt(message_hex, key_hex)
    
    print(f"\nOUTPUT: C = {cipher_hex}")
    
    # Lấy toàn bộ output đã thu thập
    collector.stop()
    full_output = collector.get_output()
    
    # Ghi kết quả ra file
    write_to_file(full_output)
    
    print(f"\nQuá trình mã hóa hoàn tất.")
    print(f"Kết quả đã được ghi vào: {get_file_path('outputDES.txt')}")

if __name__ == "__main__":
    main()
