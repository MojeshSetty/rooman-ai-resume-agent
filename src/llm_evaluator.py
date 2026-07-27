import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMEvaluator:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "your_groq_api_key_here":
            raise ValueError("GROQ_API_KEY is not set in .env file.")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    def evaluate_candidate(self, job_description: str, resume_text: str) -> dict:
        """
        Queries LLM for a qualitative assessment and extracted key skills.
        """
        prompt = f"""
You are an expert technical recruiter evaluating a candidate against a job description.

JOB DESCRIPTION:
{job_description[:1500]}

CANDIDATE RESUME:
{resume_text[:2000]}

Evaluate the fit and return strictly a valid JSON object with these keys:
- "matched_skills": list of top skills matched
- "missing_skills": list of important missing requirements
- "rationale": 2 sentence summary on fit suitability
- "qualitative_grade": "Strong Fit", "Moderate Fit", or "Weak Fit"
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You respond only in valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        try:
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception:
            return {
                "matched_skills": [],
                "missing_skills": [],
                "rationale": "Evaluation parsing error.",
                "qualitative_grade": "N/A"
            }