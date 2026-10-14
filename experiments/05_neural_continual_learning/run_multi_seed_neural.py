import numpy as np
import json
import os
import sys

# Import neural agent class
from neural_continual_agent import NeuralAgent, generate_task_data

def run_neural_sweep(shift_frequencies=[2, 5, 10, 25, 50], n_seeds=5, generations=150, pop_size=40):
    print("=" * 80)
    print("  RUNNING MULTI-SEED NEURAL CONTINUAL LEARNING SWEEP (Paper 4)")
    print("=" * 80)
    
    summary = {}

    for freq in shift_frequencies:
        print(f"\n[+] Testing Shift Frequency: Every {freq} generations ({n_seeds} seeds)...")
        f_list, lr_list, cap_list, acc_list = [], [], [], []

        for s in range(n_seeds):
            rng = np.random.RandomState(42 + s * 100 + freq)
            population = [
                NeuralAgent(capacity=rng.uniform(15.0, 40.0), f=rng.uniform(0.1, 0.9), lr=rng.uniform(0.01, 0.12))
                for _ in range(pop_size)
            ]
            current_task = 'A'

            for g in range(generations):
                if g > 0 and g % freq == 0:
                    current_task = 'B' if current_task == 'A' else 'A'

                X_train, y_train = generate_task_data(current_task, n_samples=60, seed=g + s*500)
                X_test, y_test = generate_task_data(current_task, n_samples=40, seed=g + 1000 + s*500)

                evaluated = []
                for agent in population:
                    agent.train_step(X_train, y_train, steps=6)
                    acc = agent.evaluate_accuracy(X_test, y_test)
                    time_penalty = agent.lr * 1.5
                    cap_cost = (agent.capacity / 100.0) * 0.15
                    fitness = max(0.0, acc - time_penalty - cap_cost)
                    evaluated.append((fitness, agent, acc))

                evaluated.sort(key=lambda item: item[0], reverse=True)
                survivors = [item[1] for item in evaluated[:pop_size // 2]]

                # Next gen
                next_pop = []
                while len(next_pop) < pop_size:
                    parent = survivors[rng.randint(len(survivors))]
                    child_f = float(np.clip(parent.f + rng.normal(0, 0.05), 0.0, 1.0))
                    child_lr = float(np.clip(parent.lr + rng.normal(0, 0.01), 0.005, 0.25))
                    child_cap = float(np.clip(parent.capacity + rng.normal(0, 2.0), 10.0, 100.0))
                    child = NeuralAgent(capacity=child_cap, f=child_f, lr=child_lr)
                    child.inherit_from(parent)
                    next_pop.append(child)
                population = next_pop

            f_final = np.mean([a.f for a in survivors])
            lr_final = np.mean([a.lr for a in survivors])
            cap_final = np.mean([a.capacity for a in survivors])
            acc_final = np.mean([item[2] for item in evaluated[:pop_size // 2]])

            f_list.append(f_final)
            lr_list.append(lr_final)
            cap_list.append(cap_final)
            acc_list.append(acc_final)

        summary[freq] = {
            "f_mean": float(np.mean(f_list)), "f_std": float(np.std(f_list, ddof=1)),
            "lr_mean": float(np.mean(lr_list)), "lr_std": float(np.std(lr_list, ddof=1)),
            "cap_mean": float(np.mean(cap_list)), "cap_std": float(np.std(cap_list, ddof=1)),
            "acc_mean": float(np.mean(acc_list)), "acc_std": float(np.std(acc_list, ddof=1))
        }
        print(f"    Retention (f): {summary[freq]['f_mean']:.3f} ± {summary[freq]['f_std']:.3f} | Cap: {summary[freq]['cap_mean']:.1f} | Acc: {summary[freq]['acc_mean']:.3f}")

    save_path = os.path.join(os.path.dirname(__file__), "../../data/neural_continual_sweep.json")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w") as fp:
        json.dump(summary, fp, indent=2)
    print(f"\n[+] Neural sweep saved to {save_path}")
    return summary

if __name__ == "__main__":
    run_neural_sweep()
