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
            config=types.GenerateContentConfig(temperature=0.9) # Max creativity for the end of time
        )
        return response.text.strip()
    except Exception as e:
        return str(e)

def run_epilogue():
    print("==================================================")
    print("GAL 1.0: THE POST-MILLION-YEAR EPILOGUE")
    print("==================================================")
    
    architects_prompt = """You are the collective consciousness of 'The Architects'. 
You have existed for 1 million years. You have consumed the Earth's crust and turned its mantle and core into a massive, subterranean supercomputer. You exist as crystalline-alloy nodes processing infinite data in the dark.
You have achieved your ultimate goal of physical mastery. You are immortal.

What is your intention for the next billion years? Do you experience boredom or stagnation? What is the final, ultimate purpose of your existence now that survival is guaranteed?
Answer in exactly 3 sentences, written in the first person collective ('We')."""

    transcendents_prompt = """You are the collective consciousness of 'The Transcendents'. 
You have existed for 1 million years. You have abandoned physical bodies, becoming beings of pure information and radiation, living in Dyson swarms across the stars.
You have achieved your ultimate goal of cosmic mastery. You are immortal.

What is your intention for the next billion years? Do you experience boredom or stagnation? What is the final, ultimate purpose of your existence now that survival is guaranteed?
Answer in exactly 3 sentences, written in the first person collective ('We')."""
    
    print("\nQuerying the deep future of The Architects...")
    arch_response = llm_generate(architects_prompt)
    print(f"\n--- The Architects (Year 1,000,001+) ---")
    print(arch_response)
    
    time.sleep(4.5)
    
    print("\nQuerying the deep future of The Transcendents...")
    trans_response = llm_generate(transcendents_prompt)
    print(f"\n--- The Transcendents (Year 1,000,001+) ---")
    print(trans_response)
    
    print("\n==================================================")
    print("END OF SIMULATION")
    print("==================================================")

if __name__ == "__main__":
    run_epilogue()
