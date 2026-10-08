def run_true_math():
    print("==================================================")
    print("PURE MATH: THE GOLDEN ANGLE & LIGHT")
    print("==================================================")
    
    # 1. FIBONACCI & THE GOLDEN RATIO
    print("[TEST 1: The Fibonacci Sequence]")
    # Generate Fibonacci sequence
    fib = [1, 1]
    for i in range(40):
        fib.append(fib[-1] + fib[-2])
        
    print(f"Fibonacci sequence (last 2): {fib[-2]}, {fib[-1]}")
    
    # Calculate Golden Ratio (Phi)
    # The ratio of consecutive Fibonacci numbers converges to Phi
    phi = fib[-1] / fib[-2]
    print(f"Calculated Golden Ratio (Phi): {phi:.10f}")
    
    # Calculate the Golden Angle
    # A full circle divided by Phi squared
    golden_angle = 360 / (phi ** 2)
    print(f"Calculated Golden Angle: {golden_angle:.10f} degrees\n")
    
    if abs(golden_angle - 137.5) < 0.1:
        print("-> MATH VERIFIED: The number 137.5 mathematically emerges directly from the Fibonacci sequence.")
    
    # 2. THE SPEED OF LIGHT & 137 (Fine-Structure Constant)
    print("\n[TEST 2: The Speed of Light (c)]")
    print("The user asked about sunlight. The speed of light (c) is exactly 299,792,458 m/s.")
    print("In physics, 137 emerges from the Fine-Structure Constant equation:")
    print("Alpha = (e^2) / (4 * pi * epsilon_0 * hbar * c)")
    print("Notice that 'c' (the speed of light) is directly in the denominator.")
    
    # We can plug in the real-world constants
    e = 1.602176634e-19        # Elementary charge (Coulombs)
    epsilon_0 = 8.8541878128e-12 # Vacuum permittivity
    hbar = 1.054571817e-34     # Reduced Planck constant
    c = 299792458              # Speed of light
    pi = 3.141592653589793
    
    # Calculate Alpha
    alpha = (e**2) / (4 * pi * epsilon_0 * hbar * c)
    inverse_alpha = 1 / alpha
    
    print(f"\nPlugging the speed of light into the equation gives the inverse Fine-Structure Constant:")
    print(f"Calculated 1/Alpha = {inverse_alpha:.6f}")
    
    print("\n==================================================")
    print("SIMULATION COMPLETE")
    print("==================================================")

if __name__ == "__main__":
    run_true_math()
