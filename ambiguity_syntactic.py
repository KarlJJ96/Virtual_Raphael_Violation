import spacy

def detect_subordinate_clauses(doc):
    subordinate_clauses = 0
    for token in doc:
        if token.dep_ in ["mark", "advcl", "acl"]:
            subordinate_clauses += 1
    return subordinate_clauses

def detect_prepositional_phrase_attachment_ambiguities(doc):
    potential_ambiguities = []
    for token in doc:
        if token.pos_ == "ADP":
            prev_token_1 = token.head
            prev_token_2 = prev_token_1.head if prev_token_1.dep_ != "ROOT" else None
            if prev_token_2 and prev_token_1.dep_ != "ROOT":
                potential_ambiguities.append(token)
    return potential_ambiguities

def check_syntactic_ambiguity(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    ambiguous_sentences = []

    for sent in doc.sents:
        subordinate_clauses = detect_subordinate_clauses(sent)
        prepositional_phrase_ambiguities = detect_prepositional_phrase_attachment_ambiguities(sent)

        if subordinate_clauses > 2 or prepositional_phrase_ambiguities:
            ambiguous_sentences.append(sent.text)

    return "\n".join(ambiguous_sentences)
