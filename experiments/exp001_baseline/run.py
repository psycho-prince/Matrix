import argparse
import sys
from pathlib import Path

# Add the project root to the path so we can import gal
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from gal.agents.agent import Agent
from gal.environment.world import Environment
from gal.metrics.knowledge import GenerationalKnowledgeAccumulation

def run_baseline(num_agents=100, generations=10):
    print(f"Starting Baseline Experiment (Exp001)")
    print(f"Configuration: {num_agents} agents per generation, {generations} generations.")
    print("Hypothesis: Independent populations without knowledge transfer will not accumulate knowledge across generations.")
    
    world = Environment()
    
    knowledge_history = []
    
    for gen in range(1, generations + 1):
        print(f"\n--- Generation {gen} ---")
        
        # In baseline, there is no inheritance. Generation starts from scratch.
        population = [Agent(identity=f"GAL-GEN{gen}-{i:03d}", generation=gen) for i in range(num_agents)]
        
        # Simulate life cycle
        for agent in population:
            agent.develop()
            agent.learn(world)
            agent.work()
            
        # Measure knowledge at end of generation
        gen_knowledge = sum(agent.knowledge_count for agent in population) / num_agents
        knowledge_history.append(gen_knowledge)
        print(f"Generation {gen} Average Knowledge: {gen_knowledge:.2f} concepts")
        
        # Generation dies. No inheritance step in baseline.
        
    print("\n--- Experiment Complete ---")
    
    # Calculate GKA (Generational Knowledge Accumulation)
    gka = GenerationalKnowledgeAccumulation(knowledge_history)
    print(f"Generational Knowledge Accumulation (GKA) score: {gka.calculate():.4f}")
    if gka.calculate() <= 0.1:
        print("Result supports hypothesis: No significant generational accumulation observed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Baseline Experiment (No Inheritance)")
    parser.add_argument("--agents", type=int, default=100, help="Number of agents per generation")
    parser.add_argument("--generations", type=int, default=10, help="Number of generations to simulate")
    
    args = parser.parse_args()
    run_baseline(num_agents=args.agents, generations=args.generations)
