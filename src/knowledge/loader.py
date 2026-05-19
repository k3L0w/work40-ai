from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


DEFAULT_CHUNK_SIZE = 650
DEFAULT_CHUNK_OVERLAP = 120


@dataclass(frozen=True)
class KnowledgeDocument:
    title: str
    content: str
    source_path: str
    source_filename: str
    chunk_index: int


def load_documents(
    path: Path,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[KnowledgeDocument]:
    documents: list[KnowledgeDocument] = []
    for file_path in sorted(path.glob("*.md")):
        content = file_path.read_text(encoding="utf-8").strip()
        if not content:
            continue
        title = extract_title(content, file_path.stem)
        chunks = split_markdown_text(
            content,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        for index, chunk in enumerate(chunks):
            documents.append(
                KnowledgeDocument(
                    title=title,
                    content=chunk,
                    source_path=str(file_path),
                    source_filename=file_path.name,
                    chunk_index=index,
                )
            )
    return documents


def split_markdown_text(
    content: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    normalized = "\n".join(line.rstrip() for line in content.splitlines()).strip()
    if not normalized:
        return []

    chunks: list[str] = []
    start = 0
    text_length = len(normalized)
    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = normalized[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == text_length:
            break
        start = end - chunk_overlap
    return chunks


def extract_title(content: str, fallback: str) -> str:
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped.removeprefix("# ").strip()
    return fallback.replace("-", " ").title()
