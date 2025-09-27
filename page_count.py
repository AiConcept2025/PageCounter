"""
Utilities to calculate number of page in document
"""
import os
from PyPDF2 import PdfReader
from docx import Document


def selector(file_path: str) -> int:
    _, extension = os.path.splitext(file_path)
    if extension == 'pdf':
        return pdf_page_count(file_path)
    if extension == 'doc' or extension == 'docx':
        return docx_pages_count(file_path)
    return -1


def pdf_page_count(file_path: str) -> int:
    """
    Returns number of pages in PDF doc
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
    """
    doc = Document(file_path)
    page_count = sum(p.contains_page_break for p in doc.paragraphs) + 1
    return page_count


if __name__ == '__main__':
    selector('some_page_path')
