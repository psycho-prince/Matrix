import json, glob, numpy as np, sys, os
from scipy import stats

data_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "../data/results")
raw_dir = os.path.join(data_dir, "raw") if not data_dir.endswith("raw") else data_dir

b_files = sorted(glob.glob(os.path.join(raw_dir, "mode_B-copy_seed_*.json")))
c_files = sorted(glob.glob(os.path.join(raw_dir, "mode_C-full_seed_*.json")))

if not b_files or not c_files:
    # fallback to local results/raw
    b_files = sorted(glob.glob("results/raw/mode_B-copy_seed_*.json"))
    c_files = sorted(glob.glob("results/raw/mode_C-full_seed_*.json"))

if not b_files or not c_files:
    print(f"Error: No data files found in {raw_dir} or results/raw/")
    sys.exit(1)

b_gen10 = []
c_gen10 = []

for bf, cf in zip(b_files, c_files):
    with open(bf) as f: b_data = json.load(f)
    with open(cf) as f: c_data = json.load(f)
    b_gen10.append(b_data["task_success_rates"][-1])
    c_gen10.append(c_data["task_success_rates"][-1])

b_gen10 = np.array(b_gen10)
c_gen10 = np.array(c_gen10)

t_stat, p_val = stats.ttest_rel(b_gen10, c_gen10)
diff = b_gen10 - c_gen10
mean_diff = np.mean(diff)
std_diff = np.std(diff, ddof=1)
n = len(diff)
se = std_diff / np.sqrt(n)
ci_lower = mean_diff - stats.t.ppf(0.975, n-1) * se
ci_upper = mean_diff + stats.t.ppf(0.975, n-1) * se
d_z = mean_diff / std_diff

print(f"N: {n}")
print(f"B mean: {np.mean(b_gen10):.4f}")
print(f"C mean: {np.mean(c_gen10):.4f}")
print(f"t-stat: {t_stat:.4f}")
print(f"p-value: {p_val:.4e}")
print(f"Mean diff: {mean_diff:.4f}")
print(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
print(f"Cohen's dz: {d_z:.4f}")
