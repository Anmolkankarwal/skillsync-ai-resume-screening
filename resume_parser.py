import re
import PyPDF2
from docx import Document
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')

# ===================================
# STOPWORDS
# ===================================

STOP_WORDS = set(stopwords.words("english"))

# ===================================
# READ PDF
# ===================================

def read_pdf(file):

    text = ""

    pdf_reader = PyPDF2.PdfReader(file)

    for page in pdf_reader.pages:

        extracted = page.extract_text()

        if extracted:

            text += extracted + " "

    return text

# ===================================
# READ DOCX
# ===================================

def read_docx(file):

    text = ""

    document = Document(file)

    for para in document.paragraphs:

        text += para.text + " "

    return text

# ===================================
# CLEAN TEXT
# ===================================

def clean_text(text):

    # LOWERCASE

    text = text.lower()

    # REMOVE SPECIAL CHARACTERS

    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    # REMOVE EXTRA SPACES

    text = re.sub(r"\s+", " ", text)

    # TOKENIZE

    words = text.split()

    # REMOVE STOPWORDS

    filtered_words = [

        word for word in words

        if word not in STOP_WORDS

    ]

    # JOIN BACK

    cleaned = " ".join(filtered_words)

    return cleaned