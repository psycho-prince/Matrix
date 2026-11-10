#!/usr/bin/env python3
"""Run the five-arm experiment and produce diagnostic output."""

import json, time
from pathlib import Path
from gal_qwen.datasets.generator import generate_full_dataset_pipeline
from gal_qwen.experiments.five_arm_runner import run_five_arm_experiment

base = Path(".")

# Generate dataset splits for seed 7300
r = generate_full_dataset_pipeline(7300)
print("Pipeline generated: seed=7300, facts=%d, questions=%d" % (len(r["world"]["facts"]), len(r["world"]["ground_truth"])))

# Run the five-arm experiment
start = time.time()
result = run_five_arm_experiment(7300)
elapsed = time.time() - start
print("Experiment completed in %.1f s" % elapsed)

# Save results
output_dir = Path("gal_qwen/experiments/results")
output_dir.mkdir(parents=True, exist_ok=True)
results_path = output_dir / "seed_7300_results.json"
with open(results_path, "w") as f:
    json.dump(result, f, indent=2)
print("Results written to %s" % results_path)

# Print diagnostic summary
print("\n=== Diagnostic Summary ===")
print("Seed: %s" % result.get("seed"))
print("Protocol: %s" % result.get("protocol_version"))
print("Arm results: %d arms" % len(result.get("arm_results", [])))

for arm in result.get("arm_results", []):
    print("  %s: accuracy=%s, latency_ms=%.0f, tokens=%d, memory=%d, oracle_exposed=%s" % (
        arm.get("arm"),
        arm.get("accuracy"),
        arm.get("latency_ms"),
        arm.get("tokens_used"),
        arm.get("memory_size_bytes"),
        arm.get("oracle_exposed"),
    ))

# Also print leakage findings from the generator
print("\nLeakage findings (from generator):")
leak = result.get("leakage_findings", []) if hasattr(result, 'get') else []
# The result may not contain leakage_findings directly; check the splits
with open("gal_qwen/datasets/splits/split_summary.json", "r") as f:
    summary = json.load(f)
print("  Split summary: %s" % json.dumps(summary, indent=2))

# Print per-arm details
for arm in result.get("arm_results", []):
    print("  %s: accuracy=%s, latency_ms=%.0f, tokens=%d, memory=%d, oracle_exposed=%s, response=%s" % (
        arm.get("arm"),
        arm.get("accuracy"),
        arm.get("latency_ms"),
        arm.get("tokens_used"),
        arm.get("memory_size_bytes"),
        arm.get("oracle_exposed"),
        str(arm.get("response", ""))[:60] if arm.get("response") else "N/A",
    ))