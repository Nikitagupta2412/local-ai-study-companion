import requests
import json

def ask_local_ai(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma3:4b",
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json().get("response", "No response generated.")
    else:
        return f"Error: {response.status_code}"

if __name__ == "__main__":
    print("Testing Ollama Connection...")
    print(ask_local_ai("Summarize why local AI is great for student privacy in one sentence."))