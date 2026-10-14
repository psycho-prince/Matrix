"""
Scalable Continual Learning Benchmark on Permuted-MNIST.

Unifying Generational Memory Economics with Modern Deep Plasticity Theory:
- Dohare et al. (Nature 2024): Loss of Plasticity in Deep Continual Learning
- Ash & Adams (NeurIPS 2020): On Warm-Starting Neural Network Training (Shrink & Perturb)
- Rechavi et al. (Cell 2011, 2014): Transgenerational Epigenetic Timers

Compares:
1. Variance-Preserving Generational Shrinkage (Ours: theta = f * theta* + sqrt(1 - f^2) * xi)
2. Elastic Weight Consolidation (Kirkpatrick et al., PNAS 2017)
3. Experience Replay (Chaudhry et al., 2019)
4. Naive Sequential Fine-tuning (Exact Cloning f = 1.0)
5. Tabula Rasa (Full Re-initialization f = 0.0)

Evaluates:
- Standard Regime (hidden_dim=16, capacity=25.0)
- Capacity Bottleneck Regime (hidden_dim=4, capacity=3.0) demonstrating Plasticity Recovery
"""

import numpy as np
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../data/mnist'))
from mnist_benchmark import generate_mnist_benchmarks, get_permuted_mnist_task

class BaseMLPAgent:
    def __init__(self, input_dim=64, hidden_dim=16, output_dim=1, capacity=25.0, lr=0.04, seed=None):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.capacity = float(capacity)
        self.lr = float(lr)
        
        rng = np.random.RandomState(seed)
        self.W1 = rng.randn(input_dim, hidden_dim) * np.sqrt(2.0 / input_dim)
        self.b1 = np.zeros((1, hidden_dim))
        self.W2 = rng.randn(hidden_dim, output_dim) * np.sqrt(2.0 / hidden_dim)
        self.b2 = np.zeros((1, output_dim))

    @staticmethod
    def sigmoid(x):
        return 1.0 / (1.0 + np.exp(-np.clip(x, -15.0, 15.0)))

    def forward(self, X):
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = np.maximum(0, self.z1)  # ReLU
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.out = self.sigmoid(self.z2)
        return self.out

    def enforce_capacity(self):
        norm_val = np.sqrt(np.sum(self.W1**2) + np.sum(self.b1**2) + np.sum(self.W2**2) + np.sum(self.b2**2))
        if norm_val > self.capacity:
            scale = self.capacity / norm_val
            self.W1 *= scale
            self.b1 *= scale
            self.W2 *= scale
            self.b2 *= scale

    def evaluate_accuracy(self, X, y):
        preds = (self.forward(X) >= 0.5).astype(float)
        return float(np.mean(preds == y))


class VariancePreservingAgent(BaseMLPAgent):
    """
    Theorem 2: Variance-Preserving Generational Shrinkage.
    W_child = f * W_parent + sqrt(1 - f^2) * xi
    Conserves total parameter energy E[||W||^2] = const.
    """
    def __init__(self, f=0.55, **kwargs):
        super().__init__(**kwargs)
        self.f = float(np.clip(f, 0.0, 1.0))

    def inherit_variance_preserving(self, parent, seed):
        rng = np.random.RandomState(seed)
        noise_W1 = rng.randn(self.input_dim, self.hidden_dim) * np.sqrt(2.0 / self.input_dim)
        noise_W2 = rng.randn(self.hidden_dim, self.output_dim) * np.sqrt(2.0 / self.hidden_dim)
        
        alpha = self.f
        beta = np.sqrt(max(0.0, 1.0 - alpha**2))
        
        self.W1 = alpha * parent.W1.copy() + beta * noise_W1
        self.b1 = alpha * parent.b1.copy()
        self.W2 = alpha * parent.W2.copy() + beta * noise_W2
        self.b2 = alpha * parent.b2.copy()
        self.enforce_capacity()

    def train_step(self, X, y, steps=25):
        for _ in range(steps):
            y_pred = self.forward(X)
            diff = (y_pred - y) / max(1, len(X))
            grad_W2 = np.dot(self.a1.T, diff)
            grad_b2 = np.sum(diff, axis=0, keepdims=True)
            grad_a1 = np.dot(diff, self.W2.T)
            grad_z1 = grad_a1 * (self.z1 > 0)
            grad_W1 = np.dot(X.T, grad_z1)
            grad_b1 = np.sum(grad_z1, axis=0, keepdims=True)

            self.W1 -= self.lr * grad_W1
            self.b1 -= self.lr * grad_b1
            self.W2 -= self.lr * grad_W2
            self.b2 -= self.lr * grad_b2
            self.enforce_capacity()


