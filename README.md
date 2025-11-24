# AI Communication Evaluator 🎤

## 🚀 Overview
This tool was built for the Nirmaan AI Internship Case Study. It acts like an automated teacher that evaluates student self-introductions. Instead of just counting words, it uses AI to understand the **quality** and **meaning** of the speech.

**Live Demo:** [[Try it here]](https://huggingface.co/spaces/deepshikhar23/nirmaan-ai-evaluator)

## 🧠 How It Works
Most simple grading tools fail because they only look for specific keywords. This solution is different because it understands **intent**.

1.  **Content Analysis (Hybrid Approach):**
    * **The Rules:** It checks for basics, like if the student said "Hello" (Salutation).
    * **The AI Brain:** It uses a smart model (BERT) to understand topics. For example, if a student says *"I want to be a pilot,"* the AI knows this counts as an **Ambition**, even if the student didn't use the exact word "Goal."
2.  **Language Quality:**
    * It acts as a grammar checker to find spelling and sentence errors.
    * It measures how rich the student's vocabulary is.
3.  **Speech Metrics:**
    * It calculates how fast the student speaks (Words Per Minute).
    * It detects hesitancy by counting filler words like "um" and "uh."

## 🛠️ Tech Stack
* **Frontend/Backend:** Streamlit (Python)
* **AI Models:** `sentence-transformers` (for understanding meaning), VADER (for checking tone)
* **Hosting:** Deployed on Hugging Face Spaces

## 📦 How to Run Locally
If you want to run this on your own computer, follow these steps:

1.  Clone this repository.
2.  Install the required tools:
    ```bash
    pip install -r requirements.txt
    ```
3.  Launch the application:
    ```bash
    streamlit run app.py
    ```
