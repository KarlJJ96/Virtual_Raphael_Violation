# -*- coding: utf-8 -*-
"""Virtual_Raphael_Violation_Tool.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1f6bZ2ZtgP9H5h-1s04EJhZt9GnpwNQ2-
"""

!pip install pandas scikit-learn transformers torch tqdm openpyxl PyMuPDF

import torch
from transformers import BertTokenizer, BertForSequenceClassification
import fitz
import re
import string

# Load the saved model and tokenizer
model_save_path = 'bert_model.pt'
tokenizer_save_path = 'bert_tokenizer'

tokenizer = BertTokenizer.from_pretrained(tokenizer_save_path)
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
model.load_state_dict(torch.load(model_save_path))
model.eval()

# Device setup
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Function to classify text
def classify_text(text, model, tokenizer, device):
    encodings = tokenizer(text, truncation=True, padding=True, return_tensors='pt', max_length=512)
    input_ids, attention_mask = encodings['input_ids'].to(device), encodings['attention_mask'].to(device)
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        prediction = torch.argmax(outputs.logits, dim=1)
    return prediction.item()

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    pages_text = []
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text = page.get_text("text")
        pages_text.append(text)
    return pages_text

# Function to remove all punctuation from text
def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

# Function to remove formatting like page numbers and headers/footers
def remove_formatting(text):
    text = re.sub(r'Page \d+ of \d+', '', text)
    text = re.sub(r'Document Code:.*\n', '', text)
    text = re.sub(r'Copyright.*\n', '', text)
    text = re.sub(r'\n{2,}', '\n', text)
    return text

# Function to extract relevant pages between specified headings
def extract_relevant_pages(pages_text):
    start_keywords = ["Introduction", "Purpose"]
    end_keywords = ["Appendices", "Appendix"]
    start_idx = -1
    end_idx = len(pages_text)

    # Find the start index
    for i, text in enumerate(pages_text):
        if any(keyword in text for keyword in start_keywords):
            start_idx = i
            break

    # Find the end index
    for i, text in enumerate(pages_text):
        if any(keyword in text for keyword in end_keywords):
            end_idx = i
            break

    if start_idx == -1:
        start_idx = 0  # Use the entire text if no start keyword is found

    return pages_text[start_idx:end_idx]

# Load and process the procedure guide from a PDF file
pdf_path = 'your_file_here.pdf'
pages_text = extract_text_from_pdf(pdf_path)

# Extract relevant pages
relevant_pages = extract_relevant_pages(pages_text)

# Classify each page and output those classified as 1
classified_pages = []
for page_num, page_text in enumerate(relevant_pages, start=1):
    cleaned_text = remove_formatting(page_text)
    clean_text = remove_punctuation(cleaned_text)
    if clean_text.strip():  # Skip empty pages
        prediction = classify_text(clean_text, model, tokenizer, device)
        if prediction == 1:
            classified_pages.append(f"Page {page_num}\n{page_text}")

# Save the classified pages to a text file
output_file_path = 'High Potential Violation Directives.txt'
with open(output_file_path, 'w') as file:
    for page_text in classified_pages:
        file.write(page_text + "\n")

print(f"Classified pages saved to {output_file_path}")