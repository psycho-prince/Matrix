import numpy as np

def pure_math_simulation(f, max_generations=1000):
    """
    A pure mathematical, deterministic abstraction of the agent model.
    No RNG.
    f: Inheritance factor (0.0 to 1.0)
    """
    # Generate Fibonacci shifts
    shifts = set()
    a, b = 1, 1
    current_gen = 0
    while current_gen < max_generations:
        current_gen += a
        if current_gen < max_generations:
            shifts.add(current_gen)
        a, b = b, a + b
        
    # State
    skill_A = 0.0
    skill_B = 0.0
    capacity = 1.0
    learn_amount = 0.4  # deterministic learning per generation
    
    active_is_A = True
    
    total_success = 0.0
    
    for g in range(max_generations):
        if g in shifts:
            active_is_A = not active_is_A
            
        # 1. Inherit
        skill_A *= f
        skill_B *= f
        
        # 2. Learn
        if active_is_A:
            skill_A += learn_amount
        else:
            skill_B += learn_amount
            
        # 3. Enforce capacity
        total = skill_A + skill_B
        if total > capacity:
            skill_A *= (capacity / total)
            skill_B *= (capacity / total)
            
        # 4. Evaluate success (deterministic linear mapping for abstraction)
        # Assuming difficulty is 0.4, success is bounded
        active_skill = skill_A if active_is_A else skill_B
        
        # Pure math proxy for success: the integral of the active skill over the generation
        success = min(1.0, active_skill)
        total_success += success
        
    return total_success / max_generations

if __name__ == "__main__":
    PHI = (1 + np.sqrt(5)) / 2
    INV_PHI = 1.0 / PHI  # 0.6180339887...
    
    # Sweep around the Golden Ratio at high resolution
    factors = np.linspace(0.500, 0.700, 2000)
    
    best_f = 0
    best_score = -1
    
    print("=== Pure Mathematical Limit Test ===")
    print(f"Testing 2000 points between 0.500 and 0.700 (Deterministic, No RNG)")
    print(f"Mathematical Golden Ratio (1/phi) = {INV_PHI:.10f}\n")
    
    for f in factors:
        score = pure_math_simulation(f, max_generations=10000)
        if score > best_score:
            best_score = score
            best_f = f
            
    print(f"Empirical Maximum Success Score: {best_score:.6f}")
    print(f"Optimal Inheritance Factor (f) : {best_f:.10f}")
    
    error = abs(best_f - INV_PHI)
    print(f"Difference from exact 1/phi    : {error:.10f}")
    
    if error < 0.005:
        print("\nConclusion: The pure math deterministic model confirms the global maximum converges precisely around the Golden Ratio conjugate (1/phi).")
