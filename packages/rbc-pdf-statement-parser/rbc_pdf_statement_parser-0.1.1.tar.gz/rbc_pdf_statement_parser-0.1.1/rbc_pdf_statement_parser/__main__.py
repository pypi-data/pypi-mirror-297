"""CLI-like entry point for running as a module.

For example:
```bash
python -m rbc_pdf_statement_parser
```
"""

from .convert_all_to_table import main

if __name__ == "__main__":
    main()
