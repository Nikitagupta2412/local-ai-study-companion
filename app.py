import os
import streamlit as st
import requests
from pypdf import PdfReader

# Page Configuration
st.set_page_config(page_title="Local AI Study Companion", page_icon="🎓", layout="centered")

st.title("🎓 Local AI Study Companion")
st.write("Upload your study notes (TXT, MD, or PDF) and let your local AI assist you offline & privately!")

# File Uploader Widget
uploaded_file = st.file_uploader("Upload a study note file", type=["txt", "md", "pdf"])

def extract_text(file):
    """Extracts text content from uploaded .txt, .md, or .pdf files."""
    if file.name.endswith('.pdf'):
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    else:
        return file.read().decode("utf-8")

def ask_local_ai(prompt):
    """Communicates with the local Ollama instance."""
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemma3:4b",
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "No response received.")
        return f"Error from Ollama API: {response.status_code}"
    except Exception as e:
        return f"Could not connect to local Ollama server: {e}"

if uploaded_file is not None:
    content = extract_text(uploaded_file)
    st.success(f"Loaded '{uploaded_file.name}' successfully!")
    
    # Study Mode Selection
    study_mode = st.selectbox(
        "Select Study Mode:",
        ["Summarize Notes", "Generate Practice Quiz", "Create Flashcards", "Ask a Custom Question"]
    )
    
    user_question = ""
    if study_mode == "Ask a Custom Question":
        user_question = st.text_input("What question do you have about these notes?")

    # Submit Button
    if st.button("Generate Response"):
        if study_mode == "Ask a Custom Question" and not user_question.strip():
            st.warning("Please type a question before submitting.")
        else:
            with st.spinner("Processing with local model..."):
                if study_mode == "Summarize Notes":
                    prompt = f"Summarize these notes into key concise bullet points:\n\n{content}"
                elif study_mode == "Generate Practice Quiz":
                    prompt = f"Create a 5-question multiple-choice quiz with an answer key based on these notes:\n\n{content}"
                elif study_mode == "Create Flashcards":
                    prompt = f"Extract 5 key concepts as Q&A flashcards from these notes:\n\n{content}"
                else:
                    prompt = f"Based on the following notes, answer this question: '{user_question}'\n\nNotes:\n{content}"
                
                output = ask_local_ai(prompt)
                
                st.markdown("---")
                st.markdown("### 🤖 AI Output")
                st.markdown(output)