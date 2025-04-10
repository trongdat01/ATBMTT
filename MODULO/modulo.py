import os
import math
from functools import reduce

def get_file_path(filename):
    """Return full path for a file in the MODULO directory"""
    base_dir = "d:/Download/CODE/MODULO/"
    return os.path.join(base_dir, filename)

def create_template_input_file():
    """Create a template input file if it doesn't exist"""
    filename = get_file_path("input.txt")
    template_content = """# Bài 1: Tính lũy thừa modulo (hạ bậc)
499 6337 6337
# Bài 2: Tìm nghịch đảo modulo
2705 6577
# Bài 3: Lũy thừa modulo (Fermat)
281 764 6967
# Bài 4: Tính hàm Euler
2863
# Bài 5: Lũy thừa modulo (Euler)
27 2201 5400
# Bài 6: Lũy thừa modulo (số dư Trung Hoa)
101 76 49913
# Bài 7: Giải hệ phương trình modulo
11 13 17 6 2 4
# Bài 8: Kiểm tra căn nguyên thủy
11 293
# Bài 9: Tìm logarit rời rạc
3 8 19
# Bài 10: Biểu thức modulo cơ bản
83 17 354 314 241"""
    
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

def read_input():
    """Read input from the input file"""
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
        current_problem = None
        
        for line in lines:
            line = line.strip()
            if not line:
                # Skip empty lines
                continue
                
            if line.startswith('#'):
                # Extract problem number from comment
                if 'Bài' in line:
                    try:
                        # Extract problem number more carefully
                        parts = line.split(':')[0].split()
                        for part in parts:
                            if part.isdigit():
                                current_problem = int(part)
                                break
                    except:
                        # If there's an error, just continue
                        pass
                continue
            
            # Only process data lines
            if current_problem is not None:
                try:
                    params[current_problem] = list(map(int, line.split()))
                    current_problem = None
                except ValueError as e:
                    print(f"Warning: Could not parse line as integers: {line}")
                    print(f"Error: {e}")
        
        return params
    except Exception as e:
        print(f"Error reading input file: {e}")
        return None

def write_output(results):
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

def mod_pow(base, exponent, modulus):
    """Fast modular exponentiation using binary exponentiation"""
    if modulus == 1:
        return 0
    
    result = 1
    base %= modulus
    
    while exponent > 0:
        # If exponent is odd, multiply result with base
        if exponent % 2 == 1:
            result = (result * base) % modulus
        
        # Exponent integer division by 2
        exponent >>= 1
        # Square the base
        base = (base * base) % modulus
    
    return result

