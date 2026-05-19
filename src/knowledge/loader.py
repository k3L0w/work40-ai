from __future__ import annotations

from dataclasses import dataclass, field
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
    category: str = "geral"
    source_type: str = "curated_note"
    last_reviewed: str = ""
    metadata: dict[str, str] = field(default_factory=dict)


def load_documents(
    path: Path,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[KnowledgeDocument]:
    documents: list[KnowledgeDocument] = []
    for file_path in sorted(path.rglob("*.md")):
        raw_content = file_path.read_text(encoding="utf-8").strip()
        if not raw_content:
            continue
        metadata, content = parse_frontmatter(raw_content)
        clean_content = content.strip()
        if not clean_content:
            continue
        title = metadata.get("title") or extract_title(clean_content, file_path.stem)
        chunks = split_markdown_text(
            clean_content,
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
                    category=metadata.get("category", "geral"),
                    source_type=metadata.get("source_type", "curated_note"),
                    last_reviewed=metadata.get("last_reviewed", ""),
                    metadata=metadata,
                )
            )
    return documents


def parse_frontmatter(content: str) -> tuple[dict[str, str], str]:
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, content

    metadata: dict[str, str] = {}
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            body = "\n".join(lines[index + 1 :]).strip()
            return metadata, body
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return {}, content


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
    return fallback.replace("-", " ").replace("_", " ").title()
