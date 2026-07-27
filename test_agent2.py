import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from rich.console import Console
from src.document_parser import DocumentParser
from src.nlp_scorer import NLPScorer
from src.llm_evaluator import LLMEvaluator
from src.formatter import ResultFormatter

console = Console()

def main():
    console.print("[bold blue]🚀 Starting Live Resume Tester...[/bold blue]")

    # 1. Initialize an invisible tkinter window to use the native OS file dialog
    root = tk.Tk()
    root.withdraw() # Hides the main GUI window so we only see the file picker

    console.print("[cyan]Waiting for file selection... (Check your taskbar if the window is hidden)[/cyan]")
    
    # Open the OS file picker
    file_path = filedialog.askopenfilename(
        title="Select a Resume PDF (< 500KB)",
        filetypes=[("PDF Files", "*.pdf")]
    )

    # Handle if the user clicks 'Cancel'
    if not file_path:
        console.print("[red]❌ No file selected. Exiting test.[/red]")
        return

    filename = os.path.basename(file_path)

    # 2. Enforce the strict 2MB (2048KB) file size limit
    file_size_bytes = os.path.getsize(file_path)
    file_size_kb = file_size_bytes / 1024

    if file_size_kb > 2048:
        console.print(f"[bold red]❌ Error: '{filename}' is {file_size_kb:.1f}KB.[/bold red]")
        console.print("[red]Please upload a resume under 2MB to proceed.[/red]")
        return
        
    console.print(f"[bold green]✅ Successfully loaded: {filename} ({file_size_kb:.1f}KB)[/bold green]")

    # 3. Load the target Job Description
    jd_path = "data/job_description.txt"
    if not os.path.exists(jd_path):
        console.print(f"[red]Error: Job description file not found at {jd_path}[/red]")
        return
        
    with open(jd_path, "r", encoding="utf-8") as f:
        job_description = f.read()

    # 4. Run the Agent Pipeline on the single selected file
    console.print("[yellow]🔍 Extracting text from PDF...[/yellow]")
    resume_text = DocumentParser.parse_pdf(file_path)
    
    # We wrap it in a dictionary to match what your NLPScorer module expects
    resumes_dict = {filename: resume_text}

    console.print("[yellow]🧮 Calculating Mathematical NLP similarity...[/yellow]")
    scorer = NLPScorer()
    sim_scores = scorer.compute_similarity(job_description, resumes_dict)

    console.print("[yellow]🤖 Running LLM qualitative reasoning...[/yellow]")
    llm_eval = LLMEvaluator()
    llm_result = llm_eval.evaluate_candidate(job_description, resume_text)

    # 5. Format and display the exact same way your main script does
    ranked_data = [{
        "filename": filename,
        "nlp_similarity_score": sim_scores.get(filename, 0.0),
        "qualitative_grade": llm_result.get("qualitative_grade", "N/A"),
        "matched_skills": ", ".join(llm_result.get("matched_skills", [])),
        "missing_skills": ", ".join(llm_result.get("missing_skills", [])),
        "rationale": llm_result.get("rationale", "")
    }]

    console.print("\n[bold green]✅ Evaluation Complete![/bold green]")
    df = pd.DataFrame(ranked_data)
    ResultFormatter.display_cli_table(df)

if __name__ == "__main__":
    main()