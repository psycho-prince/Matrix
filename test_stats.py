import json, glob, numpy as np
from scipy import stats

b_files = sorted(glob.glob("definitive_results/raw/mode_B-copy_seed_*.json"))
c_files = sorted(glob.glob("definitive_results/raw/mode_C-full_seed_*.json"))

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