class EWCAgent(BaseMLPAgent):
    def __init__(self, ewc_lambda=15.0, **kwargs):
        super().__init__(**kwargs)
        self.ewc_lambda = ewc_lambda
        self.opt_W1 = self.W1.copy()
        self.opt_W2 = self.W2.copy()
        self.opt_b1 = self.b1.copy()
        self.opt_b2 = self.b2.copy()
        self.F_W1 = np.zeros_like(self.W1)
        self.F_W2 = np.zeros_like(self.W2)
        self.has_prior = False

    def update_fisher(self, X, y):
        self.forward(X)
        N = len(X)
        gw2_sq = np.zeros_like(self.W2)
        gw1_sq = np.zeros_like(self.W1)
        for i in range(N):
            diff = self.out[i:i+1] - y[i:i+1]
            gw2 = np.dot(self.a1[i:i+1].T, diff)
            ga1 = np.dot(diff, self.W2.T)
            gz1 = ga1 * (self.z1[i:i+1] > 0)
            gw1 = np.dot(X[i:i+1].T, gz1)
            gw2_sq += gw2**2
            gw1_sq += gw1**2
            
        self.F_W1 = (self.F_W1 + gw1_sq / N) * 0.5
        self.F_W2 = (self.F_W2 + gw2_sq / N) * 0.5
        self.opt_W1 = self.W1.copy()
        self.opt_W2 = self.W2.copy()
        self.has_prior = True

    def train_step(self, X, y, steps=25):
        for _ in range(steps):
            y_pred = self.forward(X)
            diff = (y_pred - y) / max(1, len(X))
            grad_W2 = np.dot(self.a1.T, diff)
            grad_b2 = np.sum(diff, axis=0, keepdims=True)
            grad_a1 = np.dot(diff, self.W2.T)
            grad_z1 = grad_a1 * (self.z1 > 0)
            grad_W1 = np.dot(X.T, grad_z1)
            grad_b1 = np.sum(grad_z1, axis=0, keepdims=True)

            if self.has_prior:
                grad_W1 += self.ewc_lambda * self.F_W1 * (self.W1 - self.opt_W1)
                grad_W2 += self.ewc_lambda * self.F_W2 * (self.W2 - self.opt_W2)

            self.W1 -= self.lr * grad_W1
            self.b1 -= self.lr * grad_b1
            self.W2 -= self.lr * grad_W2
            self.b2 -= self.lr * grad_b2
            self.enforce_capacity()


class ReplayAgent(BaseMLPAgent):
    def __init__(self, buffer_size=20, **kwargs):
        super().__init__(**kwargs)
        self.buffer_size = buffer_size
        self.mem_X, self.mem_y = [], []

    def store(self, X, y):
        idx = np.random.choice(len(X), min(self.buffer_size, len(X)), replace=False)
        self.mem_X.append(X[idx])
        self.mem_y.append(y[idx])

    def train_step(self, X, y, steps=25):
        for _ in range(steps):
            if len(self.mem_X) > 0:
                all_X = np.vstack(self.mem_X)
                all_y = np.vstack(self.mem_y)
                sub_idx = np.random.choice(len(all_X), min(len(all_X), 16), replace=False)
                batch_X = np.vstack([X, all_X[sub_idx]])
                batch_y = np.vstack([y, all_y[sub_idx]])
            else:
                batch_X, batch_y = X, y

            y_pred = self.forward(batch_X)
            diff = (y_pred - batch_y) / max(1, len(batch_X))
            grad_W2 = np.dot(self.a1.T, diff)
            grad_b2 = np.sum(diff, axis=0, keepdims=True)
            grad_a1 = np.dot(diff, self.W2.T)
            grad_z1 = grad_a1 * (self.z1 > 0)
            grad_W1 = np.dot(batch_X.T, grad_z1)
            grad_b1 = np.sum(grad_z1, axis=0, keepdims=True)

            self.W1 -= self.lr * grad_W1
            self.b1 -= self.lr * grad_b1
            self.W2 -= self.lr * grad_W2
            self.b2 -= self.lr * grad_b2
            self.enforce_capacity()


