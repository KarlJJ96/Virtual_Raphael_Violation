import spacy

# List of ambiguous quantity-related words (can be expanded)
ambiguous_quantity_words = [
    "some", "many", "a handful", "enough", "several", "few", "numerous",
    "various", "a lot", "plenty", "a bit", "a little", "a couple", "a number of",
    "a portion", "an amount", "more or less", "roughly", "around", "approximately"
]

def detect_ambiguous_quantity_words(doc):
    for token in doc:
        if token.text.lower() in ambiguous_quantity_words:
            return True
    return False

def check_quantity_ambiguity(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    ambiguous_sentences = []

    for sent in doc.sents:
        has_ambiguous_quantity_word = detect_ambiguous_quantity_words(sent)

        if has_ambiguous_quantity_word:
            ambiguous_sentences.append(sent.text)

    return "\n".join(ambiguous_sentences)
