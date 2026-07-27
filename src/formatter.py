import pandas as pd
from rich.console import Console
from rich.table import Table

class ResultFormatter:
    @staticmethod
    def export_to_csv(data: list[dict], output_path: str):
        """Saves ranked candidate results into a CSV file."""
        df = pd.DataFrame(data)
        df.sort_values(by="nlp_similarity_score", ascending=False, inplace=True)
        df.to_csv(output_path, index=False)
        return df

    @staticmethod
    def display_cli_table(df: pd.DataFrame):
        """Renders a beautiful styled table in the terminal."""
        console = Console()
        table = Table(title="🏆 Candidate Ranking - AI Resume Screening Agent", show_header=True)

        table.add_column("Rank", style="bold cyan", justify="center")
        table.add_column("Candidate File", style="bold white")
        table.add_column("NLP Score", style="bold green", justify="right")
        table.add_column("LLM Grade", style="bold yellow")
        table.add_column("Rationale Summary", style="dim white")

        for rank, (_, row) in enumerate(df.iterrows(), start=1):
            table.add_row(
                str(rank),
                str(row["filename"]),
                f"{row['nlp_similarity_score']:.1f}%",
                str(row["qualitative_grade"]),
                str(row["rationale"])
            )

        console.print("\n")
        console.print(table)
        console.print("\n")