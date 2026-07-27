from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class NLPScorer:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Lightweight, fast embeddings model (~80MB download)
        self.model = SentenceTransformer(model_name)

    def compute_similarity(self, job_description: str, resumes: dict[str, str]) -> dict[str, float]:
        """
        Computes Cosine Similarity between Job Description embedding
        and candidate resume embeddings. Returns scores scaled 0 - 100.
        """
        if not resumes:
            return {}

        jd_embedding = self.model.encode([job_description])
        resume_filenames = list(resumes.keys())
        resume_texts = [resumes[fn] for fn in resume_filenames]

        resume_embeddings = self.model.encode(resume_texts)
        similarities = cosine_similarity(jd_embedding, resume_embeddings)[0]

        results = {}
        for filename, score in zip(resume_filenames, similarities):
            # Scale similarity to 0 - 100 percentage
            scaled_score = round(float(np.clip(score, 0, 1) * 100), 2)
            results[filename] = scaled_score

        return results
    