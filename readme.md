# 🏆 AI Resume Screening Agent

**ROOMAN AI CHALLENGE - 24-Hour AI Agent Selection Round** *Junior AI Research Associate Track*

This repository contains a working, end-to-end AI Resume Screening Agent built in Python.

> **One-Sentence Summary:** > *"My agent takes a directory of PDF resumes and a Job Description and produces a scored, ranked candidate shortlist using mathematical NLP embeddings and qualitative LLM analysis."*

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
