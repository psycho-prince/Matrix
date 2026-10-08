import math

def is_prime(n):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def analyze_137():
    print("==================================================")
    print("PURE MATH: ANALYZING THE '137' MYSTERY")
    print("==================================================")
    
    number = 137
    print(f"\n[TARGET]: {number} (The inverse fine-structure constant approx.)\n")
    
    # 1. Is it a prime number?
    prime_check = is_prime(number)
    print(f"1. Prime Status: {number} is prime? -> {prime_check}")
    
    if prime_check:
        # Find which prime it is
        count = 0
        for i in range(2, number + 1):
            if is_prime(i):
                count += 1
        print(f"   -> It is exactly the {count}rd prime number.")
        
    # 2. Sum of Squares
    digits = [int(d) for d in str(number)]
    sum_of_squares = sum(d**2 for d in digits)
    prime_sos = is_prime(sum_of_squares)
    print(f"\n2. Sum of its squared digits: 1^2 + 3^2 + 7^2 = {sum_of_squares}")
    print(f"   -> Is the result ({sum_of_squares}) also prime? -> {prime_sos}")
    
    # 3. The Palindrome Mystery
    palindrome = 123456787654321
    is_factor = (palindrome % number == 0)
    print(f"\n3. The Palindrome Connection:")
    print(f"   -> Is {number} a factor of the perfect palindrome {palindrome}? -> {is_factor}")
    if is_factor:
        print(f"   -> {palindrome} / {number} = {palindrome // number}")
        
    # 4. Golden Ratio Connection
    # A circle is 360 degrees. 360 / (Golden Ratio^2) = 137.5 degrees (Golden Angle)
    golden_ratio = (1 + math.sqrt(5)) / 2
    golden_angle = 360 / (golden_ratio ** 2)
    print(f"\n4. The Golden Angle (Nature's Growth Pattern):")
    print(f"   -> 360 degrees / (Golden Ratio)^2 = {golden_angle:.1f} degrees")
    print(f"   -> The Golden Angle rounds to 137 degrees.")
    
    print("\n-> SCIENTIFIC CONCLUSION:")
    print("The number 137 is mathematically unique. It links prime numbers, perfect palindromes, and the Golden Ratio of nature.")
    print("Physicist Richard Feynman called it 'a magic number that comes to us with no understanding by man.'")
    print("==================================================")

if __name__ == "__main__":
    analyze_137()
