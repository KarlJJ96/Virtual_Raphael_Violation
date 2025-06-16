import spacy

def detect_scope_ambiguity(doc):
    for token in doc:
        if token.pos_ == "VERB":
            has_direct_object = any(child.dep_ == "dobj" for child in token.children)
            if not has_direct_object:
                return True
    return False

def check_scope_ambiguity(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    ambiguous_sentences = []

    for sent in doc.sents:
        has_scope_ambiguity = detect_scope_ambiguity(sent)

        if has_scope_ambiguity:
            ambiguous_sentences.append(sent.text)

    return "\n".join(ambiguous_sentences)
