from setuptools import setup, find_packages

setup(
    name="pdf_heading_parser",  # Package name
    version="0.1.0",
    packages=find_packages(),  # Automatically find all sub-packages
    install_requires=[
        'PyMuPDF',
        'frontend',
        'fitz',
        'pdfminer.six',
        'beautifulsoup4',
        'pandas',
        'lxml',
        'pytesseract',
        'pdf2image',
        'PyPDF2',
    ],
    entry_points={
        'console_scripts': [
            'pdf_heading_parser=pdf_parser.parser:parser',  # Entry point to call your parser function from command line
        ],
    },
    description="A Python library to parse headings and subheadings from PDF files.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/bansalsahab/Parser",  # GitHub URL if available
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify the required Python version
)
