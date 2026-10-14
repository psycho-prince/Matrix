"""
Continual Learning Benchmark on Permuted-MNIST.

Compares 5 paradigms on a 5-task sequential Permuted-MNIST benchmark:
1. Generational Memory Economics (Adaptive Lossy Retention f + evolvable capacity)
2. Elastic Weight Consolidation (Kirkpatrick et al., PNAS 2017)
3. Experience Replay (Buffer of historical exemplars)
4. Naive Continual Learning / Exact Cloning (f = 1.0, sequential fine-tuning)
5. Tabula Rasa / Full Amnesia (f = 0.0, re-initialization per task)

Evaluates:
- Average Continual Accuracy across all learned tasks
- Catastrophic Forgetting (Retention of Task 1 after Task 5)
- Forward Plasticity (Immediate learning speed on new tasks)
"""

import numpy as np
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../data/mnist'))
from mnist_benchmark import generate_mnist_benchmarks, get_permuted_mnist_task

class BaseMLPAgent:
    def __init__(self, input_dim=64, hidden_dim=16, output_dim=1, capacity=30.0, lr=0.03, seed=None):
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


class EWCAgent(BaseMLPAgent):
    def __init__(self, input_dim=64, hidden_dim=16, output_dim=1, ewc_lambda=15.0, **kwargs):
        super().__init__(input_dim, hidden_dim, output_dim, **kwargs)
        self.ewc_lambda = ewc_lambda
        self.opt_W1 = self.W1.copy()
        self.opt_b1 = self.b1.copy()
        self.opt_W2 = self.W2.copy()
        self.opt_b2 = self.b2.copy()
        self.F_W1 = np.zeros_like(self.W1)
        self.F_b1 = np.zeros_like(self.b1)
        self.F_W2 = np.zeros_like(self.W2)
        self.F_b2 = np.zeros_like(self.b2)
        self.has_prior = False

    def update_fisher(self, X, y):
        # Accumulate diagonal empirical Fisher information
        self.forward(X)
        N = len(X)
        g_w2_sq = np.zeros_like(self.W2)
        g_w1_sq = np.zeros_like(self.W1)
        
        for i in range(N):
            diff = self.out[i:i+1] - y[i:i+1]
            gw2 = np.dot(self.a1[i:i+1].T, diff)
            ga1 = np.dot(diff, self.W2.T)
            gz1 = ga1 * (self.z1[i:i+1] > 0)
            gw1 = np.dot(X[i:i+1].T, gz1)
            g_w2_sq += gw2**2
            g_w1_sq += gw1**2
            
        self.F_W1 = (self.F_W1 + g_w1_sq / N) * 0.5
        self.F_W2 = (self.F_W2 + g_w2_sq / N) * 0.5
        self.opt_W1 = self.W1.copy()
        self.opt_W2 = self.W2.copy()
        self.opt_b1 = self.b1.copy()
        self.opt_b2 = self.b2.copy()
        self.has_prior = True

    def train_step(self, X, y, steps=10):
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
    def __init__(self, buffer_size_per_task=20, **kwargs):
        super().__init__(**kwargs)
        self.buffer_size = buffer_size_per_task
        self.memory_X = []
        self.memory_y = []

    def store_exemplars(self, X, y):
        idx = np.random.choice(len(X), min(self.buffer_size, len(X)), replace=False)
        self.memory_X.append(X[idx])
        self.memory_y.append(y[idx])

    def train_step(self, X, y, steps=10):
        for _ in range(steps):
            if len(self.memory_X) > 0:
                mem_X_all = np.vstack(self.memory_X)
                mem_y_all = np.vstack(self.memory_y)
                mem_idx = np.random.choice(len(mem_X_all), min(len(mem_X_all), 16), replace=False)
                batch_X = np.vstack([X, mem_X_all[mem_idx]])
                batch_y = np.vstack([y, mem_y_all[mem_idx]])
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


class AdaptiveLossyAgent(BaseMLPAgent):
    def __init__(self, f=0.5, **kwargs):
        super().__init__(**kwargs)
        self.f = float(np.clip(f, 0.0, 1.0))

    def train_step(self, X, y, steps=10):
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

    def generational_reset(self, parent):
        # Lossy inheritance: scales parental weight structure by retention factor f
        self.W1 = parent.W1.copy() * self.f
        self.b1 = parent.b1.copy() * self.f
        self.W2 = parent.W2.copy() * self.f
        self.b2 = parent.b2.copy() * self.f
        self.enforce_capacity()


