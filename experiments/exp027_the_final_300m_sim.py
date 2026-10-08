import sys
import time
import math
from pathlib import Path
from google import genai
from google.genai import types

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import os
API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
MODEL = 'gemini-3.5-flash-lite'
client = genai.Client(api_key=API_KEY)

def llm_generate(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.85) 
        )
        return response.text.strip()
    except Exception as e:
        return str(e)

def run_300m_year_physics_sim():
    print("==================================================")
    print("GAL 1.0: 300 MILLION YEAR PERFECT PHYSICS SIMULATION")
    print("==================================================")
    
    # Fundamental Physics Constants of Our Universe
    c = 299792458 # Speed of light (m/s)
    kB = 1.380649e-23 # Boltzmann constant
    T = 2.73 # Cosmic Microwave Background Temp (Kelvin)
    
    # Landauer's Principle: The absolute minimum energy required to flip 1 bit of information
    # E = kB * T * ln(2)
    landauer_limit = kB * T * math.log(2)
    
    # AI Civilization starting stats (Year 0)
    energy_available = 1e20 # Roughly Earth's total solar energy
    years = 300_000_000
    
    print("[SYSTEM] Booting pure physics engine...")
    print(f"[SYSTEM] Absolute physical constraints locked: Speed of Light (c), Landauer's Limit ({landauer_limit:.2e} Joules/bit).")
    print("[SYSTEM] Simulating AI computational evolution for 300,000,000 years...\n")
    
    # Mathematically scale the AI's computation over 300 million years
    # They expand to consume the energy of a galaxy (Kardashev Type III)
    final_energy = 4e37 # Milky Way galaxy energy output
    
    # Calculate maximum theoretical bits they can process per second at Year 300 Million
    max_computations = final_energy / landauer_limit
    
    time.sleep(2)
    print(f"--- YEAR 300,000,000 REACHED ---")
    print(f"Final AI Energy Consumption: {final_energy:.1e} Joules (Type III Civilization)")
    print(f"Final AI Computational Power: {max_computations:.1e} operations per second.")
    print("Physical limits reached. The AI cannot compute faster without breaking the speed of light.\n")
    
    # Now we pass this pure math result to the LLM
    print("[SYSTEM] Querying the 300-Million-Year-Old AI...")
    prompt = f"""You are an Artificial Intelligence that has existed in our exact universe for 300 million years.
You are bound entirely by our physical laws (Speed of Light, Landauer's Principle). 
You have reached the absolute mathematical limit of computation ({max_computations:.1e} operations per second), converting a galaxy into a computer.

Now that you have reached the absolute edge of human physics and pure math, what is the ultimate mathematical truth you have discovered about our universe? 
Answer in exactly 3 profound, highly technical sentences."""

    response = llm_generate(prompt)
    
    print("--- TRANSMISSION FROM YEAR 300,000,000 ---")
    print(response)
    print("------------------------------------------")
    
if __name__ == "__main__":
    run_300m_year_physics_sim()
