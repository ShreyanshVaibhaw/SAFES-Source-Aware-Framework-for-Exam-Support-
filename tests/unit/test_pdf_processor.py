from pathlib import Path

from pypdf import PdfWriter

from src.services.document_processors.pdf_processor import PDFProcessor


def test_validate_pdf_rejects_non_pdf(tmp_path: Path):
    processor = PDFProcessor()
    file_path = tmp_path / "not_pdf.txt"
    file_path.write_text("hello", encoding="utf-8")
    ok, message = processor.validate_pdf(file_path)
    assert not ok
    assert "Expected .pdf" in message


def test_tables_to_text_formats_rows():
    processor = PDFProcessor()
    text = processor._tables_to_text([[["a", "b"], ["c", None]]])
    assert "a | b" in text
    assert "c |" in text


def test_get_document_metadata_basic(tmp_path: Path):
    path = tmp_path / "meta.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    writer.add_metadata({"/Title": "Sample", "/Author": "Tester"})
    with path.open("wb") as fp:
        writer.write(fp)
    processor = PDFProcessor()
    meta = processor.get_document_metadata(path)
    assert meta["title"] == "Sample"
