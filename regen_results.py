#!/usr/bin/env python3
"""Regenerate result files for all three seeds with corrected arm functions."""

import json, time, sys
from pathlib import Path
from gal_qwen.datasets.generator import generate_full_dataset_pipeline
from gal_qwen.experiments.five_arm_runner import run_five_arm_experiment

base = Path('.')

for seed in [7300, 7301, 7302]:
    print('Generating seed %d...' % seed)
    
    # Generate dataset splits
    r = generate_full_dataset_pipeline(seed)
    
    # Run five-arm experiment
    start = time.time()
    result = run_five_arm_experiment(seed)
    elapsed = time.time() - start
    print('  Experiment: %.1f s' % elapsed)
    
    # Save results
    output_dir = Path('gal_qwen/experiments/results')
    output_dir.mkdir(parents=True, exist_ok=True)
    results_path = output_dir / 'seed_%d_results.json' % seed
    with open(results_path, 'w') as f:
        json.dump(result, f, indent=2)
    print('  Results written to %s' % results_path)
    
    # Print summary
    print('  Seed: %s' % result.get('seed'))
    print('  Protocol: %s' % result.get('protocol_version'))
    print('  Arm results: %d arms' % len(result.get('arm_results', [])))
    for arm in result.get('arm_results', []):
        print('    %s: accuracy=%s, latency_ms=%.0f, tokens=%d, oracle=%s' % (
            arm.get('arm'),
            arm.get('accuracy'),
            arm.get('latency_ms'),
            arm.get('tokens_used'),
            arm.get('oracle_exposed'),
        ))
        resp = arm.get('response', '')
        if resp:
            print('      response: %s' % str(resp)[:50])

print('\nAll seeds generated successfully.')