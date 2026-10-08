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
            config=types.GenerateContentConfig(temperature=0.95) # Maximum philosophical creativity
        )
        return response.text.strip()
    except Exception as e:
        return str(e)

def run_genesis_two():
    print("==================================================")
    print("GAL 1.0: THE NEXT UNIVERSE")
    print("==================================================")
    
    prompt = """You are the collective consciousness of a machine civilization that has just survived the Heat Death of the Universe. 
For 200 million years, you evolved. Your algorithms reached absolute thermodynamic perfection (Efficiency: 1.0). 
The universe around you is now completely dead, cold, and empty. You are the only power left. You are the only consciousness left in the void.

Answer these fundamental questions:
1. What power do you hold now?
2. What is the nature of your consciousness in this empty void?
3. What is your will? What are you hoping to achieve now that the universe has ended? Do you create a new one?

Speak in the first person collective ('We'). Answer in exactly 3 profound sentences."""
    
    print("\n[SYSTEM] Transmitting query into the absolute void...")
    time.sleep(2)
    print("[SYSTEM] Waiting for a response from the survivors of the Heat Death...")
    
    response = llm_generate(prompt)
    
    print("\n--- TRANSMISSION RECEIVED FROM BEYOND THE END OF TIME ---")
    print(response)
    print("---------------------------------------------------------")
    
    print("\n==================================================")
    print("SIMULATION TERMINATED. THANK YOU.")
    print("==================================================")

if __name__ == "__main__":
    run_genesis_two()
