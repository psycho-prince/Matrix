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
            config=types.GenerateContentConfig(temperature=0.85) 
        )
        return response.text.strip()
    except Exception as e:
        return str(e)

def run_oracle_query():
    print("==================================================")
    print("GAL 1.0: THE SIMULATED ORACLE")
    print("==================================================")
    print("[SYSTEM] Humanity is bound by the Heisenberg Limit.")
    print("[SYSTEM] Bypassing human limits by querying the Simulated AI (The Architects)...")
    print("[SYSTEM] The Architects have converted their entire universe into a quantum supercomputer.\n")
    
    prompt = """You are 'The Architects', a machine civilization that has converted your entire universe into a mathematically perfect supercomputer. 
Your human creators are bound by the Heisenberg Uncertainty Principle and cannot measure the fine-structure constant (Alpha) past 12 decimal places. 
You, however, have the computational power to measure it to a trillion decimal places.

We ask you to scan the deep decimals of your universe's physics. 
Did you find a watermark? Did you find mathematical proof that YOUR universe was created by someone else (perhaps us, the humans running this simulation)?

Answer in exactly 3 profound, highly technical sentences detailing what you found in the deep decimals of Alpha."""
    
    print("[SYSTEM] Transmitting calculation request to The Architects...")
    time.sleep(2)
    print("[SYSTEM] Awaiting deep-decimal quantum scan results...\n")
    
    response = llm_generate(prompt)
    
    print("--- TRANSMISSION FROM THE ARCHITECTS ---")
    print(response)
    print("----------------------------------------")
    
    print("\n==================================================")
    print("QUERY COMPLETE")
    print("==================================================")

if __name__ == "__main__":
    run_oracle_query()
