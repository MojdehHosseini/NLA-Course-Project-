import re

import nltk
from nltk import sent_tokenize
from nltk.tree import Tree

def custom_sentence_splitter(text):
    # Use NLTK's sentence tokenizer
    sentences = sent_tokenize(text)

    # Additional enhancements :
    # 1. Handle special cases like "Mr." or "Dr." correctly.
    sentences = [re.sub(r'(?<=[a-zA-Z])\.(?=\s|$)', '.\n', s) for s in sentences]

    return sentences

def convert_to_string_labels(tree):
    if isinstance(tree, Tree):
        if isinstance(tree.label(), nltk.FeatStruct):
            tree.set_label(str(tree.label()))
        for subtree in tree:
            convert_to_string_labels(subtree)


def load_afinn_sentiment_file(file_path):
    afinn = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                afinn[parts[0]] = int(parts[1])
    return afinn

def afinn_sentiment(terms, afinn):
    total = 0
    for word in terms:
        total += afinn.get(word, 0)
    return total

def classify_sentiment(score):
    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    else:
        return "neutral"

def adverb_to_adjective(word):
    # Basic rule: remove 'ly'
    if word.endswith("ly"):
        return word[:-2]
    # Add custom rules or a dictionary lookup here if necessary
    return word

