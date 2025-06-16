import re
import PyPDF2
import camelot

# Regular expressions
abbreviation_pattern = re.compile(r'\b[A-Z]{2,5}\b')
definition_patterns = [
    re.compile(r'\b([A-Z]{2,5})\s*\(([^)]+)\)'),              
    re.compile(r'\b([^)]+)\s*\(([A-Z]{2,5})\)'),             
    re.compile(r'\b([A-Z]{2,5})\s*-\s*([^.\n]+)'),            
    re.compile(r'\b([^.\n]+)\s*-\s*([A-Z]{2,5})')             
]

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text += page.extractText()
    return text

def extract_tables_from_pdf(pdf_path):
    tables = camelot.read_pdf(pdf_path, pages='all')
    table_texts = []
    for table in tables:
        df = table.df
        table_text = df.to_string(header=False, index=False)
        table_texts.append(table_text)
    return table_texts

def find_abbreviations(text):
    return set(abbreviation_pattern.findall(text))

def find_defined_abbreviations(text):
    definitions = {}
    for pattern in definition_patterns:
        matches = pattern.findall(text)
        for match in matches:
            if len(match) == 2:
                key, value = match
                key = key.strip()
                value = value.strip()
                if abbreviation_pattern.fullmatch(key):
                    definitions[key] = value
                elif abbreviation_pattern.fullmatch(value):
                    definitions[value] = key
    return definitions

def find_undefined_abbreviations_from_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    table_texts = extract_tables_from_pdf(pdf_path)
    full_text = text + " " + " ".join(table_texts)
    
    all_abbrs = find_abbreviations(full_text)
    defined_abbrs = find_defined_abbreviations(full_text)
    
    undefined = all_abbrs - set(defined_abbrs.keys())
    return sorted(undefined)
