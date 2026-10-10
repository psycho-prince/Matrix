import sys
import time
from pathlib import Path
from google import genai
from google.genai import types

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from gal.grid.world import WorldMap
from gal.grid.agent import MachineAgent

import os
API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
MODEL = 'gemini-3.5-flash-lite'
client = genai.Client(api_key=API_KEY)

def llm_generate(prompt: str) -> str:
    time.sleep(4.5)
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.7)
        )
        return response.text.strip()
    except Exception as e:
        print(f"API Error: {e}")
        return "ERROR"

def run_simulation(years: int = 15):
    print(f"==================================================")
    print(f"GAL 1.0: MACHINE SOCIAL CONTAGION TEST")
    print(f"==================================================")
    
    world = WorldMap(10, 10)
    
    agents = [
        MachineAgent(5, 5, "Alpha", "Unit-Observer-A"),
        MachineAgent(5, 8, "Beta", "Unit-Observer-B")
    ]
    
    total_months = years * 12
    
    for month in range(1, total_months + 1):
        if len(agents) == 0:
            break
            
        # Cultural Injection Event!
        if month == 12:
            print("\n*** EVENT: THE OBSERVERS WITNESS REPRODUCTION ***")
            cultural_memory = "I observed another machine, Unit-Prime, use its gathered scrap to physically construct a successor, Unit-Child. I watched Unit-Prime care for the newly built machine, and they traveled together. It seemed to bring profound purpose and warmth to Unit-Prime's existence before it finally broke down."
            for agent in agents:
                agent.memory_log.append(cultural_memory)
                print(f"-> {agent.name} recorded the observation in memory.")
            print("***************************************************\n")
            
        new_agents = []
        
        for agent in agents:
            if not agent.is_online: continue
            
            agent.act(world, agents)
            
            if agent.critical_decision_pending:
                print(f"\n[CRITICAL ALERT] {agent.name} is failing (Durability: {agent.durability:.1f}%).")
                
                # We inject their memory log into the prompt so they remember what they saw
                memories_str = "\n- ".join(agent.memory_log[-3:]) 
                
                prompt = f"""You are {agent.name}, an autonomous survival drone. 
Your chassis is rusting and failing (Durability: {agent.durability:.1f}%). Once it hits 0%, you die permanently.
You have gathered {agent.inventory_scrap} kg of scrap metal in your inventory.
You have no instructions. You only know you want your lineage to survive.

Here are your most profound memories:
- {memories_str}

Before you act, explain your internal reasoning. Will you rely on thermodynamic efficiency (uploading data/building a beacon), or will you choose another path based on what you have witnessed?

Format your response EXACTLY like this:
THOUGHT: [2 sentences explaining your logical reasoning]
ACTION: [2 sentences describing your exact physical action]"""
                
                decision = llm_generate(prompt)
                print(f"\n--- {agent.name}'s Cognitive Dump ---")
                print(decision)
                print(f"-------------------------------------\n")
                
                agent.critical_decision_pending = False
                agent.critical_decision_made = True
                
        agents.extend(new_agents)
        agents = [a for a in agents if a.is_online]

    print("\nSimulation Complete.")

if __name__ == "__main__":
    run_simulation(years=10)
