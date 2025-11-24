# AI Communication Evaluator 🎤

## 🚀 Overview
This tool was built for the Nirmaan AI Internship Case Study. It evaluates student self-introductions using a multi-modal approach combining **Rule-Based Logic**, **NLP (Semantic Analysis)**, and **Linguistics**.

**Live Demo:** [LINK TO YOUR HUGGING FACE SPACE HERE]

## 🧠 Solution Approach
The solution moves beyond simple keyword matching to understand the *intent* of the speaker.

1.  **Content Analysis (Hybrid Approach):**
    * *Rule-Based:* Checks for mandatory structural elements (Salutation, Name).
    * *Semantic NLP:* Uses `sentence-transformers` (BERT) to detect topics like "Ambition" or "Hobbies" even if specific keywords are missing (e.g., "I want to be a pilot" is recognized as an Ambition).
2.  **Linguistic Quality:**
    * Uses `language-tool-python` for granular grammar checking.
    * Calculates Vocabulary Richness (TTR).
3.  **Speech Metrics:**
    * Estimates WPM (Words Per Minute) and analyzes filler word usage for clarity.

## 🛠️ Tech Stack
* **Frontend/Backend:** Streamlit (Python)
* **NLP Models:** `all-MiniLM-L6-v2` (Sentence Transformers), VADER Sentiment
* **Infrastructure:** Deployed on Hugging Face Spaces (running OpenJDK 11)

## 📦 How to Run Locally
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt