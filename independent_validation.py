import json
import glob
import numpy as np

def verify_seeds(b_files, c_files):
    b_seeds = sorted([f.split('seed_')[1].split('.json')[0] for f in b_files])
    c_seeds = sorted([f.split('seed_')[1].split('.json')[0] for f in c_files])
    
    assert len(b_seeds) == 100, f"Expected 100 B-copy seeds, found {len(b_seeds)}"
    assert len(set(b_seeds)) == 100, "B-copy seeds are not unique"
    assert len(c_seeds) == 100, f"Expected 100 C-full seeds, found {len(c_seeds)}"
    assert len(set(c_seeds)) == 100, "C-full seeds are not unique"
    
    assert b_seeds == c_seeds, "Seed IDs do not match across paired comparisons"
    print("Seed integrity verified: 100 unique seeds with matching IDs.")

def permutation_test(b_gen10, c_gen10, n_permutations=100000):
    diff = b_gen10 - c_gen10
    observed_mean_diff = np.mean(diff)
    n = len(diff)
    
    # Sign-flip permutation test
    count_extreme = 0
    rng = np.random.default_rng(42)
    
    for _ in range(n_permutations):
        signs = rng.choice([-1, 1], size=n)
        permuted_diff = diff * signs
        permuted_mean = np.mean(permuted_diff)
        if permuted_mean >= observed_mean_diff:
            count_extreme += 1
            
    p_value = (count_extreme + 1) / (n_permutations + 1)
    print(f"Permutation test (N={n_permutations}):")
    print(f"Observed mean difference: {observed_mean_diff:.4f}")
    print(f"p-value (Monte Carlo plus-one): {p_value:.6e}")
    if count_extreme == 0:
        print(f"Zero extreme results observed. p_MC = 1/{n_permutations+1}")

if __name__ == "__main__":
    b_files = sorted(glob.glob("results/raw/mode_B-copy_seed_*.json"))
    c_files = sorted(glob.glob("results/raw/mode_C-full_seed_*.json"))
    
    if not b_files or not c_files:
        print("Run ./reproduce.sh first to generate data.")
        exit(1)
        
    verify_seeds(b_files, c_files)
    
    b_gen10 = []
    c_gen10 = []
    
    for bf, cf in zip(b_files, c_files):
        with open(bf) as f: b_data = json.load(f)
        with open(cf) as f: c_data = json.load(f)
        b_gen10.append(b_data["task_success_rates"][-1])
        c_gen10.append(c_data["task_success_rates"][-1])
        
    b_gen10 = np.array(b_gen10)
    c_gen10 = np.array(c_gen10)
    
    permutation_test(b_gen10, c_gen10)
