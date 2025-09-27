import os
from PyPDF2 import PdfReader


def selector(file_path: str) -> int:
    _, extension = os.path.splitext(file_path)
    if extension == 'pdf':
        return pdf_page_count(file_path)
    return -1


def pdf_page_count(file_path: str) -> int:
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


if __name__ == '__main__':
    selector('some_page_path')
