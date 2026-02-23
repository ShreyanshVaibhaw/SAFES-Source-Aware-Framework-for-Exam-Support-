"""Token-aware text chunking for source documents."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import tiktoken

from src.utils.logger import get_logger


@dataclass
class ChunkConfig:
    """Configuration for text chunking."""

    chunk_size: int = 500
    chunk_overlap: int = 50
    min_chunk_size: int = 100
    separators: List[str] = field(default_factory=lambda: ["\n\n", "\n", ". ", " "])


class TextChunker:
    """Split extracted document text into token-bounded chunks."""

    def __init__(self, config: Optional[ChunkConfig] = None) -> None:
        self.config = config or ChunkConfig()
        self.logger = get_logger(__name__)
        self._encoder = tiktoken.get_encoding("cl100k_base")

    def chunk_document(self, pages_data: List[Dict], document_id: str) -> List[Dict]:
        """Chunk all pages of a processed document."""
        chunks: List[Dict] = []
        chunk_index = 0

        for page in pages_data:
            text = (page.get("content") or "").strip()
            page_number = page.get("page_number")
            if not text:
                continue

            sections = self._split_by_sections(text)
            search_start = 0

            for section_title, section_text in sections:
                for piece in self._create_chunks(section_text):
                    start_pos = text.find(piece, search_start)
                    if start_pos < 0:
                        start_pos = search_start
                    end_pos = start_pos + len(piece)
                    search_start = end_pos

                    chunk_id = f"{document_id}_chunk_{chunk_index:04d}"
                    chunks.append(
                        {
                            "chunk_id": chunk_id,
                            "document_id": document_id,
                            "content": piece.strip(),
                            "page_number": page_number,
                            "section_title": section_title,
                            "token_count": self.count_tokens(piece),
                            "start_char": start_pos,
                            "end_char": end_pos,
                            "metadata": {
                                "page_number": page_number,
                                "section_title": section_title,
                                "start_position": start_pos,
                            },
                        }
                    )
                    chunk_index += 1

        return chunks

    def _split_by_sections(self, text: str) -> List[Tuple[str, str]]:
        """Split text into section-aware blocks."""
        lines = text.splitlines()
        sections: List[Tuple[str, List[str]]] = []
        current_title = "General"
        current_lines: List[str] = []

        header_patterns = [
            re.compile(r"^\s{0,3}#{1,6}\s+(.+)$"),
            re.compile(r"^\s*\d+(\.\d+)*\s+(.+)$"),
            re.compile(r"^[A-Z][A-Z0-9\s\-]{4,}$"),
        ]

        def flush() -> None:
            nonlocal current_lines
            if current_lines:
                sections.append((current_title, current_lines))
                current_lines = []

        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                current_lines.append("")
                continue

            matched_title: Optional[str] = None
            for pattern in header_patterns:
                m = pattern.match(line)
                if not m:
                    continue
                if m.groups():
                    matched_title = m.group(m.lastindex or 1).strip()
                else:
                    matched_title = line
                break

            if matched_title and len(current_lines) > 0:
                flush()
                current_title = matched_title
            elif matched_title and not current_lines:
                current_title = matched_title
            else:
                current_lines.append(raw_line)

        flush()

        if not sections:
            return [("General", text)]

        merged: List[Tuple[str, str]] = []
        pending_title, pending_text = sections[0][0], "\n".join(sections[0][1]).strip()
        for title, lines_block in sections[1:]:
            block_text = "\n".join(lines_block).strip()
            if self.count_tokens(pending_text) < self.config.min_chunk_size:
                pending_text = (pending_text + "\n\n" + block_text).strip()
                pending_title = f"{pending_title} / {title}"
            else:
                merged.append((pending_title, pending_text))
                pending_title = title
                pending_text = block_text
        merged.append((pending_title, pending_text))
        return merged

    def _create_chunks(self, text: str) -> List[str]:
        """Create overlapping chunks from section text."""
        text = text.strip()
        if not text:
            return []
        if self.count_tokens(text) <= self.config.chunk_size:
            return [text]

        token_ids = self._encoder.encode(text)
        chunk_size = self.config.chunk_size
        overlap = min(self.config.chunk_overlap, max(0, chunk_size - 1))
        step = max(1, chunk_size - overlap)

        output: List[str] = []
        for start in range(0, len(token_ids), step):
            end = start + chunk_size
            piece_ids = token_ids[start:end]
            if not piece_ids:
                continue
            piece = self._encoder.decode(piece_ids).strip()
            if not piece:
                continue
            if output and self.count_tokens(piece) < self.config.min_chunk_size:
                output[-1] = (output[-1] + " " + piece).strip()
            else:
                output.append(piece)
            if end >= len(token_ids):
                break

        return output

    def _get_overlap_text(self, previous_chunk: str) -> str:
        """Return the overlap tail text from the previous chunk."""
        ids = self._encoder.encode(previous_chunk)
        if not ids:
            return ""
        overlap_ids = ids[-self.config.chunk_overlap :]
        return self._encoder.decode(overlap_ids).strip()

    def count_tokens(self, text: str) -> int:
        """Count tokens for input text."""
        if not text:
            return 0
        return len(self._encoder.encode(text))

    def _find_best_split_point(self, text: str, target_length: int) -> int:
        """Find split point near target length favoring natural boundaries."""
        if not text:
            return 0
        target_length = max(1, min(target_length, len(text)))
        window = text[:target_length]
        for sep in self.config.separators:
            idx = window.rfind(sep)
            if idx > 0:
                return idx + len(sep)
        return target_length
