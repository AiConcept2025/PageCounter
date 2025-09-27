"""
Utilities to calculate number of page in document
"""
import os
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image


def selector(file_path: str) -> int:
    _, extension = os.path.splitext(file_path)
    if extension == 'pdf':
        return pdf_pages_count(file_path)
    if extension == 'doc' or extension == 'docx':
        return docx_pages_count(file_path)
    if extension == 'txt':
        return txt_pages_count(file_path)
    if extension == 'rtf':
        return rtf_pages_count(file_path)
    if extension == 'tiff':
        return tiff_pages_count(file_path)
    if extension == 'png':
        return png_frames_count(file_path)
    if extension == 'jpg':
        return gif_frames_count(file_path)
    return -1


def pdf_pages_count(file_path: str) -> int:
    """
    Returns number of pages in PDF doc

    Args:
        file_path (str): The path to the text file.

    Returns:
        int: The calculated number of pages.
    """
    try:
        with open('your_pdf_file.pdf', 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            return num_pages
    except FileNotFoundError:
        print('Error: The specified PDF file was not found.')
        return -1
    except Exception as e:
        print(f'An error occurred: {e}')
        return -1


def docx_pages_count(file_path: str) -> int:
    """
    Returns number of page in Word file

    Args:
        file_path (str): The path to the text file.

    Returns:
        int: The calculated number of pages.
    """
    doc = Document(file_path)
    page_count = sum(p.contains_page_break for p in doc.paragraphs) + 1
    return page_count


def txt_pages_count(file_path: str, lines_per_page: int = 50) -> int:
    """
    Counts the number of 'pages' in a plain text file based on a specified
    number of lines per page.

    Args:
        file_path (str): The path to the text file.
        lines_per_page (int): The maximum number of lines to consider a
        single page.

    Returns:
        int: The calculated number of pages.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            line_count = 0
            for _ in file:
                line_count += 1

        if line_count == 0:
            return 0
        else:
            # Calculate pages, ensuring at least one page for non-empty files
            return (line_count + lines_per_page - 1) // lines_per_page
    except FileNotFoundError:
        print(f'Error: File not found at {file_path}')
        return -1
    except Exception as e:
        print(f'An error occurred: {e}')
        return -1


def rtf_pages_count(file_path: str) -> int:
    """
    Returns number of page in Word RTF file based on the '\page' control word.

    Args:
        file_path (str): The path to the text file.

    Returns:
        int: The calculated number of pages.
    """
    try:
        # RTF often uses latin-1
        with open(file_path, 'r', encoding='latin-1') as f:
            content = f.read()
            # Count occurrences of '\page' and add 1 for the first page
            page_count = content.count('\\page') + 1
            return page_count
    except FileNotFoundError:
        print(f'Error: File not found at {file_path}')
        return None
    except Exception as e:
        print(f'An error occurred: {e}')
        return None


def tiff_pages_count(file_path: str) -> int:
    """
    Counts the number of pages in a multi-page TIFF file.

    Args:
        file_path (str): The path to the TIFF file.

    Returns:
        int: The number of pages in the TIFF file, or 0 if an error occurs.
    """
    try:
        img = Image.open(file_path)
        page_count = 0
        while True:
            try:
                img.seek(page_count)
                page_count += 1
            except EOFError:
                break
        return page_count
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return -1
    except Exception as e:
        print(f"An error occurred: {e}")
        return -1


def png_frames_count(file_path: str) -> int:
    """
    Counts the number of pages in a multi-page TIFF file.

    Args:
        file_path (str): The path to the TIFF file.

    Returns:
        int: The number of pages in the TIFF file, or 0 if an error occurs.
    """
    try:
        img = Image.open(file_path)
        frame_count = 0
        while True:
            try:
                img.seek(frame_count)
                frame_count += 1
            except EOFError:
                break
        return frame_count
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return -1


def gif_frames_count(file_path: str) -> int:
    """
    Counts the number of frames (pages) in a GIF image.

    Args:
        gif_path (str): The path to the GIF file.

    Returns:
        int: The number of frames in the GIF.
    """
    try:
        img = Image.open(file_path)
        return img.n_frames
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return -1
    except Exception as e:
        print(f"An error occurred: {e}")
        return -1


if __name__ == '__main__':
    selector('some_page_path')
