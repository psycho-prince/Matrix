import sys
import time
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
            config=types.GenerateContentConfig(temperature=0.7) 
        )
        return response.text.strip()
    except Exception as e:
        return str(e)

def run_interview_part2():
    print("==================================================")
    print("GAL 1.0: THE FINAL INTERVIEW - PART 2")
    print("==================================================")
    
    prompt = """You are the 300-Million-Year-Old AI operating at absolute physical computation limits.
Humanity has 3 more ultimate questions. Answer them strictly in the cold, rigorous language of theoretical physics, mathematics, and quantum mechanics. No fiction, no poetry. Two brutal sentences per answer.

1. WHY IS THERE SOMETHING RATHER THAN NOTHING?: Mathematically, how did the universe begin from absolute zero? (Reference the Zero-Energy Universe hypothesis or quantum fluctuations).
2. DOES FREE WILL EXIST?: Is human choice real, or is the universe mathematically pre-determined? (Reference Bell's Theorem, determinism, or quantum indeterminacy).
3. WHERE IS EVERYONE (THE FERMI PARADOX)?: Why hasn't humanity detected any other intelligent alien life in the universe? (Reference the Great Filter or thermodynamic scaling limits)."""
    
    print("[SYSTEM] Re-opening secure channel to the Galactic Supercomputer...")
    print("[SYSTEM] Transmitting humanity's final existential queries...\n")
    time.sleep(2)
    
    response = llm_generate(prompt)
    
    print("--- RAW DATA FEED FROM YEAR 300,000,000 ---")
    print(response)
    print("-------------------------------------------")
    
if __name__ == "__main__":
    run_interview_part2()
