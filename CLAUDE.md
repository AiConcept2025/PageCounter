# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

**PageCounter** - Python utility library for counting pages/frames in document and image files.

**Stack:** Python 3.x, PyPDF2, python-docx, Pillow (PIL)

**Supported Formats:**
- Documents: PDF, DOC/DOCX, TXT, RTF
- Images: TIFF, PNG, JPG/JPEG (multi-frame/multi-page)

## Architecture

**Single-file utility** (`page_count.py`):
- `selector(file_path)` - Main entry point that routes to format-specific handlers based on file extension
- Format handlers return page count as `int` or `-1` on error
- Each handler follows pattern: open file → count pages/frames → return count or -1

**Key Design Patterns:**
- Extension-based dispatch (case-insensitive)
- Consistent error handling: return `-1` on errors, print error messages to stdout
- Text files use line-based pagination (default 50 lines/page)
- RTF uses `\page` control word counting
- Multi-page images (TIFF/PNG/GIF) use PIL frame iteration via `seek()`

**Known Issues:**
- Line 26: `gif_frames_count()` called for JPG/JPEG (should likely be `jpg_frames_count()` or similar)
- RTF handler returns `None` on error (inconsistent with other handlers returning `-1`)
- DOCX page counting via page breaks may be inaccurate for complex layouts

## Setup & Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run module directly (example usage)
python page_count.py

# Use as library
from page_count import selector
page_count = selector('/path/to/document.pdf')
```

## Testing Approach

No test suite currently exists. When adding tests:
- Test each format handler with valid files
- Test error cases (missing files, corrupted files, unsupported formats)
- Verify edge cases (empty files, single-page docs, multi-page TIFF)
- Test `selector()` routing logic for all extensions (including case variations)

## Integration Context

This module is located in `/server/app/app-counter/` within a larger translation service project. It's used as a utility for document processing workflows, likely for billing/pricing based on page counts.
