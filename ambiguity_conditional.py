import spacy

# List of conditional and disjunctive conjunctions
conditional_conjunctions = ["if", "when", "unless", "as long as", "provided that", "in case"]
disjunctive_conjunctions = ["or", "either"]

def detect_conditional_conjunctions(doc):
    for token in doc:
        if token.text.lower() in conditional_conjunctions:
            return True
    return False

def detect_disjunctive_conjunctions(doc):
    for token in doc:
        if token.text.lower() in disjunctive_conjunctions:
            return True
    return False

def detect_nested_conditions(doc):
    condition_count = 0
    for token in doc:
        if token.text.lower() in conditional_conjunctions:
            condition_count += 1
        if condition_count > 1:
            return True
    return False

def check_conditional_ambiguity(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    ambiguous_sentences = []

    for sent in doc.sents:
        has_conditional_conjunction = detect_conditional_conjunctions(sent)
        has_disjunctive_conjunction = detect_disjunctive_conjunctions(sent)
        has_nested_conditions = detect_nested_conditions(sent)

        if has_conditional_conjunction and (has_disjunctive_conjunction or has_nested_conditions):
            ambiguous_sentences.append(sent.text)

    return "\n".join(ambiguous_sentences)
