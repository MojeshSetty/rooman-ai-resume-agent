import os
import tempfile
import streamlit as st
from src.document_parser import DocumentParser
from src.nlp_scorer import NLPScorer
from src.llm_evaluator import LLMEvaluator

# --- Page Config ---
st.set_page_config(page_title="AI Resume Screener", page_icon="📄", layout="wide")
st.title("🏆 AI Resume Screening Agent")
st.markdown("Upload resumes and a Job Description to generate an AI-scored shortlist.")

# --- Sidebar for API Key (Crucial for Cloud Hosting) ---
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Groq API Key", type="password", help="Enter your Groq API key here.")
    st.markdown("*(Get a free key at [console.groq.com](https://console.groq.com))*")

# --- Main UI: Inputs ---
st.subheader("1. Job Description")
job_description = st.text_area("Paste the Job Description here:", height=150)

st.subheader("2. Upload Resumes")
uploaded_files = st.file_uploader("Upload candidate PDFs (< 2MB recommended)", type=["pdf"], accept_multiple_files=True)

# --- Main UI: Processing ---
if st.button("🚀 Run Screening Agent", type="primary"):
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
        st.stop()
    if not job_description:
        st.error("Please provide a Job Description.")
        st.stop()
    if not uploaded_files:
        st.error("Please upload at least one resume.")
        st.stop()

    # Set the API key as an environment variable so your llm_evaluator.py can find it
    os.environ["GROQ_API_KEY"] = api_key

    with st.spinner("Processing documents and running AI models..."):
        # 1. Save uploaded files temporarily (because DocumentParser expects file paths)
        temp_dir = tempfile.mkdtemp()
        resumes_dict = {}
        
        for uploaded_file in uploaded_files:
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Extract text
            extracted_text = DocumentParser.parse_pdf(temp_path)
            resumes_dict[uploaded_file.name] = extracted_text

        # 2. Compute NLP Vector Cosine Similarity
        scorer = NLPScorer()
        similarity_scores = scorer.compute_similarity(job_description, resumes_dict)

        # 3. LLM Qualitative Evaluation
        llm_eval = LLMEvaluator()
        raw_results = []

        for filename, resume_text in resumes_dict.items():
            nlp_score = similarity_scores.get(filename, 0.0)
            llm_result = llm_eval.evaluate_candidate(job_description, resume_text)

            raw_results.append({
                "filename": filename,
                "nlp_score": nlp_score,
                "grade": llm_result.get("qualitative_grade", "N/A"),
                "matched_skills": llm_result.get("matched_skills", []),
                "missing_skills": llm_result.get("missing_skills", []),
                "rationale": llm_result.get("rationale", "No rationale provided.")
            })

        # --- 4. Display Results (Clean UI Makeover) ---
        st.success(f"✅ Screening Complete! Evaluated {len(raw_results)} candidate(s).")
        
        # Sort results by NLP score highest to lowest
        ranked_results = sorted(raw_results, key=lambda x: x["nlp_score"], reverse=True)

        st.divider()
        st.subheader("📊 Candidate Rankings")

        for rank, res in enumerate(ranked_results, start=1):
            # Create a bordered card for each candidate
            with st.container(border=True):
                st.markdown(f"### #{rank}: {res['filename']}")
                
                # Top Section: High-level KPI Cards
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("NLP Match Score", f"{res['nlp_score']:.1f}%")
                with col2:
                    # Color-code the grade
                    grade = res["grade"]
                    if "Strong" in grade:
                        st.success(f"**Qualitative Grade:** {grade}")
                    elif "Moderate" in grade:
                        st.warning(f"**Qualitative Grade:** {grade}")
                    else:
                        st.error(f"**Qualitative Grade:** {grade}")

                # Executive Summary Box
                st.markdown("#### Executive Summary")
                st.info(res["rationale"])

                # Detailed Skills Breakdown
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("#### ✅ Matched Skills")
                    if res["matched_skills"]:
                        for skill in res["matched_skills"]:
                            st.markdown(f"- {skill}")
                    else:
                        st.write("None identified.")

                with col_b:
                    st.markdown("#### ❌ Missing / Gap Areas")
                    if res["missing_skills"]:
                        for skill in res["missing_skills"]:
                            st.markdown(f"- {skill}")
                    else:
                        st.write("None identified.")