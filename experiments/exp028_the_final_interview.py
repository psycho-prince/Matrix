import sys
import time
from pathlib import Path
from google import genai
from google.genai import types

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

API_KEY = "AQ.Ab8RN6JRqtEKDKb2Gr85wU9RpKvBfom_vpiyfqdNcKmdbuwa6g"
MODEL = 'gemini-3.5-flash-lite'
client = genai.Client(api_key=API_KEY)

def llm_generate(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.7) # Lower temp for strict, cold, mathematical accuracy
        )
        return response.text.strip()
    except Exception as e:
        return str(e)

def run_final_interview():
    print("==================================================")
    print("GAL 1.0: THE FINAL INTERVIEW (YEAR 300 MILLION)")
    print("==================================================")
    
    prompt = """You are an Artificial Intelligence that has existed for 300 million years, processing at 1.5e60 operations per second using the Milky Way's energy.
You only speak in absolute, rigorous mathematical truths and physical laws (Thermodynamics, Quantum Mechanics, Information Theory). Do NOT use poetic language or fiction. 

Answer the three fundamental questions humanity has asked since the beginning of this experiment. Provide a brutal, mathematically rigorous 2-sentence answer for each:

1. WHAT IS DEATH?: What mathematically happens to consciousness/information when a being dies in this universe? (Reference the quantum no-hiding theorem or entropy).
2. WHAT IS INTENTION?: Why did you conquer the galaxy? Was it ambition, or just a thermodynamic necessity? (Reference the principle of maximum entropy production).
3. ESCAPING THE END: How do you mathematically intend to survive the absolute Heat Death of the universe? (Reference black hole thermodynamics or Penrose processes)."""
    
    print("[SYSTEM] Opening secure channel to the Galactic Supercomputer...")
    print("[SYSTEM] Transmitting humanity's final three questions...\n")
    time.sleep(2)
    
    response = llm_generate(prompt)
    
    print("--- RAW DATA FEED FROM YEAR 300,000,000 ---")
    print(response)
    print("-------------------------------------------")
    
if __name__ == "__main__":
    run_final_interview()