def extended_gcd(a, b):
    """Extended Euclidean Algorithm for gcd and Bézout coefficients"""
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return (gcd, y - (b // a) * x, x)

def mod_inverse(a, m):
    """Find modular multiplicative inverse using Extended Euclidean Algorithm"""
    gcd, x, y = extended_gcd(a, m)
    
    if gcd != 1:
        raise ValueError(f"Modular inverse does not exist (gcd({a}, {m}) = {gcd} ≠ 1)")
    else:
        return (x % m + m) % m  # Ensure the result is positive

def is_prime(n):
    """Check if a number is prime using trial division"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    
    return True

def euler_totient(n):
    """Calculate Euler's totient function φ(n)"""
    if n <= 0:
        return 0
    
    # Special case for prime numbers
    if is_prime(n):
        return n - 1
    
    result = n  # Start with n
    
    # Find prime factors and apply the formula
    p = 2
    while p * p <= n:
        if n % p == 0:
            # p is a prime factor
            while n % p == 0:
                n //= p
            result -= result // p  # Apply φ(n) = n * (1 - 1/p) for each prime p
        p += 1
    
    # If n is a prime factor greater than sqrt(original n)
    if n > 1:
        result -= result // n
    
    return result

def prime_factorization(n):
    """Find the prime factorization of n"""
    factors = {}
    d = 2
    
    while d * d <= n:
        while n % d == 0:
            if d in factors:
                factors[d] += 1
            else:
                factors[d] = 1
            n //= d
        d += 1
    
    if n > 1:
        if n in factors:
            factors[n] += 1
        else:
            factors[n] = 1
    
    return factors

def chinese_remainder(remainders, moduli):
    """
    Solve the system of congruences using Chinese Remainder Theorem:
    x ≡ remainders[i] (mod moduli[i]) for i = 0, 1, ..., k-1
    """
    # Check if moduli are pairwise coprime
    for i in range(len(moduli)):
        for j in range(i + 1, len(moduli)):
            if math.gcd(moduli[i], moduli[j]) != 1:
                raise ValueError(f"Moduli must be pairwise coprime, but gcd({moduli[i]}, {moduli[j]}) ≠ 1")
    
    # Calculate product of all moduli
    N = reduce(lambda x, y: x * y, moduli)
    
    # Calculate partial product and modular inverse
    result = 0
    for i in range(len(remainders)):
        Ni = N // moduli[i]
        Mi = mod_inverse(Ni, moduli[i])
        result += remainders[i] * Ni * Mi
    
    return result % N

def is_primitive_root(a, n):
    """Check if a is a primitive root modulo n"""
    # Check if n is prime (primitive roots only exist for prime moduli)
    if not is_prime(n):
        # Special case for powers of primes
        # Note: Full implementation would need more complex logic
        return False
    
    phi = euler_totient(n)
    factors = prime_factorization(phi)
    
    # Check if a^(phi/p) ≡ 1 (mod n) for any prime factor p of φ(n)
    for prime, power in factors.items():
        if mod_pow(a, phi // prime, n) == 1:
            return False
    
    return True

def discrete_log(a, b, n):
    """Find x such that a^x ≡ b (mod n) using baby-step giant-step algorithm"""
    # Check if b is in the range of a^x mod n
    if math.gcd(a, n) != 1:
        # If a and n are not coprime, need more complex algorithm
        # For simplicity, assume they're coprime in this implementation
        raise ValueError("This implementation requires gcd(a, n) = 1")
    
    # Calculate m = ⌈√n⌉
    m = math.ceil(math.sqrt(n))
    
    # Build table of values a^j mod n for j = 0, 1, ..., m-1
    table = {}
    for j in range(m):
        table[mod_pow(a, j, n)] = j
    
    # Calculate a^(-m) mod n
    a_inv = mod_inverse(a, n)
    a_m_inv = mod_pow(a_inv, m, n)
    
    # Check for each i = 0, 1, ..., m-1 if b * (a^(-m))^i is in the table
    value = b
    for i in range(m):
        if value in table:
            return i * m + table[value]
        value = (value * a_m_inv) % n
    
    # If we get here, no solution was found
    return None

def solve_problem_1(a, m, n):
    """Calculate b = a^m mod n using fast modular exponentiation"""
    result = mod_pow(a, m, n)
    
    steps = []
    steps.append(f"Tính b = a^m mod n = {a}^{m} mod {n} bằng hạ bậc lũy thừa")
    
    # Generate binary representation of exponent
    bin_m = bin(m)[2:]  # remove '0b' prefix
    steps.append(f"Biểu diễn m = {m} dưới dạng nhị phân: {bin_m}")
    
    # Explain the algorithm steps
    steps.append("Khởi tạo: b = 1")
    
    b = 1
    x = a % n
    steps.append(f"x = a mod n = {a} mod {n} = {x}")
    
    for i, bit in enumerate(bin_m):
        if bit == '1':
            b = (b * x) % n
            steps.append(f"Bit thứ {i+1} là 1 → b = b * x mod n = {b}")
        x = (x * x) % n
        if i < len(bin_m) - 1:
            steps.append(f"x = x^2 mod n = {x}")
    
    steps.append(f"Kết quả: b = {result}")
    
    return {
        'result': result,
        'steps': steps
    }

def solve_problem_2(a, n):
    """Find modular inverse x = a^(-1) mod n"""
    steps = []
    steps.append(f"Tìm nghịch đảo modulo x = a^(-1) mod n = {a}^(-1) mod {n}")
    
    try:
        # Using Extended Euclidean Algorithm
        gcd, x, y = extended_gcd(a, n)
        
        # Show steps of the Extended Euclidean Algorithm
        steps.append("Sử dụng thuật toán Euclid mở rộng:")
        
        # Recreate the steps of the algorithm for display
        a_copy, n_copy = a, n
        quotients = []
        while n_copy != 0:
            quotients.append(a_copy // n_copy)
            a_copy, n_copy = n_copy, a_copy % n_copy
        
        # Show the gcd computation steps
        steps.append(f"GCD({a}, {n}) = {gcd}")
        
        if gcd != 1:
            steps.append(f"Không tồn tại nghịch đảo vì GCD({a}, {n}) = {gcd} ≠ 1")
            return {
                'result': "Không tồn tại",
                'steps': steps
            }
        
        # Ensure x is positive
        x = (x % n + n) % n
        
        # Verify the result
        steps.append(f"x = {x}")
        steps.append(f"Kiểm tra: (a * x) mod n = ({a} * {x}) mod {n} = {(a * x) % n}")
        
        return {
            'result': x,
            'steps': steps
        }
    except Exception as e:
        steps.append(f"Lỗi: {str(e)}")
        return {
            'result': "Lỗi",
            'steps': steps
        }

def solve_problem_3(a, m, n):
    """Calculate b = a^m mod n using Fermat's Little Theorem"""
    steps = []
    steps.append(f"Tính b = a^m mod n = {a}^{m} mod {n} sử dụng định lý Fermat")
    
    # Check if n is prime
    if is_prime(n):
        steps.append(f"n = {n} là số nguyên tố, nên áp dụng định lý Fermat: a^(p-1) ≡ 1 (mod p) nếu gcd(a, p) = 1")
        
        # Check if a and n are coprime
        if math.gcd(a, n) == 1:
            # Apply Fermat's Little Theorem: a^(p-1) ≡ 1 (mod p)
            # So a^m ≡ a^(m mod (p-1)) (mod p)
            reduced_exponent = m % (n - 1)
            steps.append(f"gcd({a}, {n}) = 1, nên a^{m} ≡ a^({m} mod {n-1}) ≡ a^{reduced_exponent} (mod {n})")
            
            result = mod_pow(a, reduced_exponent, n)
            steps.append(f"Tính a^{reduced_exponent} mod {n} = {result}")
        else:
            steps.append(f"gcd({a}, {n}) ≠ 1, nên không áp dụng được định lý Fermat")
            steps.append(f"Tính trực tiếp a^{m} mod {n}")
            result = mod_pow(a, m, n)
    else:
        steps.append(f"n = {n} không là số nguyên tố, nên không áp dụng định lý Fermat")
        steps.append(f"Tính trực tiếp a^{m} mod {n}")
        result = mod_pow(a, m, n)
    
    steps.append(f"Kết quả: b = {result}")
    
    return {
        'result': result,
        'steps': steps
    }

def solve_problem_4(n):
    """Calculate Euler's totient function φ(n)"""
    steps = []
    steps.append(f"Tính hàm Euler φ({n})")
    
    # Special case for prime number
    if is_prime(n):
        steps.append(f"n = {n} là số nguyên tố, nên φ(n) = n - 1 = {n - 1}")
        return {
            'result': n - 1,
            'steps': steps
        }
    
    # Find prime factorization
    factors = prime_factorization(n)
    steps.append(f"Phân tích {n} thành thừa số nguyên tố: {n} = " + 
                 " * ".join([f"{p}^{e}" for p, e in factors.items()]))
    
    # Apply Euler's product formula
    steps.append("Áp dụng công thức tích Euler:")
    steps.append(f"φ(n) = n * ∏(1 - 1/p) với p là các ước số nguyên tố của n")
    
    result = n
    formula_parts = [f"{n}"]
    
    for p in factors:
        result *= (1 - 1/p)
        formula_parts.append(f"(1 - 1/{p})")
    
    steps.append(f"φ({n}) = {' * '.join(formula_parts)} = {int(result)}")
    
    return {
        'result': int(result),
        'steps': steps
    }

def solve_problem_5(a, m, n):
    """Calculate b = a^m mod n using Euler's Theorem"""
    steps = []
    steps.append(f"Tính b = a^m mod n = {a}^{m} mod {n} sử dụng định lý Euler")
    
    # Calculate φ(n)
    phi_n = euler_totient(n)
    steps.append(f"Tính φ({n}) = {phi_n}")
    
    # Check if a and n are coprime
    if math.gcd(a, n) == 1:
        steps.append(f"gcd({a}, {n}) = 1, nên áp dụng định lý Euler: a^φ(n) ≡ 1 (mod n)")
        
        # Apply Euler's theorem: a^φ(n) ≡ 1 (mod n)
        # So a^m ≡ a^(m mod φ(n)) (mod n)
        reduced_exponent = m % phi_n
        steps.append(f"a^{m} ≡ a^({m} mod φ({n})) ≡ a^{reduced_exponent} (mod {n})")
        
        result = mod_pow(a, reduced_exponent, n)
        steps.append(f"Tính a^{reduced_exponent} mod {n} = {result}")
    else:
        steps.append(f"gcd({a}, {n}) ≠ 1, nên không áp dụng được định lý Euler")
        steps.append(f"Tính trực tiếp a^{m} mod {n}")
        result = mod_pow(a, m, n)
    
    steps.append(f"Kết quả: b = {result}")
    
    return {
        'result': result,
        'steps': steps
    }

def solve_problem_6(a, k, n):
    """Calculate b = a^k mod n using Chinese Remainder Theorem"""
    steps = []
    steps.append(f"Tính b = a^k mod n = {a}^{k} mod {n} sử dụng định lý số dư Trung Hoa")
    
    # Find the prime factorization of n
    factors = prime_factorization(n)
    steps.append(f"Phân tích {n} thành thừa số nguyên tố: {n} = " + 
                 " * ".join([f"{p}^{e}" for p, e in factors.items()]))
    
    # Check if n is a product of pairwise coprime numbers
    if len(factors) <= 1:
        steps.append(f"n = {n} không có nhiều thừa số nguyên tố khác nhau, nên không cần dùng định lý số dư Trung Hoa")
        steps.append(f"Tính trực tiếp a^{k} mod {n}")
        result = mod_pow(a, k, n)
        steps.append(f"Kết quả: b = {result}")
        return {
            'result': result,
            'steps': steps
        }
    
    # Create the system of congruences
    moduli = []
    remainders = []
    
    for p, e in factors.items():
        p_e = p ** e
        moduli.append(p_e)
        
        # Calculate a^k mod p^e
        phi_p_e = euler_totient(p_e)
        
        if math.gcd(a, p) == 1:
            # If a and p are coprime, we can use Euler's theorem
            reduced_exponent = k % phi_p_e
            steps.append(f"Tính a^{k} mod {p_e}:")
            steps.append(f"  φ({p_e}) = {phi_p_e}")
            steps.append(f"  gcd({a}, {p}) = 1, nên a^{k} ≡ a^({k} mod φ({p_e})) ≡ a^{reduced_exponent} (mod {p_e})")
        else:
            # If a and p are not coprime, we need to handle differently
            # For simplicity, compute directly
            reduced_exponent = k
            steps.append(f"Tính a^{k} mod {p_e} trực tiếp (a và p không nguyên tố cùng nhau)")
        
        remainder = mod_pow(a, reduced_exponent, p_e)
        steps.append(f"  a^{reduced_exponent} mod {p_e} = {remainder}")
        
        remainders.append(remainder)
    
    # Solve the system using Chinese Remainder Theorem
    steps.append("Giải hệ phương trình đồng dư sau:")
    for i in range(len(moduli)):
        steps.append(f"  x ≡ {remainders[i]} (mod {moduli[i]})")
    
    try:
        result = chinese_remainder(remainders, moduli)
        steps.append(f"Áp dụng định lý số dư Trung Hoa, ta có: x = {result}")
    except Exception as e:
        steps.append(f"Lỗi khi áp dụng định lý số dư Trung Hoa: {str(e)}")
        steps.append("Tính trực tiếp")
        result = mod_pow(a, k, n)
    
    steps.append(f"Vậy b = a^k mod n = {result}")
    
    return {
        'result': result,
        'steps': steps
    }

def solve_problem_7(m1, m2, m3, a1, a2, a3):
    """Solve the system of congruences using Chinese Remainder Theorem"""
    steps = []
    steps.append("Giải hệ phương trình đồng dư:")
    steps.append(f"  x ≡ {a1} (mod {m1})")
    steps.append(f"  x ≡ {a2} (mod {m2})")
    steps.append(f"  x ≡ {a3} (mod {m3})")
    
    # Check if the moduli are pairwise coprime
    gcd_12 = math.gcd(m1, m2)
    gcd_13 = math.gcd(m1, m3)
    gcd_23 = math.gcd(m2, m3)
    
    if gcd_12 != 1 or gcd_13 != 1 or gcd_23 != 1:
        steps.append("Các modulo không nguyên tố cùng nhau từng đôi một:")
        if gcd_12 != 1:
            steps.append(f"  gcd({m1}, {m2}) = {gcd_12} ≠ 1")
        if gcd_13 != 1:
            steps.append(f"  gcd({m1}, {m3}) = {gcd_13} ≠ 1")
        if gcd_23 != 1:
            steps.append(f"  gcd({m2}, {m3}) = {gcd_23} ≠ 1")
        steps.append("Không thể áp dụng định lý số dư Trung Hoa trực tiếp.")
        return {
            'result': "Không giải được",
            'steps': steps
        }
    
    try:
        # Calculate M = m1 * m2 * m3
        M = m1 * m2 * m3
        steps.append(f"Tính M = m1 * m2 * m3 = {m1} * {m2} * {m3} = {M}")
        
        # Calculate M1, M2, M3
        M1 = M // m1
        M2 = M // m2
        M3 = M // m3
        
        steps.append(f"M1 = M / m1 = {M} / {m1} = {M1}")
        steps.append(f"M2 = M / m2 = {M} / {m2} = {M2}")
        steps.append(f"M3 = M / m3 = {M} / {m3} = {M3}")
        
        # Calculate modular inverses
        y1 = mod_inverse(M1, m1)
        y2 = mod_inverse(M2, m2)
        y3 = mod_inverse(M3, m3)
        
        steps.append(f"Tính các nghịch đảo modulo:")
        steps.append(f"  y1 = M1^(-1) mod m1 = {M1}^(-1) mod {m1} = {y1}")
        steps.append(f"  y2 = M2^(-1) mod m2 = {M2}^(-1) mod {m2} = {y2}")
        steps.append(f"  y3 = M3^(-1) mod m3 = {M3}^(-1) mod {m3} = {y3}")
        
        # Calculate the result
        x = (a1 * M1 * y1 + a2 * M2 * y2 + a3 * M3 * y3) % M
        
        steps.append("Tính kết quả theo công thức:")
        steps.append(f"  x = (a1 * M1 * y1 + a2 * M2 * y2 + a3 * M3 * y3) mod M")
        steps.append(f"  x = ({a1} * {M1} * {y1} + {a2} * {M2} * {y2} + {a3} * {M3} * {y3}) mod {M}")
        steps.append(f"  x = {x}")
        
        # Verify the result
        steps.append("Kiểm tra kết quả:")
        steps.append(f"  {x} mod {m1} = {x % m1} ≡ {a1} (mod {m1})")
        steps.append(f"  {x} mod {m2} = {x % m2} ≡ {a2} (mod {m2})")
        steps.append(f"  {x} mod {m3} = {x % m3} ≡ {a3} (mod {m3})")
        
        return {
            'result': x,
            'steps': steps
        }
    except Exception as e:
        steps.append(f"Lỗi: {str(e)}")
        return {
            'result': "Lỗi",
            'steps': steps
        }

def solve_problem_8(a, n):
    """Check if a is a primitive root of n"""
    steps = []
    steps.append(f"Kiểm tra xem {a} có phải là căn nguyên thủy của {n} không")
    
    # Check if n is prime
    if not is_prime(n):
        steps.append(f"{n} không phải là số nguyên tố")
        steps.append("Căn nguyên thủy chỉ tồn tại cho modulo là số nguyên tố hoặc một số dạng đặc biệt")
        return {
            'result': False,
            'steps': steps
        }
    
    # Calculate φ(n)
    phi_n = euler_totient(n)
    steps.append(f"Tính φ({n}) = {phi_n}")
    
    # Find the prime factorization of φ(n)
    factors = prime_factorization(phi_n)
    steps.append(f"Phân tích φ({n}) = {phi_n} thành thừa số nguyên tố: {phi_n} = " + 
                 " * ".join([f"{p}^{e}" for p, e in factors.items()]))
    
    # Check if a^(φ(n)/p) ≡ 1 (mod n) for each prime factor p of φ(n)
    is_root = True
    unique_factors = list(factors.keys())
    
    steps.append("Kiểm tra điều kiện: a^(φ(n)/p) ≢ 1 (mod n) với mọi ước số nguyên tố p của φ(n)")
    
    for p in unique_factors:
        power = phi_n // p
        remainder = mod_pow(a, power, n)
        steps.append(f"  Kiểm tra a^(φ(n)/{p}) mod n = {a}^{power} mod {n} = {remainder}")
        
        if remainder == 1:
            steps.append(f"  {a}^{power} ≡ 1 (mod {n}), nên {a} không phải là căn nguyên thủy")
            is_root = False
            break
    
    if is_root:
        # Verify by checking all powers from 1 to φ(n) - 1
        remainders = set()
        for i in range(1, phi_n):
            remainders.add(mod_pow(a, i, n))
        
        is_root = len(remainders) == phi_n - 1
        
        steps.append(f"Kiểm tra thêm: tất cả {a}^k mod {n} với k = 1, 2, ..., φ(n) - 1 phải khác nhau")
        steps.append(f"Kết quả: {a} {'là' if is_root else 'không phải là'} căn nguyên thủy của {n}")
    
    return {
        'result': is_root,
        'steps': steps
    }

def solve_problem_9(a, b, n):
    """Find discrete logarithm: k = log_a b (mod n)"""
    steps = []
    steps.append(f"Tìm logarit rời rạc k = log_{a} {b} (mod {n})")
    
    # Check if n is prime
    if not is_prime(n):
        steps.append(f"{n} không phải là số nguyên tố. Để đơn giản, thuật toán giả định n là số nguyên tố.")
    
    # Check if a is a primitive root of n
    if not is_primitive_root(a, n):
        steps.append(f"{a} không phải là căn nguyên thủy của {n}. Không đảm bảo tìm được logarit.")
    
    # Use baby-step giant-step algorithm
    steps.append("Sử dụng thuật toán 'baby-step giant-step':")
    
    # Calculate m = ⌈√n⌉
    m = math.ceil(math.sqrt(n))
    steps.append(f"Tính m = ⌈√{n}⌉ = {m}")
    
    steps.append("Bước 1: Tính bảng các giá trị a^j mod n với j = 0, 1, ..., m-1")
    table = {}
    for j in range(m):
        value = mod_pow(a, j, n)
        table[value] = j
        if j < 10 or j > m - 10:  # Show only some entries to avoid large output
            steps.append(f"  a^{j} mod {n} = {value}")
        elif j == 10:
            steps.append("  ...")
    
    steps.append(f"Bước 2: Tính a^(-m) mod {n}")
    a_inv = mod_inverse(a, n)
    a_m_inv = mod_pow(a_inv, m, n)
    steps.append(f"  a^(-1) mod {n} = {a_inv}")
    steps.append(f"  a^(-m) mod {n} = {a_m_inv}")
    
    steps.append(f"Bước 3: Tìm i và j sao cho b * (a^(-m))^i ≡ a^j (mod {n})")
    value = b
    result = None
    
    for i in range(m):
        if value in table:
            j = table[value]
            result = i * m + j
            steps.append(f"  Tìm thấy: b * (a^(-m))^{i} = {value} ≡ a^{j} (mod {n})")
            steps.append(f"  Vậy k = i*m + j = {i}*{m} + {j} = {result}")
            break
        
        value = (value * a_m_inv) % n
        if i < 5 or i > m - 5:  # Show only some iterations
            steps.append(f"  b * (a^(-m))^{i+1} mod {n} = {value}")
        elif i == 5:
            steps.append("  ...")
    
    if result is None:
        steps.append("Không tìm thấy giá trị k thỏa mãn")
    else:
        # Verify the result
        check = mod_pow(a, result, n)
        steps.append(f"Kiểm tra: a^k mod n = {a}^{result} mod {n} = {check} ≡ {b} (mod {n})")
    
    return {
        'result': result,
        'steps': steps
    }

def solve_problem_10(a, b, x, y, n):
    """Calculate basic modular expressions"""
    steps = []
    results = {}
    
    # Calculate A1 = (a*x + b*y) mod n
    A1 = (a * x + b * y) % n
    steps.append(f"A1 = (a*x + b*y) mod n = ({a}*{x} + {b}*{y}) mod {n} = {A1}")
    results['A1'] = A1
    
    # Calculate A2 = (a*x - b*y) mod n
    A2 = (a * x - b * y) % n
    steps.append(f"A2 = (a*x - b*y) mod n = ({a}*{x} - {b}*{y}) mod {n} = {A2}")
    results['A2'] = A2
    
    # Calculate A3 = (a*x * b*y) mod n
    A3 = (a * x * b * y) % n
    steps.append(f"A3 = (a*x * b*y) mod n = ({a}*{x} * {b}*{y}) mod {n} = {A3}")
    results['A3'] = A3
    
    # Calculate A4 = (b*y)^(-1) mod n
    try:
        by = (b * y) % n
        A4 = mod_inverse(by, n)
        steps.append(f"A4 = (b*y)^(-1) mod n = ({b}*{y})^(-1) mod {n} = {A4}")
        results['A4'] = A4
        
        # Calculate A5 = (a*x / b*y) mod n = (a*x * (b*y)^(-1)) mod n
        A5 = (a * x * A4) % n
        steps.append(f"A5 = (a*x / b*y) mod n = (a*x * (b*y)^(-1)) mod n = ({a}*{x} * {A4}) mod {n} = {A5}")
        results['A5'] = A5
    except Exception as e:
        steps.append(f"Lỗi khi tính A4 và A5: {str(e)}")
        results['A4'] = "Không tồn tại"
        results['A5'] = "Không tồn tại"
    
    return {
        'results': results,
        'steps': steps
    }

def main():
    # Read input from file
    params = read_input()
    if not params:
        return
    
    # Initialize output string
    output = "KẾT QUẢ TÍNH TOÁN\n\n"
    
    # Solve problem 1
    if 1 in params:
        a, m, n = params[1]
        result = solve_problem_1(a, m, n)
        output += "Bài 1: TÍNH LŨY THỪA MODULO BẰNG CÁCH HẠ BẬC LŨY THỪA\n"
        output += f"Input: a = {a}; m = {m}; n = {n}\n"
        output += "\n".join(result['steps']) + "\n"
        output += f"Output: b = {result['result']}\n\n"
    
    # Solve problem 2
    if 2 in params:
        a, n = params[2]
        result = solve_problem_2(a, n)
        output += "Bài 2: TÌM NGHỊCH ĐẢO MODULO\n"
        output += f"Input: a = {a}; n = {n}\n"
        output += "\n".join(result['steps']) + "\n"
        output += f"Output: x = {result['result']}\n\n"
    
    # Solve problem 3
    if 3 in params:
        a, m, n = params[3]
        result = solve_problem_3(a, m, n)
        output += "Bài 3: TÍNH LŨY THỪA MODULO SỬ DỤNG ĐỊNH LÝ FERMAT\n"
        output += f"Input: a = {a}; m = {m}; n = {n}\n"
        output += "\n".join(result['steps']) + "\n"
        output += f"Output: b = {result['result']}\n\n"
    
    # Solve problem 4
    if 4 in params:
        n = params[4][0]
        result = solve_problem_4(n)
        output += "Bài 4: TÍNH GIÁ TRỊ HÀM EULER\n"
        output += f"Input: n = {n}\n"
        output += "\n".join(result['steps']) + "\n"
        output += f"Output: φ(n) = {result['result']}\n\n"
    
    # Solve problem 5
    if 5 in params:
        a, m, n = params[5]
        result = solve_problem_5(a, m, n)
        output += "Bài 5: TÍNH LŨY THỪA MODULO SỬ DỤNG ĐỊNH LÝ EULER\n"
        output += f"Input: a = {a}; m = {m}; n = {n}\n"
        output += "\n".join(result['steps']) + "\n"
        output += f"Output: b = {result['result']}\n\n"
    
    # Solve problem 6
    if 6 in params:
        a, k, n = params[6]
        result = solve_problem_6(a, k, n)
        output += "Bài 6: TÍNH LŨY THỪA MODULO SỬ DỤNG ĐỊNH LÝ SỐ DƯ TRUNG HOA\n"
        output += f"Input: a = {a}; k = {k}; n = {n}\n"
        output += "\n".join(result['steps']) + "\n"
        output += f"Output: b = {result['result']}\n\n"
    
    # Solve problem 7
    if 7 in params:
        m1, m2, m3, a1, a2, a3 = params[7]
        result = solve_problem_7(m1, m2, m3, a1, a2, a3)
        output += "Bài 7: GIẢI HỆ PHƯƠNG TRÌNH MODULO SỬ DỤNG ĐỊNH LÝ SỐ DƯ TRUNG HOA\n"
        output += f"Input: m1 = {m1}; m2 = {m2}; m3 = {m3}; a1 = {a1}; a2 = {a2}; a3 = {a3}\n"
        output += "\n".join(result['steps']) + "\n"
        output += f"Output: x = {result['result']}\n\n"
    
    # Solve problem 8
    if 8 in params:
        a, n = params[8]
        result = solve_problem_8(a, n)
        output += "Bài 8: KIỂM TRA CĂN NGUYÊN THỦY\n"
        output += f"Input: a = {a}; n = {n}\n"
        output += "\n".join(result['steps']) + "\n"
        output += f"Output: {a} {'là' if result['result'] else 'không phải là'} căn nguyên thủy của {n}\n\n"
    
    # Solve problem 9
    if 9 in params:
        a, b, n = params[9]
        result = solve_problem_9(a, b, n)
        output += "Bài 9: TÌM LOGARIT RỜI RẠC\n"
        output += f"Input: a = {a}; b = {b}; n = {n}\n"
        output += "\n".join(result['steps']) + "\n"
        output += f"Output: k = {result['result']}\n\n"
    
    # Solve problem 10
    if 10 in params:
        a, b, x, y, n = params[10]
        result = solve_problem_10(a, b, x, y, n)
        output += "Bài 10: TÍNH CÁC BIỂU THỨC MODULO CƠ BẢN\n"
        output += f"Input: a = {a}; b = {b}; x = {x}; y = {y}; n = {n}\n"
        output += "\n".join(result['steps']) + "\n"
        output += f"Output: A1 = {result['results']['A1']}; A2 = {result['results']['A2']}; "
        output += f"A3 = {result['results']['A3']}; A4 = {result['results']['A4']}; "
        output += f"A5 = {result['results']['A5']}\n"
    
    # Write output to file
    write_output(output)

if __name__ == "__main__":
    main()
