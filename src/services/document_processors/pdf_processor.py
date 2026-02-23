"""PDF extraction utilities with page-level metadata."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import pdfplumber
from pypdf import PdfReader

from src.utils.logger import get_logger


class PDFProcessor:
    """Extract text, tables, and metadata from PDF files."""

    def __init__(self) -> None:
        self.supported_extensions = [".pdf"]
        self.logger = get_logger(__name__)

    def extract_text_with_metadata(self, file_path: Path) -> List[Dict]:
        """Extract text and metadata page-by-page."""
        output: List[Dict] = []
        with pdfplumber.open(file_path) as pdf:
            total = len(pdf.pages)
            for page_idx, page in enumerate(pdf.pages, start=1):
                try:
                    text = page.extract_text() or ""
                    tables = page.extract_tables() or []
                    table_text = self._tables_to_text(tables)
                    page_content = text.strip()
                    if table_text:
                        page_content = f"{page_content}\n\n[TABLES]\n{table_text}".strip()

                    output.append(
                        {
                            "page_number": page_idx,
                            "content": page_content,
                            "tables": table_text,
                            "has_images": bool(page.images),
                        }
                    )
                except Exception as exc:  # pragma: no cover - library dependent
                    self.logger.warning(
                        f"Failed to extract page {page_idx}/{total} from {file_path.name}: {exc}"
                    )
                    output.append(
                        {
                            "page_number": page_idx,
                            "content": "",
                            "tables": "",
                            "has_images": False,
                            "error": str(exc),
                        }
                    )
        return output

    def _tables_to_text(self, tables: List) -> str:
        """Convert extracted table rows into pipe-delimited text."""
        lines: List[str] = []
        for table in tables or []:
            for row in table or []:
                cells = [(cell or "").strip().replace("\n", " ") for cell in row]
                lines.append(" | ".join(cells))
            if table:
                lines.append("")
        return "\n".join(line for line in lines if line is not None).strip()

    def get_document_metadata(self, file_path: Path) -> Dict:
        """Return common PDF metadata fields."""
        reader = PdfReader(str(file_path))
        metadata = reader.metadata or {}
        return {
            "title": getattr(metadata, "title", None) or metadata.get("/Title"),
            "author": getattr(metadata, "author", None) or metadata.get("/Author"),
            "subject": getattr(metadata, "subject", None) or metadata.get("/Subject"),
            "creator": getattr(metadata, "creator", None) or metadata.get("/Creator"),
            "page_count": len(reader.pages),
            "creation_date": metadata.get("/CreationDate"),
        }

    def extract_images_info(self, file_path: Path) -> List[Dict]:
        """Return summary information about images in each page."""
        image_data: List[Dict] = []
        with pdfplumber.open(file_path) as pdf:
            for page_idx, page in enumerate(pdf.pages, start=1):
                images = page.images or []
                dimensions = [
                    {"width": int(img.get("width", 0)), "height": int(img.get("height", 0))}
                    for img in images
                ]
                image_data.append(
                    {
                        "page_number": page_idx,
                        "image_count": len(images),
                        "dimensions": dimensions,
                    }
                )
        return image_data

    def validate_pdf(self, file_path: Path) -> Tuple[bool, str]:
        """Validate that the file is a readable, non-encrypted PDF with text."""
        if not file_path.exists():
            return False, "File not found."
        if file_path.suffix.lower() != ".pdf":
            return False, "Unsupported extension. Expected .pdf."

        try:
            reader = PdfReader(str(file_path))
            if reader.is_encrypted:
                return False, "PDF is encrypted/password protected."
            if len(reader.pages) == 0:
                return False, "PDF has no pages."

            text_found = False
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages[: min(3, len(pdf.pages))]:
                    if (page.extract_text() or "").strip():
                        text_found = True
                        break
            if not text_found:
                return False, "PDF appears to contain no extractable text."
        except Exception as exc:
            return False, f"Invalid PDF: {exc}"

        return True, ""