def run_comprehensive_continual_benchmark(n_tasks=5, seed=42):
    print("=" * 80)
    print("  RIGOROUS CONTINUAL LEARNING BENCHMARK ON PERMUTED-MNIST")
    print("  Evaluating: Memory Economics vs EWC vs Replay vs Cloning vs Tabula Rasa")
    print("=" * 80)

    X_raw, y_raw = generate_mnist_benchmarks(n_samples_per_digit=80, seed=seed)
    mask = np.isin(y_raw, [0, 1, 8, 9])
    X_base = X_raw[mask]
    y_base = (np.isin(y_raw[mask], [8, 9])).astype(float).reshape(-1, 1)

    tasks = []
    for t in range(n_tasks):
        X_task = get_permuted_mnist_task(X_base, permutation_seed=t * 137 + 11)
        split = int(0.7 * len(X_task))
        tasks.append((X_task[:split], y_base[:split], X_task[split:], y_base[split:]))

    # Evaluate all 5 Methods
    methods = {
        "Adaptive Lossy (Ours, f=0.45)": AdaptiveLossyAgent(hidden_dim=16, capacity=25.0, lr=0.04, f=0.45, seed=seed),
        "Elastic Weight Consolidation (EWC)": EWCAgent(hidden_dim=16, capacity=25.0, lr=0.04, ewc_lambda=10.0, seed=seed),
        "Experience Replay (ER)": ReplayAgent(hidden_dim=16, capacity=25.0, lr=0.04, buffer_size_per_task=20, seed=seed),
        "Naive Sequential Cloning (f=1.0)": BaseMLPAgent(hidden_dim=16, capacity=25.0, lr=0.04, seed=seed),
        "Tabula Rasa / Reset (f=0.0)": BaseMLPAgent(hidden_dim=16, capacity=25.0, lr=0.04, seed=seed)
    }

    results = {}

    for name, agent in methods.items():
        print(f"\n[+] Running Method: {name}")
        task1_initial_acc = 0.0

        for t_idx, (X_tr, y_tr, X_te, y_te) in enumerate(tasks):
            if name == "Tabula Rasa / Reset (f=0.0)" and t_idx > 0:
                agent = BaseMLPAgent(hidden_dim=16, capacity=25.0, lr=0.04, seed=seed + t_idx)
            elif "Adaptive Lossy" in name and t_idx > 0:
                # Generational transition between tasks
                child = AdaptiveLossyAgent(hidden_dim=16, capacity=25.0, lr=0.04, f=0.45, seed=seed + t_idx)
                child.generational_reset(agent)
                agent = child

            # Train on current task
            if isinstance(agent, EWCAgent):
                agent.train_step(X_tr, y_tr, steps=25)
                agent.update_fisher(X_tr, y_tr)
            elif isinstance(agent, ReplayAgent):
                agent.train_step(X_tr, y_tr, steps=25)
                agent.store_exemplars(X_tr, y_tr)
            else:
                for _ in range(25):
                    # Standard train step
                    y_pred = agent.forward(X_tr)
                    diff = (y_pred - y_tr) / len(X_tr)
                    grad_W2 = np.dot(agent.a1.T, diff)
                    grad_b2 = np.sum(diff, axis=0, keepdims=True)
                    grad_a1 = np.dot(diff, agent.W2.T)
                    grad_z1 = grad_a1 * (agent.z1 > 0)
                    grad_W1 = np.dot(X_tr.T, grad_z1)
                    grad_b1 = np.sum(grad_z1, axis=0, keepdims=True)
                    agent.W1 -= agent.lr * grad_W1
                    agent.b1 -= agent.lr * grad_b1
                    agent.W2 -= agent.lr * grad_W2
                    agent.b2 -= agent.lr * grad_b2
                    agent.enforce_capacity()

            curr_acc = agent.evaluate_accuracy(X_te, y_te)
            if t_idx == 0:
                task1_initial_acc = curr_acc
            print(f"    Task {t_idx+1} Immediate Test Acc: {curr_acc*100:.1f}%")

        # Evaluate final performance across ALL 5 tasks
        final_task_accuracies = []
        for t_idx, (_, _, X_te, y_te) in enumerate(tasks):
            final_task_accuracies.append(agent.evaluate_accuracy(X_te, y_te))

        mean_continual_acc = float(np.mean(final_task_accuracies))
        task1_final_acc = float(final_task_accuracies[0])
        forgetting = float(task1_initial_acc - task1_final_acc)
        bwt = float(np.mean([final_task_accuracies[j] - 0.85 for j in range(len(tasks)-1)])) # Backward transfer approx

        results[name] = {
            "mean_continual_accuracy": round(mean_continual_acc * 100, 2),
            "task1_initial_accuracy": round(task1_initial_acc * 100, 2),
            "task1_final_accuracy": round(task1_final_acc * 100, 2),
            "catastrophic_forgetting": round(forgetting * 100, 2),
            "task_accuracies": [round(a * 100, 1) for a in final_task_accuracies]
        }
        print(f"    --> Final Mean Acc Across All 5 Tasks: {results[name]['mean_continual_accuracy']}%")
        print(f"    --> Task 1 Forgetting Drop: {results[name]['catastrophic_forgetting']}%")

    out_file = os.path.join(os.path.dirname(__file__), "../../data/mnist/permuted_mnist_results.json")
    with open(out_file, "w") as fp:
        json.dump(results, fp, indent=2)

    print("\n" + "=" * 80)
    print("  SUMMARY BENCHMARK COMPARISON (5-Task Permuted-MNIST)")
    print("=" * 80)
    print(f"{'Method':<36} | {'Mean Acc (%)':<14} | {'Task 1 Forgetting (%)':<22}")
    print("-" * 80)
    for name, d in results.items():
        print(f"{name:<36} | {d['mean_continual_accuracy']:<14} | {d['catastrophic_forgetting']:<22}")
    print("=" * 80)
    print(f"Saved results to {out_file}")
    return results

if __name__ == "__main__":
    run_comprehensive_continual_benchmark()
