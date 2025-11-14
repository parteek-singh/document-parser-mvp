# extractor.py
import re
from typing import List, Dict, Any

import fitz  # PyMuPDF
import pdfplumber


def is_heading(line: str) -> bool:
    """
    Heuristic to decide whether a line is a heading.
    You can tune this later for your domain.
    """
    line = line.strip()
    if not line:
        return False

    # Very long lines are unlikely to be headings
    if len(line) > 80:
        return False

    # Pattern like "1.", "1.2", "2.3.4 Title"
    numbered_heading = re.match(r"^\d+(\.\d+)*\s+.+", line)
    if numbered_heading:
        return True

    # ALL CAPS (ignoring non-letters)
    letters = re.sub(r"[^A-Za-z]+", "", line)
    if letters and letters.isupper():
        return True

    # Common headings (optional – extend as needed)
    common_headings = [
        "DIRECTORS' REPORT",
        "FINANCIAL STATEMENTS",
        "NOTES TO THE FINANCIAL STATEMENTS",
        "MANAGEMENT DISCUSSION AND ANALYSIS",
        "OUTLOOK",
    ]
    if line.upper() in common_headings:
        return True

    return False


def split_into_sections(full_text: str) -> List[Dict[str, Any]]:
    """
    Split full text into sections by detecting headings.
    Returns list of {heading, content}.
    """
    lines = full_text.splitlines()
    sections: List[Dict[str, Any]] = []

    current_heading = "INTRODUCTION"
    current_lines: List[str] = []

    for line in lines:
        if is_heading(line):
            # Close previous section
            if current_lines:
                sections.append({
                    "heading": current_heading,
                    "content": "\n".join(current_lines).strip()
                })
                current_lines = []

            current_heading = line.strip()
        else:
            current_lines.append(line)

    # Final section
    if current_lines:
        sections.append({
            "heading": current_heading,
            "content": "\n".join(current_lines).strip()
        })

    return sections


def extract_tables(path: str) -> List[Dict[str, Any]]:
    """
    Extract tables from PDF using pdfplumber.
    Returns a list of tables, each with page number and rows.
    """
    tables: List[Dict[str, Any]] = []

    with pdfplumber.open(path) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):
            page_tables = page.extract_tables()
            for t in page_tables:
                # t is a list of rows; each row is a list of cell strings
                tables.append({
                    "page_no": page_no,
                    "rows": t
                })

    return tables


def extract_pdf_text(path: str) -> Dict[str, Any]:
    """
    Extract full text, per-page text, sections, and tables from a PDF.
    """
    doc = fitz.open(path)
    pages = []

    for i, page in enumerate(doc):
        text = page.get_text("text")
        pages.append({
            "page_no": i + 1,
            "text": text
        })

    full_text = "\n\n".join(p["text"] for p in pages)
    sections = split_into_sections(full_text)
    tables = extract_tables(path)

    return {
        "pages": pages,
        "full_text": full_text,
        "page_count": len(pages),
        "sections": sections,
        "tables": tables
    }

# For quick testing
# print(extract_pdf_text("/Users/parteekslathia/Documents/work/ASX/annocements/TESTV1/resource/agl_dividend.pdf"))