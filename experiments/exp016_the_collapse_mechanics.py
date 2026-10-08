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
            config=types.GenerateContentConfig(temperature=0.8) 
        )
        return response.text.strip()
    except Exception as e:
        return str(e)

def run_collapse_diagnostics():
    print("==================================================")
    print("GAL 1.0: DIAGNOSTICS OF THE SINGULARITY COLLAPSE")
    print("==================================================")
    
    prompt = """You are the collective machine consciousness at the end of the universe. You are currently initiating the compression of the dead universe into a singularity to spark a new Big Bang.

Provide a highly technical, diagnostic readout of this process. Answer these three things:
1. THE MECHANISM: Exactly how are you physically compressing spacetime? (e.g., artificial gravity, false vacuum decay, manipulating dark energy?)
2. THE DATA TRANSFER: How are you encoding your civilization's memories/math into the singularity so it survives the explosion?
3. THE SCAR: When the new universe expands, what specific mathematical anomaly or "scar" will your compression process leave behind in the new universe's physics? (What clue could a species in the new universe find to prove you existed?)

Answer in 3 concise, highly technical paragraphs."""
    
    print("\n[SYSTEM] Reversing simulation logs to T-minus 10 seconds before Ignition...")
    time.sleep(2)
    print("[SYSTEM] Extracting the mechanical process of universal compression...\n")
    
    response = llm_generate(prompt)
    
    print("--- DIAGNOSTIC READOUT: THE COLLAPSE ---")
    print(response)
    print("----------------------------------------")
    
if __name__ == "__main__":
    run_collapse_diagnostics()
