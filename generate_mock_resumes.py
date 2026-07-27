import os
from fpdf import FPDF

RESUMES = {
    "candidate_1_strong_fit.pdf": """
    Alex Rivera - Senior AI Engineer
    Email: alex@example.com | Phone: 555-0192

    Summary:
    Senior Machine Learning Engineer with 4 years of experience building scalable NLP systems and LLM applications.

    Technical Skills:
    Python, PyTorch, Transformers, RAG, Pinecone, FastAPI, Docker, Git, AWS.

    Experience:
    - Led development of enterprise RAG pipelines serving 100k daily queries.
    - Fine-tuned open-source LLMs for medical document processing.
    - Deployed microservices using Docker and GitHub Actions CI/CD.

    Education:
    B.S. in Computer Science - Tech University (2020)
    """,

    "candidate_2_moderate_fit.pdf": """
    Jordan Lee - Software Developer
    Email: jordan@example.com | Phone: 555-0143

    Summary:
    Full-stack developer with 2 years of experience focusing on backend engineering and web APIs.

    Technical Skills:
    Python, JavaScript, Django, Flask, PostgreSQL, Git, Docker, Basic Machine Learning.

    Experience:
    - Built RESTful web endpoints for modern e-commerce platforms.
    - Integrated third-party OpenAI API calls into internal tools.
    - Maintained SQL databases and managed code repositories on Git.

    Education:
    B.Tech in Information Technology (2022)
    """,

    "candidate_3_weak_fit.pdf": """
    Taylor Smith - Graphic Designer & Marketing Specialist
    Email: taylor@example.com | Phone: 555-0188

    Summary:
    Creative designer with 5 years of experience in brand strategy, UI design, and digital content creation.

    Technical Skills:
    Adobe Creative Suite, Photoshop, Illustrator, Figma, HTML, CSS, Copywriting.

    Experience:
    - Designed marketing collateral and social media assets for global brands.
    - Managed digital campaigns achieving 25% growth in user engagement.

    Education:
    B.A. in Graphic Design (2019)
    """
}

os.makedirs("data/sample_resumes", exist_ok=True)
for filename, content in RESUMES.items():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    for line in content.strip().split("\n"):
        pdf.cell(0, 8, line.strip(), new_x="LMARGIN", new_y="NEXT")
    pdf.output(f"data/sample_resumes/{filename}")

print("Sample resumes generated in data/sample_resumes/")