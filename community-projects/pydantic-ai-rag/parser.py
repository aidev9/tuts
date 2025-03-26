#from llama_cloud_services import LlamaParse
from llama_parse import LlamaParse
import os
from dotenv import load_dotenv

import PyPDF2
import io

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download NLTK resources if needed
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Downloading NLTK resources...")
    nltk.download('punkt')
    nltk.download('stopwords')

# Load environment variables from .env file
load_dotenv()

def clean_text(text):
    cleaned_text = text
    
    # Replace multiple spaces with single space
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    # Remove whitespace at the beginning and end of lines
    cleaned_text = re.sub(r'^\s+|\s+$', '', cleaned_text, flags=re.MULTILINE)
    
    # Keep only alphanumeric, spaces, and basic punctuation
    cleaned_text = re.sub(r'[^\w\s.,;:!?()-]', '', cleaned_text)

    # Fix line breaks in the middle of sentences
    cleaned_text = re.sub(r'(?<=[a-z])\n(?=[a-z])', ' ', cleaned_text)
    # Ensure paragraphs are separated by double line breaks
    cleaned_text = re.sub(r'\n{2,}', '\n\n', cleaned_text)

    stop_words = set(stopwords.words('english'))
    words = word_tokenize(cleaned_text)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    cleaned_text = ' '.join(filtered_words)

    return cleaned_text

def parse_pdf(bytes) -> tuple[str, int]:
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(bytes))
    # Get number of pages
    num_pages = len(pdf_reader.pages)
    
    # Extract text from all pages
    all_text = ""
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        all_text += text + "\n\n"

    return clean_text(all_text), num_pages
    


