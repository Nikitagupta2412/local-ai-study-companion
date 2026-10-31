import os
import requests
from pypdf import PdfReader

def read_file(file_path):
    """Reads text from .txt, .md, or .pdf files."""
    if not os.path.exists(file_path):
        print(f"\n❌ Error: File '{file_path}' does not exist.")
        return None

    if file_path.endswith('.pdf'):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    elif file_path.endswith('.txt') or file_path.endswith('.md'):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    else:
        print("\n⚠️ Unsupported file format. Please use .pdf, .md, or .txt.")
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

def main():
    print("==========================================")
    print("       🎓 LOCAL AI STUDY COMPANION       ")
    print("==========================================")
    
    file_path = input("\nEnter the path to your notes file (e.g., notes/sample_study_notes.txt): ").strip()
    content = read_file(file_path)
    
    if not content:
        return

    while True:
        print("\n--- CHOOSE A STUDY MODE ---")
        print("1. 📝 Summarize Notes")
        print("2. ❓ Generate Practice Quiz (5 Questions)")
        print("3. 📇 Create Flashcards (Q&A Pairs)")
        print("4. 💬 Ask a Custom Question")
        print("5. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == '1':
            prompt = f"Summarize the following study material into concise key bullet points:\n\n{content}"
            print("\n⏳ Generating summary...")
            print("\n--- AI Summary ---")
            print(ask_local_ai(prompt))

        elif choice == '2':
            prompt = f"Create a 5-question multiple choice quiz based on these notes. Include an answer key at the bottom:\n\n{content}"
            print("\n⏳ Generating quiz...")
            print("\n--- Practice Quiz ---")
            print(ask_local_ai(prompt))

        elif choice == '3':
            prompt = f"Extract 5 key concepts from these notes and format them as Question/Answer flashcards:\n\n{content}"
            print("\n⏳ Generating flashcards...")
            print("\n--- Flashcards ---")
            print(ask_local_ai(prompt))

        elif choice == '4':
            user_q = input("\nWhat question do you have about these notes? ")
            prompt = f"Based on the following notes, answer this question: '{user_q}'\n\nNotes:\n{content}"
            print("\n⏳ Finding answer...")
            print("\n--- Answer ---")
            print(ask_local_ai(prompt))

        elif choice == '5':
            print("\nHappy studying! Goodbye! 👋\n")
            break
        else:
            print("Invalid choice, please select 1-5.")

if __name__ == "__main__":
    main()