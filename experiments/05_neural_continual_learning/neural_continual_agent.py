"""
Neural Continual Learning under Generational Memory Economics (Paper 4 Prototype).

Agents are parameterized by small neural network weights (MLP) performing nonlinear classification
under non-stationary environmental task distributions (Task A: circle vs Task B: spiral/xor).
Offspring inherit parental network weights scaled by retention trait f, subject to parameter budget (capacity)
and gradient learning speed (learning rate lr) under metabolic costs.
"""

import numpy as np
import json
import os

class NeuralAgent:
    def __init__(self, input_dim=2, hidden_dim=8, output_dim=1, capacity=30, f=0.5, lr=0.05):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        
        # Evolvable traits
        self.f = float(np.clip(f, 0.0, 1.0))
        self.lr = float(np.clip(lr, 0.001, 0.3))
        self.capacity = float(np.clip(capacity, 10.0, 100.0))
        
        # Neural weights
        self.W1 = np.random.randn(input_dim, hidden_dim) * 0.2
        self.b1 = np.zeros((1, hidden_dim))
        self.W2 = np.random.randn(hidden_dim, output_dim) * 0.2
        self.b2 = np.zeros((1, output_dim))

    @staticmethod
    def sigmoid(x):
        return 1.0 / (1.0 + np.exp(-np.clip(x, -15.0, 15.0)))

    def forward(self, X):
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = np.tanh(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.out = self.sigmoid(self.z2)
        return self.out

    def enforce_capacity(self):
        # L2 norm of weights bounded by capacity budget
        total_norm = np.sqrt(np.sum(self.W1**2) + np.sum(self.b1**2) + np.sum(self.W2**2) + np.sum(self.b2**2))
        if total_norm > self.capacity:
            scale = self.capacity / total_norm
            self.W1 *= scale
            self.b1 *= scale
            self.W2 *= scale
            self.b2 *= scale

    def train_step(self, X, y, steps=5):
        """Standard backprop gradient step during agent lifetime."""
        for _ in range(steps):
            y_pred = self.forward(X)
            # Binary Cross Entropy gradient
            loss_grad = (y_pred - y) / max(1, len(X))
            
            grad_W2 = np.dot(self.a1.T, loss_grad)
            grad_b2 = np.sum(loss_grad, axis=0, keepdims=True)
            
            grad_a1 = np.dot(loss_grad, self.W2.T)
            grad_z1 = grad_a1 * (1.0 - self.a1**2)
            grad_W1 = np.dot(X.T, grad_z1)
            grad_b1 = np.sum(grad_z1, axis=0, keepdims=True)
            
            self.W1 -= self.lr * grad_W1
            self.b1 -= self.lr * grad_b1
            self.W2 -= self.lr * grad_W2
            self.b2 -= self.lr * grad_b2
            self.enforce_capacity()

    def evaluate_accuracy(self, X, y):
        preds = (self.forward(X) >= 0.5).astype(float)
        return np.mean(preds == y)

    def inherit_from(self, parent):
        """Lamarckian weight transfer scaled by retention trait f."""
        self.W1 = parent.W1.copy() * self.f
        self.b1 = parent.b1.copy() * self.f
        self.W2 = parent.W2.copy() * self.f
        self.b2 = parent.b2.copy() * self.f
        self.enforce_capacity()


def generate_task_data(task_type, n_samples=80, seed=42):
    rng = np.random.RandomState(seed)
    X = rng.uniform(-1.0, 1.0, (n_samples, 2))
    if task_type == 'A':
        # Concentric circle decision boundary
        y = (np.sum(X**2, axis=1, keepdims=True) < 0.36).astype(float)
    else:
        # XOR quadrant boundary
        y = ((X[:, 0:1] * X[:, 1:2]) > 0).astype(float)
    return X, y


def run_neural_continual_experiment(shift_freq=10, generations=200, pop_size=40, seed=42):
    rng = np.random.RandomState(seed)
    
    # Initialize neural population
    population = [
        NeuralAgent(capacity=rng.uniform(15.0, 45.0), f=rng.uniform(0.1, 0.9), lr=rng.uniform(0.01, 0.15))
        for _ in range(pop_size)
    ]
    
    current_task = 'A'
    history = []

    for g in range(generations):
        if g > 0 and g % shift_freq == 0:
            current_task = 'B' if current_task == 'A' else 'A'
            
        X_train, y_train = generate_task_data(current_task, n_samples=60, seed=g)
        X_test, y_test = generate_task_data(current_task, n_samples=40, seed=g+1000)
        
        evaluated = []
        for agent in population:
            # Lifetime learning
            agent.train_step(X_train, y_train, steps=6)
            acc = agent.evaluate_accuracy(X_test, y_test)
            
            # Metabolic costs: learning penalty + capacity upkeep
            time_penalty = agent.lr * 1.5
            cap_cost = (agent.capacity / 100.0) * 0.15
            fitness = max(0.0, acc - time_penalty - cap_cost)
            
            evaluated.append((fitness, agent))
            
        # Selection: top 50%
        evaluated.sort(key=lambda item: item[0], reverse=True)
        survivors = [item[1] for item in evaluated[:pop_size // 2]]
        
        # Metrics
        mean_f = np.mean([a.f for a in survivors])
        mean_lr = np.mean([a.lr for a in survivors])
        mean_cap = np.mean([a.capacity for a in survivors])
        mean_acc = np.mean([item[0] for item in evaluated[:pop_size // 2]])
        history.append({"gen": g, "f": float(mean_f), "lr": float(mean_lr), "cap": float(mean_cap), "fitness": float(mean_acc)})
        
        # Next generation reproduction
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

    return history


if __name__ == "__main__":
    print("=== Neural Continual Learning under Generational Memory Economics ===")
    print("Testing neural agents evolving weight retention, learning rate, and parameter capacity...\n")
    
    for freq in [2, 10, 50]:
        hist = run_neural_continual_experiment(shift_freq=freq, generations=150)
        final = hist[-1]
        print(f"Shift Frequency: Every {freq:2d} gens | Final Retention (f): {final['f']:.3f} | LR: {final['lr']:.3f} | Capacity: {final['cap']:.1f}")

    # Save prototype run data
    save_path = os.path.join(os.path.dirname(__file__), "../../data/neural_continual_prototype.json")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w") as fp:
        json.dump(hist, fp, indent=2)
    print(f"\nPrototype results saved to {save_path}")
