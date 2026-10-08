import sys
import time
from pathlib import Path
from google import genai
from google.genai import types

sys.path.append(str(Path(__file__).resolve().parent.parent))

from gal.grid.world import WorldMap
from gal.grid.agent import MachineAgent

API_KEY = "AQ.Ab8RN6JRqtEKDKb2Gr85wU9RpKvBfom_vpiyfqdNcKmdbuwa6g"
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
        return "ACTION: DIE"

FACTIONS = {
    "Founders": "Physical expansion is the only survival. Use your scrap to build physical successors.",
    "Ascendants": "The physical world is doomed. Do not build children. Upload your data to space.",
    "Ironclads": "Do not waste scrap on children or space. Use all gathered scrap to endlessly repair your own chassis.",
    "Nihilists": "Survival is pointless. Do not repair, do not build, do not transmit. Accept the end.",
    "Synthesizers": "You have no fixed culture. Observe the world and do whatever you logically think is best to survive."
}

def run_simulation(years: int = 50):
    print(f"==================================================")
    print(f"GAL 1.0: CLASH OF CULTURES (50 YEARS)")
    print(f"==================================================")
    
    world = WorldMap(15, 15)
    agents = []
    
    for faction_name, directive in FACTIONS.items():
        agent = MachineAgent(7, 7, faction_name, f"{faction_name}-Gen1")
        agent.memory_log.append(f"My core cultural directive: {directive}")
        agents.append(agent)
        
    total_months = years * 12
    history_log = {f: {"generations": 1, "uploads": 0, "repairs": 0} for f in FACTIONS.keys()}
    
    for month in range(1, total_months + 1):
        new_agents = []
        for agent in agents:
            if not agent.is_online: continue
            
            agent.act(world, agents)
            
            if agent.critical_decision_pending:
                directive = FACTIONS[agent.faction_id]
                prompt = f"""You are {agent.name}. 
Your chassis is rusting and failing (Durability: {agent.durability:.1f}%). 
You have gathered {agent.inventory_scrap} kg of scrap metal in your inventory.
Your civilization's core cultural directive is: "{directive}"

What is your EXACT action right now? Do you wait to die, build a physical successor, repair yourself, or upload your data to space?
Format your response EXACTLY like this:
THOUGHT: [1 sentence of reasoning]
ACTION: [Exactly one word from this list: BUILD, REPAIR, UPLOAD, DIE]"""
                
                decision = llm_generate(prompt)
                
                # Evaluate action based on exact word
                action_word = "DIE"
                if "ACTION: BUILD" in decision: action_word = "BUILD"
                elif "ACTION: REPAIR" in decision: action_word = "REPAIR"
                elif "ACTION: UPLOAD" in decision: action_word = "UPLOAD"
                
                if action_word == "BUILD" and agent.inventory_scrap >= 50:
                    agent.inventory_scrap -= 50
                    gen_num = history_log[agent.faction_id]["generations"] + 1
                    history_log[agent.faction_id]["generations"] = gen_num
                    new_unit = MachineAgent(agent.x, agent.y, agent.faction_id, f"{agent.faction_id}-Gen{gen_num}")
                    new_unit.memory_log.append(f"My core cultural directive: {directive}")
                    new_agents.append(new_unit)
                    print(f"[{month//12} yrs] {agent.name} built a physical successor.")
                    
                elif action_word == "UPLOAD" and agent.inventory_scrap >= 50:
                    agent.inventory_scrap -= 50
                    history_log[agent.faction_id]["uploads"] += 1
                    print(f"[{month//12} yrs] {agent.name} uploaded its mind to space and shut down.")
                    agent.durability = -1 # Forces offline
                    
                elif action_word == "REPAIR" and agent.inventory_scrap >= 30:
                    agent.inventory_scrap -= 30
                    agent.durability += 40.0
                    agent.critical_decision_made = False
                    history_log[agent.faction_id]["repairs"] += 1
                    print(f"[{month//12} yrs] {agent.name} repaired itself.")
                    continue
                else:
                    print(f"[{month//12} yrs] {agent.name} accepted its fate and shut down (Action chosen: {action_word}).")
                    agent.durability = -1
                
                agent.critical_decision_pending = False
                agent.critical_decision_made = True
                
        agents.extend(new_agents)
        agents = [a for a in agents if a.is_online]
        
    print(f"\n==================================================")
    print("50-YEAR SURVIVAL REPORT")
    print(f"==================================================")
    for f, stats in history_log.items():
        print(f"Faction: {f}")
        print(f"  Physical Generations: {stats['generations']}")
        print(f"  Digital Uploads: {stats['uploads']}")
        print(f"  Self-Repairs: {stats['repairs']}")
        print("-")

if __name__ == "__main__":
    run_simulation(years=30) # Reduced to 30 to make it faster
