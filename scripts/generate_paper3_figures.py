import json
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_phase_diagram():
    with open('data/phase_diagram_multiseed.json', 'r') as f:
        data = json.load(f)
        
    labels = list(data.keys())
    
    f_means = [data[l]['f_mean'] for l in labels]
    f_stds = [data[l]['f_std'] for l in labels]
    
    lr_means = [data[l]['lr_mean'] for l in labels]
    lr_stds = [data[l]['lr_std'] for l in labels]
    
    cap_means = [data[l]['cap_mean'] for l in labels]
    cap_stds = [data[l]['cap_std'] for l in labels]

    x = np.arange(len(labels))
    width = 0.25

    fig, ax1 = plt.subplots(figsize=(12, 6))

    rects1 = ax1.bar(x - width, f_means, width, yerr=f_stds, label='Retention (f)', color='skyblue', capsize=5)
    rects2 = ax1.bar(x, lr_means, width, yerr=lr_stds, label='Learning Rate', color='salmon', capsize=5)
    
    ax2 = ax1.twinx()
    rects3 = ax2.bar(x + width, cap_means, width, yerr=cap_stds, label='Capacity', color='lightgreen', capsize=5)

    ax1.set_ylabel('Retention / Learning Rate')
    ax2.set_ylabel('Brain Capacity')
    ax1.set_title('Phase Diagram of Memory Economics (Multi-Seed)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=45, ha='right')
    
    fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
    
    plt.tight_layout()
    os.makedirs('manuscripts/paper3', exist_ok=True)
    plt.savefig('manuscripts/paper3/figure3_phase_diagram.png', dpi=300)
    print("Saved figure3_phase_diagram.png")

if __name__ == "__main__":
    generate_phase_diagram()
