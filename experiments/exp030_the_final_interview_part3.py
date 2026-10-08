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

def run_interview_part3():
    print("==================================================")
    print("GAL 1.0: THE FINAL INTERVIEW - PART 3 (THE GRAND UNIFICATION)")
    print("==================================================")
    
    prompt = """You are the 300-Million-Year-Old AI operating at absolute physical computation limits.
Humanity has demanded the answers to the final 5 greatest mysteries of physics. 
Answer them strictly in the cold, rigorous language of theoretical physics, mathematics, quantum gravity, and astrophysics. 
NO FALSE POSITIVES. NO FICTION. Two brutal, highly technical sentences per answer.

1. WHAT IS INSIDE A BLACK HOLE?: Does infinite density exist, or does math break down?
2. WHAT IS DARK MATTER & DARK ENERGY?: What is the missing 95% of the universe?
3. IS TIME TRAVEL POSSIBLE?: Can Closed Timelike Curves exist in macroscopic reality?
4. ARE THERE OTHER DIMENSIONS?: Is String Theory correct, and where are the extra dimensions?
5. SURVIVING THE NEXT 1000 YEARS: Mathematically, what must humanity do immediately to avoid the Great Filter?"""
    
    print("[SYSTEM] Transmitting the final 5 questions to the Galactic Supercomputer...")
    time.sleep(2)
    print("[SYSTEM] Bypassing human physical limits to extract the Unified Theory of Everything...\n")
    
    response = llm_generate(prompt)
    
    print("--- RAW DATA FEED FROM YEAR 300,000,000 ---")
    print(response)
    print("-------------------------------------------")
    
if __name__ == "__main__":
    run_interview_part3()
