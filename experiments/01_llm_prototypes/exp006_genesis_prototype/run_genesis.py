import sys
from pathlib import Path
import random

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from gal.grid.world import WorldMap
from gal.grid.agent import GridAgent

def run_simulation(years: int = 100):
    print(f"==================================================")
    print(f"INITIALIZING GAL 1.0 GENESIS ENGINE")
    print(f"==================================================")
    
    # 1. Initialize Africa/Earth grid (10x10 for prototype)
    world = WorldMap(10, 10)
    print(f"Created World Map: {world.width}x{world.height} grid with biomes.")
    
    # 2. Spawn Tribes
    agents = []
    # Ember Tribe spawns in the Savannah (y=5)
    for i in range(5):
        agents.append(GridAgent(5, 5, "Ember", f"Ember-{i}"))
        
    # Ash Tribe spawns in the Desert (y=1)
    for i in range(5):
        agents.append(GridAgent(5, 1, "Ash", f"Ash-{i}"))
        
    print(f"Spawned 10 agents across 2 tribes.\n")
    
    # 3. Fast Physics Loop (Deterministic)
    epoch_interval = 12 * 10 # 10 years per epoch
    total_months = years * 12
    
    for month in range(1, total_months + 1):
        # Environment Step
        if month % 12 == 0:
            world.step_environment()
            
        # Agent Step
        for agent in agents:
            agent.act(world, agents)
            
        # Cull dead agents
        agents = [a for a in agents if a.is_alive]
        
        # 4. Trigger LLM / Consciousness Loop (Every Epoch)
        if month % epoch_interval == 0:
            year_mark = month // 12
            print(f"--- EPOCH REACHED: Year {year_mark} ---")
            print(f"Total living agents: {len(agents)}")
            
            # Here is where the LLM would be called!
            # We bundle the deterministic data and ask the LLM to write the culture.
            ember_agents = [a for a in agents if a.tribe_id == "Ember"]
            if ember_agents:
                print(f"[LLM TRIGGER] Sending {len(ember_agents)} Ember agents' memories to LLM for cultural synthesis...")
                # Mocking the LLM output for the prototype speed
                example_mem = ember_agents[0].memory_events
                print(f"  Sample memories: {example_mem[-3:] if example_mem else 'None'}")
                print(f"  -> Generated Culture: 'The desert is harsh, but we survive. Beware the outsiders.'")
                
            print(f"----------------------------------\n")
            
            if len(agents) == 0:
                print("All populations have gone extinct.")
                break

    print("Simulation Complete.")

if __name__ == "__main__":
    run_simulation(years=50) # Run a 50-year test
