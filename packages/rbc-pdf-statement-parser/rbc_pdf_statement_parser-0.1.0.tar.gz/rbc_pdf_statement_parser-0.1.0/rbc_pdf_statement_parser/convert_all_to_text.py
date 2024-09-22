"""Convert all PDF files in a directory to text files."""

import pathlib
import sys
from pathlib import Path

import pymupdf


def convert_to_text(input_file: Path, output_file: Path) -> None:
    """Convert a PDF file to text and save it to a text file."""
    with pymupdf.open(input_file) as doc:
        text = "\n".join([page.get_text() for page in doc])

    pathlib.Path(output_file).write_bytes(text.encode())


def main() -> None:
    """Convert all PDF files in a directory to text files."""
    input_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    for pdf_file in input_dir.glob("**/*.pdf"):
        text_file = output_dir / (pdf_file.stem + ".txt")
        convert_to_text(pdf_file, text_file)


if __name__ == "__main__":
    main()
