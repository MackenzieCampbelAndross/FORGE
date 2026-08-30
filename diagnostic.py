import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: API Key not found in .env file")
else:
    print(f"✅ Key found: {api_key[:5]}...{api_key[-4:]}")
    
    # Configure directly
    genai.configure(api_key=api_key)
    
    print("\nAttempting to list available models...")
    try:
        count = 0
        for m in genai.list_models():
            count += 1
            if 'generateContent' in m.supported_generation_methods:
                print(f"  • {m.name}")
        
        if count == 0:
            print("\n❌ CONNECTION SUCCESSFUL BUT NO MODELS FOUND.")
            print("This means your API Key works, but it has no permissions.")
            print("Go to https://aistudio.google.com/app/apikey and ensure the key is active.")
            
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")