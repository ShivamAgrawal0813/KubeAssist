import os
import logfire

from unstructured.partition.docx import partition_docx
from unstructured.partition.pptx import partition_pptx


def parse_office(file_path: str):
    """Parse DOCX and PPTX documents using format-specific parsers."""

    with logfire.span("Office Document Parsing", filename=file_path):
        try:
            ext = os.path.splitext(file_path)[1].lower()

            logfire.info(f"Starting Office parser for {file_path}")

            if ext == ".docx":
                elements = partition_docx(filename=file_path)

            elif ext == ".pptx":
                elements = partition_pptx(filename=file_path)

            else:
                raise ValueError(f"Unsupported Office format: {ext}")

            full_text = "\n".join(str(el) for el in elements)

            if not full_text.strip():
                logfire.warning(
                    f"Unstructured returned empty text for {file_path}"
                )
            else:
                logfire.info(
                    f"Successfully parsed {len(full_text)} characters "
                    f"from {file_path}"
                )

            return full_text

        except Exception as e:
            logfire.exception(
                f"Office Parser failed for {file_path}: {e}"
            )
            raise