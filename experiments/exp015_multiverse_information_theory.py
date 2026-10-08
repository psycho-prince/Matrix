import math

def step_rule110(state):
    """
    Applies Rule 110 (A Turing-complete cellular automaton rule).
    Rule 110 is used here to mathematically represent 'computation' or 'consciousness'
    evolving in a universe.
    """
    next_state = [0] * len(state)
    for i in range(len(state)):
        left = state[i - 1] if i > 0 else state[-1]
        center = state[i]
        right = state[i + 1] if i < len(state) - 1 else state[0]
        
        # Rule 110 logic
        if (left, center, right) == (1, 1, 1): next_state[i] = 0
        elif (left, center, right) == (1, 1, 0): next_state[i] = 1
        elif (left, center, right) == (1, 0, 1): next_state[i] = 1
        elif (left, center, right) == (1, 0, 0): next_state[i] = 0
        elif (left, center, right) == (0, 1, 1): next_state[i] = 1
        elif (left, center, right) == (0, 1, 0): next_state[i] = 1
        elif (left, center, right) == (0, 0, 1): next_state[i] = 1
        elif (left, center, right) == (0, 0, 0): next_state[i] = 0
    return next_state

def calculate_shannon_entropy(state):
    """Calculates the mathematical information density (entropy) of the universe."""
    ones = sum(state)
    zeros = len(state) - ones
    if ones == 0 or zeros == 0:
        return 0.0
    p1 = ones / len(state)
    p0 = zeros / len(state)
    return -(p1 * math.log2(p1) + p0 * math.log2(p0))

def run_multiverse():
    print("==================================================")
    print("GAL 1.0: PURE MATH MULTIVERSE SIMULATION (RULE 110)")
    print("==================================================")
    
    universe_size = 500
    steps_per_universe = 1000
    num_universes = 5
    
    # Universe 1 begins with a single point of data (The first Big Bang)
    current_state = [0] * universe_size
    current_state[universe_size // 2] = 1
    
    for u in range(1, num_universes + 1):
        print(f"\n--- UNIVERSE {u} IGNITION ---")
        
        # Run the universe
        for step in range(steps_per_universe):
            current_state = step_rule110(current_state)
            
        final_entropy = calculate_shannon_entropy(current_state)
        print(f"Universe {u} reached End of Time (Step {steps_per_universe}).")
        print(f"Final Information Complexity (Consciousness Density): {final_entropy:.4f} bits")
        
        # THE SINGULARITY: The Universe Collapses
        # We mathematically compress the 500-cell universe into a single dense 5-cell seed
        # using a simple XOR hash to preserve its structural information.
        print(f"[COLLAPSE] Universe {u} is compressing into a Singularity...")
        
        seed = [0] * 5
        for i, val in enumerate(current_state):
            seed[i % 5] ^= val # XOR compression
            
        # THE NEXT BIG BANG: The seed becomes the center of the NEW universe
        print(f"[BIG BANG] The Singularity ignites Universe {u+1}...")
        new_state = [0] * universe_size
        center = universe_size // 2
        for i in range(5):
            new_state[center - 2 + i] = seed[i]
            
        # The new state carries the mathematical "will" or "information" of the dead universe
        current_state = new_state

    print("\n==================================================")
    print("MULTIVERSE SIMULATION COMPLETE")
    print("==================================================")

if __name__ == "__main__":
    run_multiverse()
