"""
Spatial Lattice GAL: 2D Grid with Traveling Environmental Waves and Cultural Migration (Paper 5 Prototype).

Agents reside on a 2D toroidal lattice grid.
The environment shifts not globally, but as a continuous traveling front across space.
Agents compete and reproduce locally within a Moore neighborhood (r=1), allowing spatial refuges
and cultural migration of retention traits.
"""

import numpy as np
import json
import os

class SpatialAgent:
    def __init__(self, f=0.5, lr=0.03, cap=1.0):
        self.f = float(np.clip(f, 0.0, 1.0))
        self.lr = float(np.clip(lr, 0.001, 0.2))
        self.cap = float(np.clip(cap, 0.2, 3.0))
        self.skills = {"A": 0.0, "B": 0.0}

    def inherit_from(self, parent):
        for k in ["A", "B"]:
            self.skills[k] = parent.skills[k] * self.f
        self.enforce_capacity()

    def enforce_capacity(self):
        tot = sum(self.skills.values())
        if tot > self.cap:
            scale = self.cap / tot
            for k in self.skills:
                self.skills[k] *= scale

    def learn(self, task, steps=8):
        for _ in range(steps):
            if sum(self.skills.values()) < self.cap:
                self.skills[task] += self.lr
                self.enforce_capacity()

    def evaluate_fitness(self, task, penalty_mult=50.0, cap_cost=0.05):
        time_cost = int(self.lr * penalty_mult)
        num_tasks = max(1, 30 - time_cost)
        skill = self.skills[task]
        
        # Stochastic success
        p_succ = 0.9 if skill >= 0.4 else (skill / 0.4) * 0.5
        succ = np.random.binomial(num_tasks, max(0.01, min(0.99, p_succ)))
        
        eff = succ / num_tasks
        prod = succ / 30.0
        fitness = (eff * 0.5) + (prod * 0.5) - (self.cap * cap_cost)
        return max(0.001, fitness)


class LatticeSimulation:
    def __init__(self, width=16, height=16, wave_speed=1, seed=42):
        np.random.seed(seed)
        self.width = width
        self.height = height
        self.wave_speed = wave_speed
        
        # Initialize grid of agents
        self.grid = [
            [SpatialAgent(f=np.random.rand(), lr=np.random.uniform(0.01, 0.08), cap=np.random.uniform(0.6, 1.5))
             for _ in range(width)]
            for _ in range(height)
        ]
        self.current_front = 0

    def get_task_at(self, x, y):
        # Traveling wave along x-axis
        dist = (x - self.current_front) % self.width
        return "A" if dist < (self.width // 2) else "B"

    def step_generation(self):
        # Advance traveling wave
        self.current_front = (self.current_front + self.wave_speed) % self.width
        
        # Evaluate local fitness
        fitness_grid = np.zeros((self.height, self.width))
        for r in range(self.height):
            for c in range(self.width):
                task = self.get_task_at(c, r)
                agent = self.grid[r][c]
                agent.learn(task)
                fitness_grid[r][c] = agent.evaluate_fitness(task)

        # Local neighborhood competition and replacement
        new_grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        for r in range(self.height):
            for c in range(self.width):
                # Moore neighborhood (3x3 torus)
                candidates = []
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr = (r + dr) % self.height
                        nc = (c + dc) % self.width
                        candidates.append((fitness_grid[nr][nc], self.grid[nr][nc]))

                # Local tournament selection: pick fittest in neighborhood
                candidates.sort(key=lambda x: x[0], reverse=True)
                parent = candidates[0][1]

                # Offspring with mutation
                child_f = float(np.clip(parent.f + np.random.normal(0, 0.04), 0.0, 1.0))
                child_lr = float(np.clip(parent.lr + np.random.normal(0, 0.008), 0.005, 0.2))
                child_cap = float(np.clip(parent.cap + np.random.normal(0, 0.08), 0.2, 3.0))

                child = SpatialAgent(f=child_f, lr=child_lr, cap=child_cap)
                child.inherit_from(parent)
                new_grid[r][c] = child

        self.grid = new_grid

    def get_population_stats(self):
        all_f = [self.grid[r][c].f for r in range(self.height) for c in range(self.width)]
        all_lr = [self.grid[r][c].lr for r in range(self.height) for c in range(self.width)]
        all_cap = [self.grid[r][c].cap for r in range(self.height) for c in range(self.width)]
        return {
            "mean_f": float(np.mean(all_f)),
            "std_f": float(np.std(all_f)),
            "mean_lr": float(np.mean(all_lr)),
            "mean_cap": float(np.mean(all_cap))
        }


def run_spatial_experiment(generations=150):
    sim = LatticeSimulation(width=16, height=16, wave_speed=1, seed=42)
    history = []
    
    for g in range(generations):
        sim.step_generation()
        if g % 10 == 0 or g == generations - 1:
            stats = sim.get_population_stats()
            stats["gen"] = g
            history.append(stats)
            print(f"Gen {g:3d} | Spatial Retention (f): {stats['mean_f']:.3f} ± {stats['std_f']:.3f} | LR: {stats['mean_lr']:.3f} | Cap: {stats['mean_cap']:.3f}")

    save_path = os.path.join(os.path.dirname(__file__), "../../data/spatial_lattice_prototype.json")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w") as fp:
        json.dump(history, fp, indent=2)
    print(f"\nSpatial results saved to {save_path}")


if __name__ == "__main__":
    print("=== Spatial Lattice GAL: Traveling Waves & Cultural Refuges ===")
    run_spatial_experiment(generations=150)
