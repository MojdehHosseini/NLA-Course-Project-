import nltk
from nltk.chunk import conlltags2tree, tree2conlltags

# Sample text
text = "Apple Inc. is a company headquartered in Cupertino, California."

# Tokenize and perform POS tagging
tokens = nltk.word_tokenize(text)
pos_tags = nltk.pos_tag(tokens)

# Create IOB tags for NER (default to 'O' for Outside)
iob_tags = [(word, pos, 'O') for word, pos in pos_tags]

# Define a simple rule to identify proper nouns as entities
for i, (word, pos, _) in enumerate(iob_tags):
    if pos in ['NNP', 'NNPS']:
        iob_tags[i] = (word, pos, 'B-PERSON')

# Create a tree from the IOB tags
tree = conlltags2tree(iob_tags)

# Extract NER entities from the tree
iob_tags = tree2conlltags(tree)

# Print the results
for word, pos, ner_tag in iob_tags:
    print(f"{word} ({ner_tag})")
