# PageCounter & CharCounter

Python utility library for counting pages/frames and characters in document and image files.

## Features

- **Page/Frame Counting**: Count pages in documents or frames in images
- **Character Counting**: Extract and count characters from text-based documents
- **Fast Performance**: Optimized with PyMuPDF (50-60x faster than PyPDF2)
- **Multiple Formats**: Support for common document and image formats

## Supported Formats

### Documents (Page & Character Counting)
- **PDF**: Using PyMuPDF (fast, accurate)
- **DOC/DOCX**: Using python-docx (paragraph text)
- **TXT**: Native Python file reading
- **RTF**: Using striprtf library (1-10ms per file)

### Images (Page/Frame Counting Only)
- **TIFF**: Multi-page support
- **PNG**: Multi-frame support
- **JPG/JPEG**: Single frame (typically)
- **GIF**: Multi-frame support

**Note**: Character counting for images requires OCR (not currently supported)

## Installation

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `docx` - Word document processing
- `lxml` - XML processing
- `pillow` - Image processing
- `PyMuPDF` - Fast PDF text extraction
- `striprtf` - RTF text extraction

## Usage

### Page Counting

```python
from page_count import selector

# Count pages in any supported document
page_count = selector('document.pdf')      # Returns: int (page count)
page_count = selector('document.docx')     # Returns: int (page count)
page_count = selector('image.tiff')        # Returns: int (frame count)

# Returns -1 on error
if page_count == -1:
    print("Error processing file")
```

### Character Counting

```python
from page_count import char_selector

# Count characters in text-based documents
char_count = char_selector('document.pdf')    # Returns: int (character count)
char_count = char_selector('document.docx')   # Returns: int (character count)
char_count = char_selector('document.txt')    # Returns: int (character count)
char_count = char_selector('document.rtf')    # Returns: int (character count)

# Images return -1 (OCR not supported)
char_count = char_selector('image.png')       # Returns: -1

# Returns -1 on error
if char_count == -1:
    print("Error processing file or unsupported format")
```

### Format-Specific Functions

```python
from page_count import (
    # Page counting functions
    pdf_pages_count,
    docx_pages_count,
    txt_pages_count,
    rtf_pages_count,
    tiff_pages_count,
    png_frames_count,
    jpg_frames_count,
    gif_frames_count,

    # Character counting functions
    pdf_char_count,
    docx_char_count,
    txt_char_count,
    rtf_char_count
)

# Use format-specific functions directly
pages = pdf_pages_count('document.pdf')
chars = pdf_char_count('document.pdf')
```

## Character Counting Details

### What Gets Counted
- All visible text characters
- Spaces, tabs, and newlines
- Punctuation marks
- Unicode characters

### Format-Specific Behavior

**PDF (PyMuPDF)**:
- Extracts all visible text from all pages
- Fastest method (40ms for 100-page document)
- May include minor whitespace variations

**DOCX (python-docx)**:
- Counts paragraph text only (fast implementation)
- Does NOT include headers, footers, or tables
- Optimized for maximum performance

**TXT (Native Python)**:
- Reads entire file content
- UTF-8 encoding by default
- Includes all characters including newlines

**RTF (striprtf)**:
- Converts RTF to plain text
- Handles encoding properly (UTF-8/ANSI)
- Skips headers, footers, and image data
- Known limitation: multi-line table cells

## Performance

### Page Counting
- PDF: ~50-100ms per 100-page document
- DOCX: ~100ms per 100-page document
- TXT: ~10ms per 10,000 lines
- Images: ~50ms per multi-page TIFF

### Character Counting
- PDF (PyMuPDF): ~40ms per 100-page document
- DOCX: ~100ms per 100-page document
- TXT: ~10ms per 10KB file
- RTF: ~1-10ms per document

## Error Handling

All functions return `-1` on errors and print error messages:

```python
count = selector('nonexistent.pdf')
# Prints: Error: The specified PDF file was not found: nonexistent.pdf
# Returns: -1
```

**Common Error Cases:**
- File not found
- Permission denied
- Corrupted file
- Unsupported format
- Empty file (returns 0, not -1)

## Examples

```python
from page_count import selector, char_selector

# Process a document
file_path = 'report.pdf'

pages = selector(file_path)
chars = char_selector(file_path)

if pages > 0 and chars > 0:
    print(f"Document has {pages} pages and {chars} characters")
    print(f"Average characters per page: {chars / pages:.0f}")
else:
    print("Error processing document")
```

## Known Issues & Limitations

1. **DOCX page counting**: Uses page breaks, may be inaccurate for complex layouts
2. **DOCX char counting**: Excludes headers, footers, and tables (by design for speed)
3. **RTF char counting**: May have issues with multi-line table cells
4. **Image formats**: Character counting requires OCR (not implemented)
5. **PDF char counting**: May include minor whitespace differences

## Bug Fixes (v1.1)

- Fixed: JPG/JPEG files now correctly route to `jpg_frames_count()` instead of `gif_frames_count()`
- Fixed: RTF page counting now returns `-1` on error (was returning `None`)
- Added: Missing `jpg_frames_count()` function

## Future Enhancements

- OCR support for image character counting (pytesseract)
- Comprehensive DOCX counting (headers, footers, tables)
- Streaming support for very large files
- Async processing for batch operations
- Caching layer for repeated calls

## License

See LICENSE file for details.
