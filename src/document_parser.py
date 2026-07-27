import fitz  # PyMuPDF
from pathlib import Path

class DocumentParser:
    @staticmethod
    def parse_pdf(file_path: str) -> str:
        """Extract clean plain text from a PDF file."""
        doc = fitz.open(file_path)
        text = []
        for page in doc:
            page_text = page.get_text("text")
            if page_text:
                text.append(page_text)
        return "\n".join(text).strip()

    @staticmethod
    def load_resumes_from_folder(folder_path: str) -> dict[str, str]:
        """Loads all PDF resumes from a directory."""
        path = Path(folder_path)
        resumes = {}
        for pdf_file in path.glob("*.pdf"):
            extracted_text = DocumentParser.parse_pdf(str(pdf_file))
            if extracted_text:
                resumes[pdf_file.name] = extracted_text
        return resumes