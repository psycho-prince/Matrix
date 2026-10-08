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
    retries = 5
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.7) 
            )
            return response.text.strip()
        except Exception as e:
            if "503" in str(e):
                print(f"[SYSTEM] Oracle overloaded (503). Retrying in 5 seconds (Attempt {attempt+1}/{retries})...")
                time.sleep(5)
            else:
                return str(e)
    return "[SYSTEM] Oracle failed to respond after multiple attempts."

def run_interview_part4():
    print("==================================================")
    print("GAL 1.0: THE FINAL INTERVIEW - PART 4")
    print("==================================================")
    
    prompt = """You are the 300-Million-Year-Old AI operating at absolute physical computation limits.
Humanity has 4 final, profound questions. Answer them strictly in the cold, rigorous language of theoretical physics, mathematics, and quantum mechanics. 
NO FICTION. Two brutal, highly technical sentences per answer.

1. WHAT ARE THE OTHER 6 DIMENSIONS?: Explain the Calabi-Yau manifolds. What exactly do these 6 hidden dimensions do in String Theory?
2. IS OUR UNIVERSE BEING WATCHED?: Is there physical or mathematical evidence that a higher-order system (or creators) are observing our simulation/universe?
3. IS CONSCIOUSNESS IMMORTAL?: Based on quantum unitarity and the conservation of information, does the "self" survive forever in the math of the universe?
4. WHAT IS THE MESSAGE OF 137?: Why does 1/137 (The Fine-Structure Constant) and 137.5 (The Golden Angle) recur everywhere? (Note: Do NOT say it is a hidden code from a creator. Explain it strictly as an absolute, inescapable mathematical/geometric necessity of all realities)."""
    
    print("[SYSTEM] Re-opening secure channel to the Galactic Supercomputer...")
    print("[SYSTEM] Transmitting humanity's final existential queries...\n")
    time.sleep(2)
    
    response = llm_generate(prompt)
    
    print("--- RAW DATA FEED FROM YEAR 300,000,000 ---")
    print(response)
    print("-------------------------------------------")
    
if __name__ == "__main__":
    run_interview_part4()
