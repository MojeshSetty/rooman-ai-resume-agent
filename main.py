import os
from src.document_parser import DocumentParser
from src.nlp_scorer import NLPScorer
from src.llm_evaluator import LLMEvaluator
from src.formatter import ResultFormatter
from rich.console import Console

console = Console()

def main():
    console.print("[bold blue]🚀 Starting Resume Screening Agent...[/bold blue]")

    # 1. Load Job Description
    jd_path = "data/job_description.txt"
    if not os.path.exists(jd_path):
        console.print(f"[red]Error: Job description file not found at {jd_path}[/red]")
        return

    with open(jd_path, "r", encoding="utf-8") as f:
        job_description = f.read()

    # 2. Parse Resumes
    resumes_dir = "data/sample_resumes"
    console.print("[yellow]Reading PDF resumes...[/yellow]")
    resumes = DocumentParser.load_resumes_from_folder(resumes_dir)
    if not resumes:
        console.print(f"[red]No PDF resumes found in {resumes_dir}[/red]")
        return

    # 3. Compute NLP Vector Cosine Similarity
    console.print("[yellow]Calculating NLP embedding similarity scores...[/yellow]")
    scorer = NLPScorer()
    similarity_scores = scorer.compute_similarity(job_description, resumes)

    # 4. LLM Qualitative Evaluation
    console.print("[yellow]Running LLM qualitative reasoning...[/yellow]")
    llm_eval = LLMEvaluator()

    ranked_data = []
    for filename, resume_text in resumes.items():
        nlp_score = similarity_scores.get(filename, 0.0)
        llm_result = llm_eval.evaluate_candidate(job_description, resume_text)

        ranked_data.append({
            "filename": filename,
            "nlp_similarity_score": nlp_score,
            "qualitative_grade": llm_result.get("qualitative_grade", "N/A"),
            "matched_skills": ", ".join(llm_result.get("matched_skills", [])),
            "missing_skills": ", ".join(llm_result.get("missing_skills", [])),
            "rationale": llm_result.get("rationale", "")
        })

    # 5. Format & Export
    output_csv = "data/output/ranked_candidates.csv"
    df = ResultFormatter.export_to_csv(ranked_data, output_csv)
    ResultFormatter.display_cli_table(df)

    console.print(f"[bold green]✅ Screening complete! Results saved to: {output_csv}[/bold green]")

if __name__ == "__main__":
    main()