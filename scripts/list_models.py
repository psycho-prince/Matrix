import os
from google import genai
from google.genai import types

def list_models():
    api_key = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
    client = genai.Client(api_key=api_key)
    
    print("Listing available models...")
    try:
        models = client.models.list()
        for m in models:
            print(f"- {m.name}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_models()
