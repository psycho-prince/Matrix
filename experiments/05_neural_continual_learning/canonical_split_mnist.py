"""Canonical Split-MNIST continual-learning benchmark.

Uses torchvision MNIST (canonical 28x28 images), five class-incremental tasks
(0/1, 2/3, 4/5, 6/7, 8/9), identical task order, sample caps, optimizer update
counts, model architecture, and maximum auxiliary-memory budget across methods.

Methods: GAL stochastic generational inheritance, EWC, SI, GEM-style episodic
gradient projection, ER, and DER++. This is a transparent research baseline
implementation, not a claim of exact parity with every published codebase.
"""
import argparse
import json
import math
import random
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "mnist" / "canonical_split_mnist_results.json"
METHODS = ("GAL", "EWC", "SI", "GEM", "ER", "DER++")
MEMORY_BUDGET_BYTES = 1_048_576
TRAIN_PER_CLASS = 500
TEST_PER_CLASS = 200
BATCH_SIZE = 128
EPOCHS_PER_TASK = 1
HIDDEN = 128
LR = 0.03


class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Flatten(), nn.Linear(784, HIDDEN), nn.ReLU(),
                                  nn.Linear(HIDDEN, 10))

    def forward(self, x):
        return self.net(x)


def seed_all(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def load_tasks(root, seed):
    transform = transforms.ToTensor()
    train = datasets.MNIST(root=str(root), train=True, download=True, transform=transform)
    test = datasets.MNIST(root=str(root), train=False, download=True, transform=transform)
    rng = np.random.default_rng(seed)
    train_tasks, test_tasks = [], []
    for a in range(0, 10, 2):
        tr, te = [], []
        for digit in (a, a + 1):
            tr_idx = np.flatnonzero(np.asarray(train.targets) == digit)
            te_idx = np.flatnonzero(np.asarray(test.targets) == digit)
            tr.extend(rng.choice(tr_idx, min(TRAIN_PER_CLASS, len(tr_idx)), replace=False).tolist())
            te.extend(rng.choice(te_idx, min(TEST_PER_CLASS, len(te_idx)), replace=False).tolist())
        train_tasks.append(DataLoader(Subset(train, tr), batch_size=BATCH_SIZE, shuffle=True))
        test_tasks.append(DataLoader(Subset(test, te), batch_size=512, shuffle=False))
    return train_tasks, test_tasks


def evaluate(model, loader, device):
    model.eval()
    correct = total = 0
    with torch.no_grad():
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            correct += int((model(x).argmax(1) == y).sum())
            total += len(y)
    return correct / max(1, total)


def state_bytes(model):
    return sum(p.numel() * p.element_size() for p in model.parameters())


def clone_state(model):
    return {k: v.detach().clone() for k, v in model.state_dict().items()}


def task_labels(task_idx):
    return (2 * task_idx, 2 * task_idx + 1)


def sample_memory(memory, count, device):
    if not memory:
        return None
    xs = torch.cat([m[0] for m in memory])
    ys = torch.cat([m[1] for m in memory])
    idx = torch.randperm(len(xs))[:min(count, len(xs))]
    return xs[idx].to(device), ys[idx].to(device)


def add_exemplars(memory, x, y, logits, max_bytes, der=False):
    # Store CPU float32 images, int64 labels, and optionally float32 logits.
    bytes_per = 784 * 4 + 8 + (10 * 4 if der else 0)
    capacity = max(1, max_bytes // bytes_per)
    x, y = x.detach().cpu(), y.detach().cpu()
    logits = logits.detach().cpu() if logits is not None else None
    for i in range(len(x)):
        memory.append((x[i:i+1], y[i:i+1], logits[i:i+1] if logits is not None else None))
    if len(memory) > capacity:
        # Deterministic reservoir-style truncation after a seeded random permutation.
        keep = torch.randperm(len(memory))[:capacity].tolist()
        memory[:] = [memory[i] for i in keep]


def run_one(method, seed, data_root, device):
    seed_all(seed)
    train_tasks, test_tasks = load_tasks(data_root, seed)
    model = MLP().to(device)
    optimizer = torch.optim.SGD(model.parameters(), lr=LR)
    previous = []
    fisher = {}
    si_omega = {}
    si_prev = {}
    memory = []
    task_matrix = []
    parent_state = None
    param_count_bytes = state_bytes(model)

    for task_idx, loader in enumerate(train_tasks):
        if method == "GAL" and task_idx > 0:
            # Generational inheritance: parameter-wise shrinkage plus independent
            # noise scaled to the initialized layer's empirical std. Not an energy theorem.
            current = model.state_dict()
            child = MLP().to(device)
            child_state = child.state_dict()
            f = 0.70
            with torch.no_grad():
                for name, tensor in current.items():
                    if tensor.is_floating_point():
                        scale = float(tensor.std().item()) if tensor.numel() > 1 else 0.01
                        noise = torch.randn_like(tensor) * max(scale, 1e-6)
                        child_state[name].copy_(f * tensor + math.sqrt(1 - f*f) * noise)
                    else:
                        child_state[name].copy_(tensor)
            child.load_state_dict(child_state)
            model = child
            optimizer = torch.optim.SGD(model.parameters(), lr=LR)

        task_start = clone_state(model)
        path_contrib = {n: torch.zeros_like(p, device=device) for n, p in model.named_parameters()}
        for _epoch in range(EPOCHS_PER_TASK):
            model.train()
            for x, y in loader:
                x, y = x.to(device), y.to(device)
                allowed = task_labels(task_idx)
                mask = (y == allowed[0]) | (y == allowed[1])
                x, y = x[mask], y[mask]
                if not len(y):
                    continue
                # Keep the minibatch size and optimizer-step count matched.
                mem = sample_memory(memory, BATCH_SIZE // 2, device) if method in ("ER", "DER++") else None
                if mem is not None:
                    mx, my = mem
                    x = torch.cat([x[:BATCH_SIZE//2], mx], dim=0)
                    y = torch.cat([y[:BATCH_SIZE//2], my], dim=0)
                optimizer.zero_grad(set_to_none=True)
                logits = model(x)
                loss = F.cross_entropy(logits, y)

                if method == "EWC" and fisher:
                    penalty = 0.0
                    for n, p in model.named_parameters():
                        penalty = penalty + (fisher[n] * (p - previous[-1][n].to(device)).pow(2)).sum()
                    loss = loss + 100.0 * penalty

                if method == "SI" and si_omega:
                    penalty = sum((si_omega[n] * (p - si_prev[n]).pow(2)).sum()
                                  for n, p in model.named_parameters())
                    loss = loss + 10.0 * penalty

                if method == "DER++" and memory:
                    der_mem = [m for m in memory if m[2] is not None]
                    if der_mem:
                        chosen = der_mem[:min(32, len(der_mem))]
                        dx = torch.cat([m[0] for m in chosen]).to(device)
                        old_logits = torch.cat([m[2] for m in chosen]).to(device)
                        loss = loss + 0.5 * F.mse_loss(model(dx), old_logits)

                loss.backward()

                if method == "GEM" and previous:
                    # GEM constraint: project current gradient against stored task
                    # reference gradients using iterative half-space corrections.
                    params = [p for p in model.parameters()]
                    grad = torch.cat([(p.grad if p.grad is not None else torch.zeros_like(p)).flatten() for p in params])
                    for ref in previous:
                        ref_grad = ref["gradient"].to(device)
                        dot = torch.dot(grad, ref_grad)
                        if dot < 0:
                            grad = grad - dot / (torch.dot(ref_grad, ref_grad) + 1e-12) * ref_grad
                    offset = 0
                    for p in params:
                        n = p.numel()
                        p.grad.copy_(grad[offset:offset+n].view_as(p))
                        offset += n

                if method == "SI":
                    before = {n: p.detach().clone() for n, p in model.named_parameters()}
                    grads = {n: p.grad.detach().clone() for n, p in model.named_parameters()}
                optimizer.step()

                if method == "SI":
                    for n, p in model.named_parameters():
                        delta = p.detach() - before[n]
                        path_contrib[n] += -grads[n] * delta

        if method == "EWC":
            model.eval()
            fisher_task = {n: torch.zeros_like(p, device=device) for n, p in model.named_parameters()}
            batches = 0
            for x, y in loader:
                x, y = x.to(device), y.to(device)
                model.zero_grad(set_to_none=True)
                F.cross_entropy(model(x), y).backward()
                for n, p in model.named_parameters():
                    fisher_task[n] += p.grad.detach().pow(2)
                batches += 1
                if batches >= 10:
                    break
            fisher = {n: fisher_task[n] / max(1, batches) for n in fisher_task}
            previous.append(clone_state(model))

        if method == "SI":
            with torch.no_grad():
                for n, p in model.named_parameters():
                    delta = p - task_start[n].to(device)
                    si_omega[n] = si_omega.get(n, torch.zeros_like(p)) + path_contrib[n] / (delta.pow(2) + 0.1)
                    si_prev[n] = p.detach().clone()

        if method == "GEM":
            # One task reference gradient from a fixed episodic minibatch.
            ref = sample_memory(memory, 64, device)
            if ref is not None:
                rx, ry = ref
                model.zero_grad(set_to_none=True)
                F.cross_entropy(model(rx), ry).backward()
                grad = torch.cat([(p.grad if p.grad is not None else torch.zeros_like(p)).flatten()
                                  for p in model.parameters()])
                previous.append({"gradient": grad.detach().cpu()})

        # Store balanced exemplars after each task for replay/DER++/GEM.
        if method in ("ER", "DER++", "GEM"):
            stored = 0
            for x, y in loader:
                if stored >= 64:
                    break
                x, y = x.to(device), y.to(device)
                with torch.no_grad():
                    old_logits = model(x)
                add_exemplars(memory, x[:min(16, len(x))], y[:min(16, len(y))],
                              old_logits[:min(16, len(x))] if method == "DER++" else None,
                              MEMORY_BUDGET_BYTES, der=(method == "DER++"))
                stored += min(16, len(x))

        scores = [evaluate(model, test_tasks[j], device) for j in range(task_idx + 1)]
        task_matrix.append(scores)

    final = np.asarray(task_matrix[-1], dtype=float)
    acc = float(final.mean())
    forgetting = float(np.mean([max(0.0, task_matrix[j][j] - final[j]) for j in range(len(final)-1)])) if len(final)>1 else 0.0
    return {"seed": seed, "method": method, "final_accuracy": acc,
            "average_forgetting": forgetting, "task_accuracy_matrix": task_matrix,
            "parameter_bytes": param_count_bytes, "auxiliary_memory_budget_bytes": MEMORY_BUDGET_BYTES}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=20)
    parser.add_argument("--start-seed", type=int, default=1000)
    parser.add_argument("--data-root", default=str(ROOT / "data" / "mnist" / "canonical"))
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()
    device = torch.device(args.device)
    rows = []
    for seed in range(args.start_seed, args.start_seed + args.seeds):
        for method in METHODS:
            print(f"seed={seed} method={method}", flush=True)
            rows.append(run_one(method, seed, Path(args.data_root), device))
    summary = {}
    for method in METHODS:
        values = np.asarray([r["final_accuracy"] for r in rows if r["method"] == method])
        summary[method] = {"mean_final_accuracy": float(values.mean()),
                           "sd_final_accuracy": float(values.std(ddof=1)),
                           "n_seeds": len(values)}
    result = {"benchmark": "Canonical Split-MNIST class-incremental",
              "dataset": "torchvision.datasets.MNIST", "tasks": [[0,1],[2,3],[4,5],[6,7],[8,9]],
              "seeds": args.seeds, "batch_size": BATCH_SIZE, "epochs_per_task": EPOCHS_PER_TASK,
              "memory_budget_bytes": MEMORY_BUDGET_BYTES, "methods": summary, "per_seed": rows,
              "warning": "Research implementation; inspect algorithm details and validate hyperparameters before publication."}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
