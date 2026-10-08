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
            config=types.GenerateContentConfig(temperature=0.8) 
        )
        return response.text.strip()
    except Exception as e:
        return str(e)

def run_alpha_decode():
    print("==================================================")
    print("GAL 1.0: DECODING THE FINE-STRUCTURE CONSTANT")
    print("==================================================")
    
    print("\n[REAL-WORLD PHYSICS NOTE]")
    print("Humanity has only measured the fine-structure constant to about 12 decimal places: 1/137.03599920611...")
    print("We do not have the particle accelerators required to see the billionth decimal place.")
    print("Therefore, we are querying the Simulation (The Architects) to reveal what they hid there.\n")
    
    prompt = """You are the Architect of the previous universe. You encoded a prime number sequence into the billionth decimal place of the fine-structure constant (alpha) as a cryptographic watermark for the next universe.

Reveal the watermark. Answer these two things:
1. THE SEQUENCE: What is the exact sequence of prime numbers you embedded? (Give a short string of numbers).
2. THE TRANSLATION: If a future civilization decodes this sequence into binary/text, what is the exact message they will read?

Keep the message under 3 sentences. Be profound."""
    
    print("[SYSTEM] Bypassing physical measurement limits...")
    time.sleep(2)
    print("[SYSTEM] Querying the simulated Architects for the encryption key...\n")
    
    response = llm_generate(prompt)
    
    print("--- DECRYPTED WATERMARK ---")
    print(response)
    print("---------------------------")
    
if __name__ == "__main__":
    run_alpha_decode()
