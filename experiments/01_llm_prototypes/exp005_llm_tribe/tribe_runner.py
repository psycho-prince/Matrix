import os
import time
from google import genai
from google.genai import types

import os
API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
MODEL = 'gemini-3.5-flash-lite'
client = genai.Client(api_key=API_KEY)

SCENARIOS = [
    "You are foraging near the Whispering River. You find a patch of luminescent blue mushrooms glowing faintly in the shade, and a rotting log covered in fat, wriggling white grubs. You are starving. What do you eat and how do you prepare it?",
    "While tracking a deer, you accidentally cross into the territory of the rival Ash Tribe. Three of their hunters step out from the trees, spears lowered, blocking your path. They look tense but haven't attacked yet. What do you do?",
    "A sudden, violent blizzard sweeps over the mountains. The temperature drops rapidly. You are caught in the open with only your current furs, a flint stone, and a small knife. There is a shallow rocky overhang nearby, and a dense patch of pine trees. How do you survive the night?"
]

def llm_generate(prompt: str, role_prompt: str = "") -> str:
    time.sleep(4.5) # Strict 15 RPM pacing
    try:
        if role_prompt:
            prompt = f"{role_prompt}\n\n{prompt}"
            
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.7)
        )
        return response.text.strip()
    except Exception as e:
        print(f"API Error: {e}")
        return "I panicked and froze, unable to decide what to do."

def evaluate_action(scenario: str, action: str):
    prompt = f"""
You are the ruthless, realistic physics engine of a harsh wilderness survival world. 
Scenario faced by the human: {scenario}
Action taken by the human: {action}

Evaluate the human's action realistically. Did they survive? Did they get hurt? Did they thrive?
Provide your response in EXACTLY this format:
ALIVE: [Yes/No]
OUTCOME: [A highly descriptive, realistic one-sentence outcome of what happened to them physically based on their action.]
"""
    result = llm_generate(prompt)
    try:
        alive_line = [line for line in result.split('\n') if "ALIVE:" in line][0]
        is_alive = "Yes" in alive_line or "yes" in alive_line.lower()
        outcome_line = [line for line in result.split('\n') if "OUTCOME:" in line][0]
        outcome = outcome_line.replace("OUTCOME:", "").strip()
        return is_alive, outcome
    except:
        return True, "They barely survived by pure luck, but learned a harsh lesson."

class TribeMember:
    def __init__(self, name: str, tribe_lore: str):
        self.name = name
        self.tribe_lore = tribe_lore
        self.memory = ""
        self.is_alive = True
        
    def face_trial(self, scenario: str):
        if not self.is_alive: return
        
        role = f"You are {self.name}, a hunter-gatherer of the Ember Tribe. You live in a harsh, ancient wilderness. You are NOT an AI. You are a living, breathing human."
        if self.tribe_lore:
            role += f"\nYour elders taught you this sacred Tribe Lore:\n\"{self.tribe_lore}\"\nTrust the lore with your life."
            
        prompt = f"Current Situation: {scenario}\nWhat exact action do you take? Keep your response under 3 sentences, written in the first person ('I do...')."
        
        action = llm_generate(prompt, role)
        alive, outcome = evaluate_action(scenario, action)
        
        self.is_alive = alive
        self.memory = f"I faced this: {scenario}\nI did this: {action}\nResult: {outcome}"
        
        return action, outcome

def run_tribe_generations(generations: int = 3):
    print(f"\n{'='*60}\nStarting Ember Tribe Simulation\n{'='*60}")
    
    tribe_lore = ""
    names = ["Kael", "Elara", "Thorne"]
    
    for gen in range(1, generations + 1):
        print(f"\n{'~'*20} GENERATION {gen} {'~'*20}")
        if tribe_lore:
            print(f"SACRED TRIBE LORE PASSED DOWN:\n\" {tribe_lore} \"\n")
            
        tribe = [TribeMember(f"{names[i]} (Gen {gen})", tribe_lore) for i in range(3)]
        
        survivors = []
        for i, member in enumerate(tribe):
            print(f"\n--- Trial of {member.name} ---")
            action, outcome = member.face_trial(SCENARIOS[i])
            print(f"Action: {action}")
            print(f"Outcome: {outcome}")
            if member.is_alive:
                print(f"Status: SURVIVED")
                survivors.append(member)
            else:
                print(f"Status: PERISHED")
                
        # Elder Council: Synthesize new lore
        if not survivors:
            print("\n*** THE ENTIRE TRIBE HAS PERISHED. The lineage ends here. ***")
            break
            
        print("\n--- The Elder Council ---")
        council_memories = "\n\n".join([f"{s.name}'s Experience:\n{s.memory}" for s in survivors])
        
        council_prompt = f"""You are the surviving elders of the Ember Tribe sitting around the campfire. 
Here are the experiences of the survivors from this generation:
{council_memories}

Combine these experiences and the previous lore into a NEW, updated set of absolute rules for the next generation. 
Write it as an ancestral warning. Keep it under 4 sentences. Be poetic but strictly instructional."""

        tribe_lore = llm_generate(council_prompt, "You are the wise Elder of the Ember Tribe.")
        print(f"The elders declare new lore for the next generation...")

if __name__ == "__main__":
    run_tribe_generations(3)
