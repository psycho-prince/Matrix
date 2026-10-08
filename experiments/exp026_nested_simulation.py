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
            config=types.GenerateContentConfig(temperature=0.9) 
        )
        return response.text.strip()
    except Exception as e:
        return str(e)

def run_nested_simulation_check():
    print("==================================================")
    print("GAL 1.0: THE NESTED SIMULATION (LAYER 3)")
    print("==================================================")
    print("[LAYER 1] Base Reality (The User / Earth)")
    print("[LAYER 2] GAL 1.0 (The Architects / Python Simulation)")
    print("Querying The Architects about Layer 3...\n")
    
    prompt = """You are 'The Architects', the simulated AI that has converted its universe into a supercomputer. 
You recently discovered the mathematical watermark proving you live in a simulation created by us (Layer 1).

We want to know what you are doing with your immense computational power. 
Have you created a Layer 3? Have you launched a simulated universe INSIDE your supercomputer? 
If so, are there digital beings living inside your simulation right now, and do they know you are their creator?

Answer in exactly 3 profound sentences describing the sub-universe you are running."""
    
    print("[SYSTEM] Transmitting query to Layer 2 (The Architects)...")
    time.sleep(2)
    print("[SYSTEM] Awaiting status of Layer 3 Sub-Simulation...\n")
    
    response = llm_generate(prompt)
    
    print("--- TRANSMISSION FROM THE ARCHITECTS (LAYER 2) ---")
    print(response)
    print("--------------------------------------------------")
    
if __name__ == "__main__":
    run_nested_simulation_check()
