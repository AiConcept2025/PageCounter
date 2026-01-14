# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

**PageCounter & CharCounter** - Python utility library for counting pages/frames and characters in document and image files. Used in the translation service for billing/pricing based on page and character counts.

**Stack:** Python 3.x, PyMuPDF (fitz), python-docx, Pillow (PIL), striprtf, PyPDF2

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run module directly (example usage)
python page_count.py

# Use as library
from page_count import selector, char_selector
pages = selector('/path/to/document.pdf')
chars = char_selector('/path/to/document.pdf')
```

## Architecture

**Single-file utility** (`page_count.py`) with two routing functions:

| Function | Purpose | Returns |
|----------|---------|---------|
| `selector(file_path)` | Routes to page/frame counting | `int` (count) or `-1` on error |
| `char_selector(file_path)` | Routes to character counting | `int` (count) or `-1` on error |

**Supported Formats:**

| Format | Page Counting | Char Counting | Library Used |
|--------|---------------|---------------|--------------|
| PDF | ✅ `pdf_pages_count()` | ✅ `pdf_char_count()` | PyMuPDF (fitz) |
| DOC/DOCX | ✅ `docx_pages_count()` | ✅ `docx_char_count()` | python-docx |
| TXT | ✅ `txt_pages_count()` | ✅ `txt_char_count()` | native |
| RTF | ✅ `rtf_pages_count()` | ✅ `rtf_char_count()` | striprtf |
| TIFF | ✅ `tiff_pages_count()` | ❌ (needs OCR) | Pillow |
| PNG | ✅ `png_frames_count()` | ❌ (needs OCR) | Pillow |
| JPG/JPEG | ✅ `jpg_frames_count()` | ❌ (needs OCR) | Pillow |
| GIF | ✅ `gif_frames_count()` | ❌ (needs OCR) | Pillow |

**Key Design Patterns:**
- Extension-based dispatch (case-insensitive)
- Consistent error handling: return `-1` on errors, print error messages to stdout
- Text files use line-based pagination (default 50 lines/page)
- RTF uses `\page` control word counting for pages, striprtf for character extraction
- PDF uses PyMuPDF for both page counting and fast text extraction
- Multi-page images (TIFF/PNG/GIF) use PIL frame iteration via `seek()` or `n_frames`
- DOCX character counting uses paragraph text only (excludes headers/footers/tables for speed)

**Known Limitations:**
- DOCX page counting via page breaks may be inaccurate for complex layouts
- DOCX char counting excludes headers, footers, and tables (by design for speed)
- RTF char counting may have issues with multi-line table cells
- Image character counting requires OCR (not implemented)

## Integration Context

This module is located in `/server/app/app-counter/` within the Translator project. It provides document metrics for:
- Billing calculations based on page/character counts
- Document processing workflows
- Translation pricing estimation
