import os
import requests
from pypdf import PdfReader

def read_file(file_path):
    """Reads text from .txt, .md, or .pdf files."""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return None

    # Handle PDF files
    if file_path.endswith('.pdf'):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    # Handle TXT and MD files
    elif file_path.endswith('.txt') or file_path.endswith('.md'):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    else:
        print("Unsupported file format. Please use .pdf, .md, or .txt.")
        return None

def ask_local_ai(prompt):
    """Sends prompt to local Ollama API endpoint."""
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma3:4b",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "No response generated.")
        else:
            return f"Error from Ollama API: {response.status_code}"
    except Exception as e:
        return f"Could not connect to Ollama: {e}"

if __name__ == "__main__":
    # Test with any file in your notes folder
    notes_path = "notes/sample_study_notes.txt"
    
    content = read_file(notes_path)
    if content:
        print(f"Reading file '{notes_path}' and sending to Ollama...")
        prompt = f"Please summarize the following study material into key takeaways:\n\n{content}"
        summary = ask_local_ai(prompt)
        print("\n--- AI Summary ---")
        print(summary)