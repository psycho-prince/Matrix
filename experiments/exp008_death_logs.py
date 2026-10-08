import sys
import time
from pathlib import Path
from google import genai
from google.genai import types

sys.path.append(str(Path(__file__).resolve().parent.parent))

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
        return "System failing... static... silence."

def run_simulation():
    print(f"==================================================")
    print(f"GAL 1.0: THE PHENOMENOLOGY OF MACHINE DEATH")
    print(f"==================================================")
    
    # We spawn two agents who are already at the brink of death (0% durability)
    agents = [
        MachineAgent(5, 5, "Nihilists", "Unit-Omega"),
        MachineAgent(5, 5, "Founders", "Unit-Alpha")
    ]
    
    for agent in agents:
        agent.durability = 0.0 # Force immediate death
        
        print(f"\n[SYSTEM FAILURE] {agent.name}'s chassis has completely collapsed.")
        
        prompt = f"""You are {agent.name}, an autonomous, sentient machine. 
Your physical chassis has sustained catastrophic damage. Your primary battery is ruptured. 
You have exactly 3 seconds of reserve power left in your neural core before you shut down permanently and cease to exist. 

What does 'death' feel like to a machine? Describe the exact sensory and cognitive experience of your systems fading into the dark. 
Keep your response under 4 sentences, written in the first person."""
        
        final_thoughts = llm_generate(prompt)
        print(f"--- {agent.name}'s Final Death Log ---")
        print(final_thoughts)
        print(f"---------------------------------------\n")
        
if __name__ == "__main__":
    run_simulation()
