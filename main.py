import requests
import os

def read_study_notes(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    return None

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
    notes_path = "notes/sample_study_notes.txt"
    note_content = read_study_notes(notes_path)
    
    if note_content:
        print("Reading local notes and sending to Ollama...")
        prompt = f"Please summarize these study notes into 3 key bullet points:\n\n{note_content}"
        result = ask_local_ai(prompt)
        print("\n--- AI Summary ---")
        print(result)
    else:
        print(f"Could not find notes file at {notes_path}")