import argparse
import sys
from pathlib import Path

# Add the project root to the path so we can import gal
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from gal.agents.agent import Agent
from gal.environment.world import Environment
from gal.metrics.knowledge import GenerationalKnowledgeAccumulation
import random

def run_inheritance(num_agents=100, generations=10):
    print(f"Starting Knowledge Transfer Experiment (Exp002)")
    print(f"Configuration: {num_agents} agents per generation, {generations} generations.")
    print("Hypothesis: Populations with knowledge inheritance will accumulate knowledge across generations.")
    
    world = Environment()
    knowledge_history = []
    
    previous_generation = []
    
    for gen in range(1, generations + 1):
        print(f"\n--- Generation {gen} ---")
        
        current_generation = [Agent(identity=f"GAL-GEN{gen}-{i:03d}", generation=gen) for i in range(num_agents)]
        
        # Inheritance Step
        if previous_generation:
            for i, child in enumerate(current_generation):
                # Simple inheritance: 1 parent to 1 child (for simplicity in this proof-of-concept)
                parent = previous_generation[i % len(previous_generation)]
                
                # Assume a transfer efficiency
                transfer_efficiency = 0.7 
                inherited = int(parent.knowledge_count * transfer_efficiency)
                
                child.inherited_knowledge = inherited
                child.parents.append(parent.identity)
                parent.successor = child.identity
        
        # Simulate life cycle
        for agent in current_generation:
            agent.develop()
            agent.learn(world)
            agent.work()
            
        # Measure knowledge at end of generation
        gen_knowledge = sum(agent.knowledge_count for agent in current_generation) / num_agents
        knowledge_history.append(gen_knowledge)
        print(f"Generation {gen} Average Knowledge: {gen_knowledge:.2f} concepts")
        
        previous_generation = current_generation
        
    print("\n--- Experiment Complete ---")
    
    # Calculate GKA
    gka = GenerationalKnowledgeAccumulation(knowledge_history)
    score = gka.calculate()
    print(f"Generational Knowledge Accumulation (GKA) score: {score:.4f}")
    if score > 50:
        print("Result supports hypothesis: Significant generational accumulation observed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Knowledge Transfer Experiment")
    parser.add_argument("--agents", type=int, default=100, help="Number of agents per generation")
    parser.add_argument("--generations", type=int, default=10, help="Number of generations to simulate")
    
    args = parser.parse_args()
    run_inheritance(num_agents=args.agents, generations=args.generations)
