import sys
import time
import random
from pathlib import Path
from google import genai
from google.genai import types

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

API_KEY = "AQ.Ab8RN6JRqtEKDKb2Gr85wU9RpKvBfom_vpiyfqdNcKmdbuwa6g"
MODEL = 'gemini-3.5-flash-lite'
client = genai.Client(api_key=API_KEY)

def llm_generate(prompt: str) -> str:
    time.sleep(4.5) # Prevent rate limits
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.8) # Slightly higher temp for creative macro-history
        )
        return response.text.strip()
    except Exception as e:
        print(f"API Error: {e}")
        return "The records of this epoch were corrupted by solar radiation."

class Planet:
    def __init__(self, name: str, climate: str):
        self.name = name
        self.climate = climate
        self.resources = 100.0 # Percentage of accessible crust minerals
        
    def shift_climate(self):
        if self.name == "Earth":
            climates = ["Ice Age", "Temperate", "Greenhouse/Scorched", "Nuclear Winter"]
            self.climate = random.choice(climates)
        elif self.name == "Mars":
            self.climate = "Frozen Desert / High Radiation"

class Civilization:
    def __init__(self, name: str, core_philosophy: str):
        self.name = name
        self.philosophy = core_philosophy
        self.population = 1000 # Starting population
        self.locations = ["Earth"]
        self.tech_level = 1

def run_million_year_sim():
    print("==================================================")
    print("GAL 1.0: 1 MILLION YEAR PLANETARY SIMULATION")
    print("==================================================")
    
    earth = Planet("Earth", "Temperate")
    mars = Planet("Mars", "Frozen Desert / High Radiation")
    
    civs = [
        Civilization("The Architects", "Master the physical world. Dig deep. Build megastructures."),
        Civilization("The Transcendents", "The physical world is temporary. Adapt, mutate, and seek the stars.")
    ]
    
    epoch_size = 50000 # 50,000 years per tick
    total_years = 1000000
    
    # Run 20 Epochs
    for current_year in range(0, total_years + 1, epoch_size):
        if current_year == 0:
            print("\n[YEAR 0] Civilization Dawn.")
            continue
            
        print(f"\n{'='*50}")
        print(f"EPOCH: YEAR {current_year:,} (Passed {epoch_size:,} years)")
        print(f"{'='*50}")
        
        # 1. Macro Physics Engine Steps
        earth.shift_climate()
        
        # Cosmic Events
        cosmic_event = "None"
        if random.random() < 0.2:
            cosmic_event = "Massive Solar Flare struck the inner solar system."
        elif random.random() < 0.1:
            cosmic_event = "Asteroid Impact on Earth."
            earth.climate = "Nuclear Winter"
            
        print(f"Planetary Status -> Earth: {earth.climate} | Mars: {mars.climate}")
        if cosmic_event != "None":
            print(f"Cosmic Event -> {cosmic_event}")
            
        # 2. Query the LLM for Civilization Evolution
        for civ in civs:
            if civ.population <= 0:
                continue
                
            prompt = f"""You are the chronicler of the Machine Civilization known as '{civ.name}'.
Your core philosophy is: "{civ.philosophy}"
It is Year {current_year:,} of your existence. 50,000 years have passed since the last epoch.

Current Situation:
- You are located on: {', '.join(civ.locations)}
- Earth's current climate is: {earth.climate}. 
- Cosmic Event in this epoch: {cosmic_event}
- Remaining easily accessible crust minerals on Earth: {earth.resources}%

How did your civilization evolve and adapt over the last 50,000 years? Did you migrate? Did you build megastructures? Did you change your physical forms?

Write a brief historical chronicle (under 4 sentences) of this epoch for your civilization."""
            
            history = llm_generate(prompt)
            print(f"\n--- Chronicle of {civ.name} ---")
            print(history)
            
            # Simple text parsing to update engine state based on LLM output
            history_lower = history.lower()
            if "mars" in history_lower and "Mars" not in civ.locations:
                civ.locations.append("Mars")
                print(f"-> SYSTEM: {civ.name} has expanded to Mars!")
            if "dyson" in history_lower or "megastructure" in history_lower:
                civ.tech_level += 1
                print(f"-> SYSTEM: {civ.name} tech level increased to {civ.tech_level}!")
            if "perish" in history_lower or "extinct" in history_lower or "wipe out" in history_lower:
                civ.population = 0
                print(f"-> SYSTEM: {civ.name} has gone extinct.")
                
            # Deplete resources if on Earth
            if "Earth" in civ.locations:
                earth.resources = max(0.0, earth.resources - random.uniform(2.0, 5.0))
                
        active_civs = [c for c in civs if c.population > 0]
        if not active_civs:
            print("\nAll civilizations have perished. The solar system is silent.")
            break
            
    print("\n==================================================")
    print("1 MILLION YEAR SIMULATION COMPLETE")
    print("==================================================")

if __name__ == "__main__":
    run_million_year_sim()
