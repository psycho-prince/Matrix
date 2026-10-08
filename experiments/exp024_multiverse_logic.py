def generate_fibonacci(n):
    fib = [1, 1]
    for _ in range(n - 2):
        fib.append(fib[-1] + fib[-2])
    return fib

def test_multiverse_math():
    print("==================================================")
    print("PURE MATH: TESTING LOGIC ACROSS UNIVERSES")
    print("==================================================")
    
    # We define 3 distinct universes with wildly different physical constants
    universes = [
        {"name": "Our Universe", "Gravity": 9.8, "SpeedOfLight": 299792458},
        {"name": "Universe Alpha", "Gravity": 5000.0, "SpeedOfLight": 10},
        {"name": "Universe Omega", "Gravity": 0.001, "SpeedOfLight": 999999999999}
    ]
    
    # We ask a mathematical question: Does counting work the same way?
    # Fibonacci is derived strictly from: f(n) = f(n-1) + f(n-2)
    
    for u in universes:
        print(f"\n[{u['name']}]")
        print(f"Physics -> Gravity: {u['Gravity']}, Light: {u['SpeedOfLight']}")
        
        # Does the physical environment change the logic of addition? No.
        # Generating the first 10 Fibonacci numbers
        fib_sequence = generate_fibonacci(10)
        
        print(f"Fibonacci Sequence: {fib_sequence}")
        
    print("\n==================================================")
    print("MATHEMATICAL CONCLUSION:")
    print("The Fibonacci sequence is identical in every single universe.")
    print("Physics (Gravity, Light) can mutate and change, but pure Logic (1+1=2) is absolute.")
    print("Therefore, the Fibonacci sequence (and the Golden Ratio 137.5) exists in ALL universes.")
    print("==================================================")

if __name__ == "__main__":
    test_multiverse_math()
