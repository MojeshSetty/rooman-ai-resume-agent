# 🏆 AI Resume Screening Agent

**ROOMAN AI CHALLENGE - 24-Hour AI Agent Selection Round** *Junior AI Research Associate Track*

This repository contains a working, end-to-end AI Resume Screening Agent built in Python.

>  *"My agent takes a directory of PDF resumes and a Job Description and produces a scored, ranked candidate shortlist using mathematical NLP embeddings and qualitative LLM analysis."*

---

## 📦 Project Deliverables Checklist

This project fulfills all required deliverables for the **Resume Screening Agent (Intermediate)** track:
* ✅ **Job Description (JD):** Located at `data/job_description.txt` (or auto-generated via setup script).
* ✅ **Folder of Sample Resumes:** PDF resumes located at `data/sample_resumes/`.
* ✅ **Ranked Output:** Exported to `data/output/ranked_candidates.csv` and rendered in terminal UI.
* ✅ **Scoring Method Note:** Detailed below in the Architecture section and code comments.

---

## 🛠️ Requirements & Setup

### Prerequisites
* Python 3.10+
* Free Groq API Key (get one instantly at [console.groq.com](https://console.groq.com/))

### 1. Environment Setup

Open your terminal in VS Code and run:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
.\venv\Scripts\activate
# On macOS / Linux:
source venv/bin/activate

```

### 2. Install Dependencies

Install the pinned packages:

```bash
pip install -r requirements.txt
```
Note on Dependencies: torch>=2.9.0 and groq>=0.5.0 are configured to prevent system-specific architecture conflicts and httpx version mismatches.

### 3. API Key Configuration

1.Create a .env file in the root project directory (use .env.example as a template).

2.Add your Groq API key:
```Code Snippet
GROQ_API_KEY=your_actual_groq_api_key_here
```
---

## 🚀 How to Run the Agent

### Step 1: Generate Mock Data (If running for the first time)
To populate sample candidate PDFs across various qualification tiers (Strong, Moderate, Weak fit), execute:
```bash
python generate_mock_resumes.py
```
### Step 2: Run the Screening Agent
Execute the main entry point:
```bash
python main.py
```
---
## 📊 Output Examples
When executed, the agent:
1. Renders a color-coded evaluation table directly in the terminal CLI using rich.

2. Generates a structured CSV export at data/output/ranked_candidates.csv.

### Output CSV Structure

