import spacy

# List of vague temporal words and expressions
vague_temporal_words = [
    "frequently", "periodically", "every so often", "sometimes", "occasionally",
    "often", "regularly", "from time to time", "at times", "once in a while",
    "rarely", "seldom", "usually", "generally", "normally", "typically", "extended time"
]

# List of temporal conjunctions and adverbs
temporal_conjunctions = [
    "before", "after", "during", "simultaneously", "while", "when", "until",
    "once", "since", "as soon as", "whenever"
]

def detect_vague_temporal_words(doc):
    for token in doc:
        if token.text.lower() in vague_temporal_words:
            return True
    return False

def detect_temporal_conjunction_ambiguities(doc):
    for token in doc:
        if token.text.lower() in temporal_conjunctions:
            head = token.head
            if head and head.pos_ in ["VERB", "AUX"]:
                for child in head.children:
                    if child.dep_ in ["advcl", "prep", "mark"] and child != token:
                        return True
    return False

def check_temporal_ambiguity(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    ambiguous_sentences = []

    for sent in doc.sents:
        has_vague_temporal_word = detect_vague_temporal_words(sent)
        has_temporal_conjunction_ambiguity = detect_temporal_conjunction_ambiguities(sent)

        if has_vague_temporal_word or has_temporal_conjunction_ambiguity:
            ambiguous_sentences.append(sent.text)

    return "\n".join(ambiguous_sentences)