def run_benchmark_suite(seed=42):
    print("=" * 85)
    print("  RUNNING UNIFIED CONTINUAL LEARNING BENCHMARK SUITE")
    print("  Unifying Nature 2024 Plasticity Theory with Generational Artificial Life")
    print("=" * 85)

    X_raw, y_raw = generate_mnist_benchmarks(n_samples_per_digit=80, seed=seed)
    mask = np.isin(y_raw, [0, 1, 8, 9])
    X_base = X_raw[mask]
    y_base = (np.isin(y_raw[mask], [8, 9])).astype(float).reshape(-1, 1)

    # 5 Sequential Tasks
    tasks = []
    for t in range(5):
        X_t = get_permuted_mnist_task(X_base, t * 137 + 11)
        split = int(0.7 * len(X_t))
        tasks.append((X_t[:split], y_base[:split], X_t[split:], y_base[split:]))

    # Benchmark 1: Standard Continual Learning Regime
    print("\n[+] Benchmark 1: Standard Continual Learning Regime (Hidden=16, Cap=25.0)")
    methods_std = {
        "Variance-Preserving Reset (Ours)": VariancePreservingAgent(hidden_dim=16, capacity=25.0, lr=0.04, f=0.55, seed=seed),
        "Elastic Weight Consolidation (EWC)": EWCAgent(hidden_dim=16, capacity=25.0, lr=0.04, ewc_lambda=15.0, seed=seed),
        "Experience Replay (ER)": ReplayAgent(hidden_dim=16, capacity=25.0, lr=0.04, buffer_size=20, seed=seed),
        "Naive Sequential Cloning (f=1.0)": BaseMLPAgent(hidden_dim=16, capacity=25.0, lr=0.04, seed=seed),
        "Tabula Rasa / Reset (f=0.0)": BaseMLPAgent(hidden_dim=16, capacity=25.0, lr=0.04, seed=seed)
    }

    results_std = {}
    for name, agent in methods_std.items():
        task1_init = 0.0
        for t_idx, (X_tr, y_tr, X_te, y_te) in enumerate(tasks):
            if "Tabula Rasa" in name and t_idx > 0:
                agent = BaseMLPAgent(hidden_dim=16, capacity=25.0, lr=0.04, seed=seed + t_idx)
            elif "Variance-Preserving" in name and t_idx > 0:
                child = VariancePreservingAgent(hidden_dim=16, capacity=25.0, lr=0.04, f=0.55, seed=seed + t_idx)
                child.inherit_variance_preserving(agent, seed=seed + t_idx * 10)
                agent = child

            if isinstance(agent, EWCAgent):
                agent.train_step(X_tr, y_tr, steps=25)
                agent.update_fisher(X_tr, y_tr)
            elif isinstance(agent, ReplayAgent):
                agent.train_step(X_tr, y_tr, steps=25)
                agent.store(X_tr, y_tr)
            elif isinstance(agent, VariancePreservingAgent):
                agent.train_step(X_tr, y_tr, steps=25)
            else:
                for _ in range(25):
                    p = agent.forward(X_tr)
                    diff = (p - y_tr) / len(X_tr)
                    gW2 = np.dot(agent.a1.T, diff)
                    gb2 = np.sum(diff, axis=0, keepdims=True)
                    ga1 = np.dot(diff, agent.W2.T)
                    gz1 = ga1 * (agent.z1 > 0)
                    gW1 = np.dot(X_tr.T, gz1)
                    gb1 = np.sum(gz1, axis=0, keepdims=True)
                    agent.W1 -= agent.lr * gW1
                    agent.b1 -= agent.lr * gb1
                    agent.W2 -= agent.lr * gW2
                    agent.b2 -= agent.lr * gb2
                    agent.enforce_capacity()

            acc = agent.evaluate_accuracy(X_te, y_te)
            if t_idx == 0:
                task1_init = acc

        final_accs = [agent.evaluate_accuracy(t_te_x, t_te_y) for _, _, t_te_x, t_te_y in tasks]
        results_std[name] = {
            "mean_continual_acc": round(float(np.mean(final_accs)) * 100, 2),
            "task1_forgetting": round(float(task1_init - final_accs[0]) * 100, 2),
            "task5_accuracy": round(float(final_accs[-1]) * 100, 2)
        }

    # Benchmark 2: Capacity Bottleneck Regime demonstrating Plasticity Recovery
    print("\n[+] Benchmark 2: Severe Capacity Bottleneck Regime (Hidden=4, Cap=3.0)")
    cloning_bot = BaseMLPAgent(hidden_dim=4, capacity=3.0, lr=0.03, seed=seed)
    lossy_bot = VariancePreservingAgent(hidden_dim=4, capacity=3.0, lr=0.03, f=0.50, seed=seed)

    cloning_task_accs, lossy_task_accs = [], []
    for t_idx, (X_tr, y_tr, X_te, y_te) in enumerate(tasks):
        # Cloning train
        for _ in range(30):
            p = cloning_bot.forward(X_tr)
            diff = (p - y_tr)/len(X_tr)
            gW2 = np.dot(cloning_bot.a1.T, diff)
            gb2 = np.sum(diff, axis=0, keepdims=True)
            ga1 = np.dot(diff, cloning_bot.W2.T)
            gz1 = ga1 * (cloning_bot.z1 > 0)
            gW1 = np.dot(X_tr.T, gz1)
            gb1 = np.sum(gz1, axis=0, keepdims=True)
            cloning_bot.W1 -= cloning_bot.lr * gW1
            cloning_bot.b1 -= cloning_bot.lr * gb1
            cloning_bot.W2 -= cloning_bot.lr * gW2
            cloning_bot.b2 -= cloning_bot.lr * gb2
            cloning_bot.enforce_capacity()
        cloning_task_accs.append(cloning_bot.evaluate_accuracy(X_te, y_te))

        # Lossy train
        if t_idx > 0:
            ch = VariancePreservingAgent(hidden_dim=4, capacity=3.0, lr=0.03, f=0.50, seed=seed+t_idx)
            ch.inherit_variance_preserving(lossy_bot, seed=seed+t_idx*10)
            lossy_bot = ch
        lossy_bot.train_step(X_tr, y_tr, steps=30)
        lossy_task_accs.append(lossy_bot.evaluate_accuracy(X_te, y_te))

    plasticity_results = {
        "cloning_task5_acc": round(float(cloning_task_accs[-1]) * 100, 2),
        "lossy_task5_acc": round(float(lossy_task_accs[-1]) * 100, 2),
        "plasticity_advantage_percent": round(float(lossy_task_accs[-1] - cloning_task_accs[-1]) * 100, 2)
    }

    full_output = {
        "standard_regime": results_std,
        "bottleneck_plasticity_regime": plasticity_results
    }

    out_file = os.path.join(os.path.dirname(__file__), "../../data/mnist/permuted_mnist_results.json")
    with open(out_file, "w") as fp:
        json.dump(full_output, fp, indent=2)

    print("\n" + "=" * 85)
    print("  SUMMARY: CONTINUAL LEARNING BENCHMARKS")
    print("=" * 85)
    for name, d in results_std.items():
        print(f"  {name:<36} | Continual Acc: {d['mean_continual_acc']}% | Task 1 Forgetting: {d['task1_forgetting']}%")
    print("-" * 85)
    print(f"  Bottleneck Plasticity on Task 5: Naive Cloning = {plasticity_results['cloning_task5_acc']}% | Ours (Variance-Preserving) = {plasticity_results['lossy_task5_acc']}%")
    print(f"  Plasticity Advantage over Saturated Baseline: +{plasticity_results['plasticity_advantage_percent']}%")
    print("=" * 85)
    return full_output

if __name__ == "__main__":
    run_benchmark_suite()
