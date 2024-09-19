import dataclasses
import logging
import re
from dataclasses import dataclass
from datetime import datetime
from functools import partial
from typing import List, Callable

from izihawa_textparser.utils import is_banned_section
from izihawa_textutils.utils import remove_markdown
from langchain_core.documents import Document
from unstructured.cleaners.core import clean

from ._text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter


@dataclass
class Chunk:
    document_id: str
    field: str
    chunk_id: int
    title: str
    text: str
    start_index: int
    length: int
    updated_at: int
    issued_at: int | None = None
    type: str | None = None
    language: str | None = None
    issns: list[str] | None = None


@dataclass
class StoredChunk:
    document_id: str
    field: str
    chunk_id: int
    title: str
    start_index: int
    length: int
    updated_at: int
    issued_at: int | None = None
    type: str | None = None
    language: str | None = None
    issns: list[str] | None = None

    def get_unique_id(self):
        return f'{self.document_id}@{self.field}@{self.chunk_id}'


def extract_title_parts(document: dict, split):
    title_parts = []
    if "title" in document:
        title_parts.append(document["title"])
    for hn in range(1, 7):
        if hn_value := split.metadata.get(f"h{hn}"):
            title_parts.append(hn_value)
    return title_parts


def _length_function(remove_tables: bool, text: str):
    cleaned_chunk = remove_markdown(text, remove_tables=remove_tables, escape_brackets=False)
    return len(cleaned_chunk)


def merge_chunks(a: Chunk, b: Chunk) -> Chunk:
    if a.chunk_id > b.chunk_id:
        t = a
        a = b
        b = t
    new_chunk = Chunk(**dataclasses.asdict(a))
    new_chunk.length = b.start_index - a.start_index + b.length
    new_chunk.text = a.text + "\n\n" + b.text
    return new_chunk


def _is_table(text: str):
    return "\\begin{tabular}" in text or (text.startswith("|") and text.endswith("|"))


def _get_language(document: dict):
    return document["languages"][0] if "languages" in document else None


class DocumentChunker:
    def __init__(
        self,
        chunk_size: int = 512,
        max_extra_length: int = 60,
        chunk_overlap: int = 32,
        min_chunk_length: int = 32,
        add_metadata: bool = False,
        add_year: bool = False,
        return_each_line: bool = False,
        remove_tables: bool = False,
        strip_whitespace: bool = False,
        separators: list[str] | None = None,
        length_function: Callable[[str], int] | None = None
    ):
        if separators is None:
            separators = ["\n\n", "\n", " ", ""]
        if length_function is None:
            length_function = partial(_length_function, remove_tables)
        self._text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            keep_separator=True,
            strip_whitespace=strip_whitespace,
            length_function=length_function,
            separators=separators,
        )
        self._markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "h1"),
                ("##", "h2"),
                ("###", "h3"),
                ("####", "h4"),
                ("#####", "h5"),
                ("######", "h6"),
            ],
            return_each_line=return_each_line,
        )
        self._chunk_size = chunk_size
        self._max_extra_length = max_extra_length
        self._chunk_overlap = chunk_overlap
        self._min_chunk_length = min_chunk_length
        self._add_metadata = add_metadata
        self._add_year = add_year
        self._remove_tables = remove_tables
        self._length_function = length_function

    def _is_figure_header(self, text: str, min_chunk_length: int | None = None):
        if min_chunk_length is None:
            min_chunk_length = self._min_chunk_length
        return bool(re.search(r"^[Tt]ab(le|\.)", text)) or self._length_function(text) < min_chunk_length

    def _splits_to_chunks(self, document: dict, field: str, splits):
        chunks = []
        for chunk_id, split in enumerate(splits):
            page_content = str(split.page_content)
            chunk_text = clean(
                remove_markdown(page_content, remove_tables=self._remove_tables, escape_brackets=False),
                extra_whitespace=True,
                dashes=True,
                bullets=True,
                trailing_punctuation=True,
            )
            title_parts = extract_title_parts(document, split)

            chunk = Chunk(
                document_id=document["id"],
                field=field,
                chunk_id=chunk_id,
                start_index=split.metadata["start_index"],
                length=len(page_content),
                issued_at=document.get("issued_at"),
                updated_at=document["updated_at"],
                type=document.get("type"),
                language=_get_language(document),
                title="\n".join(title_parts),
                text=chunk_text,
                issns=document.get("metadata", {}).get("issns"),
            )

            if any(is_banned_section(title_part) for title_part in title_parts):
                continue

            while chunks and (
                (
                    _is_table(chunk.text)
                    and self._is_figure_header(
                        chunks[-1].text, min_chunk_length=self._min_chunk_length
                    )
                )
                or (
                    self._is_figure_header(
                        chunk.text, min_chunk_length=self._min_chunk_length
                    )
                    and _is_table(chunks[-1].text)
                )
            ):
                chunk_length = self._length_function(chunk.text)
                last_chunk_length = self._length_function(chunks[-1].text)
                if chunk_length + last_chunk_length < self._chunk_size:
                    chunk = merge_chunks(chunks[-1], chunk)
                    chunks.pop(len(chunks) - 1)
                else:
                    break
            chunks.append(chunk)

        enriched_chunks = []
        for chunk in chunks:
            chunk_length = self._length_function(chunk.text)
            if chunk_length < self._min_chunk_length:
                continue
            if self._add_metadata and chunk.title:
                spaced_title = " ".join(chunk.title.split("\n"))
                meta_title = f"\nTITLE: {spaced_title}"
                chunk.text += meta_title
                if chunk_length > self._chunk_size:
                    logging.warning(
                        f"Excessive chunk size: ({chunk_length}){chunk.text}"
                    )
            if (
                self._add_year
                and "issued_at" in document
                and document.get("issued_at", -62135596800) != -62135596800
            ):
                issued_at = datetime.fromtimestamp(document["issued_at"], tz=None)
                chunk.text += f"\nYEAR: {issued_at.year}"
            enriched_chunks.append(chunk)
        return enriched_chunks

    def markdown_to_splits(self, text: str) -> list[Document]:
        return self._markdown_splitter.split_text(text)

    def text_to_splits(self, text: str) -> list[Document]:
        return self._text_splitter.split_documents(self.markdown_to_splits(text))

    def text_to_chunks(self, document, field):
        return self._splits_to_chunks(
            document,
            field,
            self.text_to_splits(document.get(field, "")),
        )

    def document_to_chunks(self, document: dict) -> List[Chunk]:
        return [
            *self.text_to_chunks(document, "abstract"),
            *self.text_to_chunks(document, "content"),
        ]

    def splits_to_text(self, splits) -> list[str]:
        previous_header = {}
        text_parts = []
        for split in splits:
            text = ""
            current_header = split.metadata
            for i in range(1, 7):
                h = f"h{i}"
                if previous_header.get(h) == current_header.get(h):
                    continue
                else:
                    for j in range(i, 7):
                        hj = f"h{j}"
                        if hj in current_header:
                            text_parts.append("#" * j + " " + current_header[hj])
                        else:
                            break
                    break
            text += split.page_content
            text_parts.append(text)
            previous_header = current_header
        return text_parts
