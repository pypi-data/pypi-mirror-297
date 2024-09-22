# rbc-pdf-statement-parser
A Python-based parser for RBC Business Account statements

## Usage

1. Collect all PDF account statements in a single folder (not nested).
2. Install this library with `python3 -m pip install rbc_pdf_statement_parser`.
3. Run with `python3 -m rbc_pdf_statement_parser <input_directory> <output_directory>`.

## Features

* Converts each PDF to a CSV of transactions, and a JSON with metadata.
* Creates a single CSV and Parquet which inventories the metadata of each PDF file.
* Creates a single CSV and Parquet of every transaction from every PDF.
