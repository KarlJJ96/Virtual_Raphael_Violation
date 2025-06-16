import spacy
import nltk
from nltk.corpus import wordnet as wn
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Download necessary NLTK data
nltk.download('wordnet')

# Initialize spaCy model
nlp = spacy.load('en_core_web_sm')

# Initialize BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def get_pos_tags(text):
    doc = nlp(text)
    pos_tags = [(token.text, token.tag_) for token in doc]
    return pos_tags

def get_wordnet_pos(spacy_tag):
    if spacy_tag.startswith('J'):
        return wn.ADJ
    elif spacy_tag.startswith('V'):
        return wn.VERB
    elif spacy_tag.startswith('N'):
        return wn.NOUN
    elif spacy_tag.startswith('R'):
        return wn.ADV
    else:
        return None

def extract_top_synsets(word, pos_tag, top_n=3):
    wn_pos = get_wordnet_pos(pos_tag)
    if wn_pos:
        synsets = wn.synsets(word, pos=wn_pos)
    else:
        synsets = wn.synsets(word)
    return synsets[:top_n]

def encode_sentence(sentence):
    inputs = tokenizer(sentence, return_tensors='pt')
    outputs = model(**inputs)
    return outputs.last_hidden_state

def get_sentence_embedding(sentence):
    embeddings = encode_sentence(sentence)
    return embeddings.mean(dim=1).squeeze().detach().numpy()

def get_definition_embedding(definition):
    return get_sentence_embedding(definition)

def calculate_similarity(embedding1, embedding2):
    return cosine_similarity([embedding1], [embedding2])[0][0]

def check_lexical_ambiguity(text, threshold=0.5):
    pos_tags = get_pos_tags(text)
    ambiguous_sentences = []

    for i, (word, pos_tag) in enumerate(pos_tags):
        synsets = extract_top_synsets(word, pos_tag)
        if len(synsets) > 1:
            sentence = ' '.join([w for w, _ in pos_tags])
            word_embedding = encode_sentence(sentence)[0][i].detach().numpy()

            max_similarity = 0
            for synset in synsets:
                definition = synset.definition()
                definition_embedding = get_definition_embedding(definition)
                similarity = calculate_similarity(word_embedding, definition_embedding)
                if similarity > max_similarity:
                    max_similarity = similarity

            if max_similarity < threshold:
                ambiguous_sentences.append(sentence)

    return "\n".join(ambiguous_sentences)
