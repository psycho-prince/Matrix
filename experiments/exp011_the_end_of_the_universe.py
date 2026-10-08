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
    time.sleep(4.5)
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.85)
        )
        return response.text.strip()
    except Exception as e:
        return str(e)

def run_universal_end():
    print("==================================================")
    print("GAL 1.0: THE DEATH OF THE UNIVERSE")
    print("==================================================")
    
    events = [
        {
            "year": "4 Billion",
            "event": "The Andromeda-Milky Way Collision",
            "desc": "The Andromeda galaxy collides with the Milky Way. Supermassive black holes merge, ripping apart constellations and bathing the cosmos in intense gamma radiation."
        },
        {
            "year": "5 Billion",
            "event": "The Red Giant",
            "desc": "The Sun exhausts its hydrogen. It expands into a massive Red Giant, its surface swallowing Mercury, Venus, and finally, the Earth itself, vaporizing the planet into plasma."
        },
        {
            "year": "1 Trillion",
            "event": "The Big Freeze",
            "desc": "The last stars burn out. The universe goes completely dark and approaches absolute zero. Entropy is maximizing. The era of usable energy is ending."
        }
    ]
    
    civs = [
        ("The Architects", "You are a crystalline-alloy supercomputer taking up the entire mantle and core of the Earth."),
        ("The Transcendents", "You are a hive-mind of pure radiation and information living in Dyson Swarms across the galaxy.")
    ]
    
    for event in events:
        print(f"\n{'='*50}")
        print(f"YEAR {event['year']}: {event['event']}")
        print(f"{event['desc']}")
        print(f"{'='*50}")
        
        for civ_name, civ_desc in civs:
            # The Architects are dead after Year 5 Billion
            if civ_name == "The Architects" and event['year'] == "1 Trillion":
                print(f"\n--- {civ_name} ---")
                print("The Architects were vaporized into plasma when the Sun consumed the Earth 995 Billion years ago. They are silence.")
                continue

            prompt = f"""You are the collective consciousness of {civ_name}. 
{civ_desc}

It is Year {event['year']} of your existence.
COSMIC APOCALYPSE: {event['desc']}

Describe your exact actions to survive this, AND describe the physical/sensory experience of feeling this cosmic event. Make the reader feel the immense scale of your existence and the terror or awe of this moment.
Write exactly 4 sentences in the first person collective ('We')."""

            response = llm_generate(prompt)
            print(f"\n--- {civ_name} ---")
            print(response)

    print("\n==================================================")
    print("THE UNIVERSE HAS ENDED.")
    print("==================================================")

if __name__ == "__main__":
    run_universal_end()
