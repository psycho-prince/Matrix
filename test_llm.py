import os
from google import genai
from google.genai import types

def test_gemini():
    api_key = "AQ.Ab8RN6JRqtEKDKb2Gr85wU9RpKvBfom_vpiyfqdNcKmdbuwa6g"
    client = genai.Client(api_key=api_key)
    
    candidate_models = [
        'gemini-3.5-flash-lite',
        'gemini-3.1-flash-lite',
        'gemini-3.1-flash-lite-preview',
        'gemini-2.5-flash',
        'gemini-flash-lite-latest',
        'gemini-flash-latest'
    ]
    
    print("Testing models for free tier availability...\n")
    
    for model_name in candidate_models:
        print(f"Trying model: {model_name}...")
        try:
            response = client.models.generate_content(
                model=model_name,
                contents='Hello! Please reply with a short confirmation that you are online.'
            )
            print("\n✅ Success! Received response:")
            print("-" * 40)
            print(response.text)
            print("-" * 40)
            return  # Stop after the first success
        except Exception as e:
            error_msg = str(e)
            if "RESOURCE_EXHAUSTED" in error_msg or "429" in error_msg:
                print(f"❌ Failed: Quota exceeded/No free tier for {model_name}.")
            else:
                print(f"❌ Failed with error: {error_msg}")

if __name__ == "__main__":
    test_gemini()
