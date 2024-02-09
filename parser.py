import nltk
from nltk import word_tokenize, pos_tag, WordPunctTokenizer, sent_tokenize
from nltk.corpus import opinion_lexicon
from utils import convert_to_string_labels, load_afinn_sentiment_file
from grammar_generator import GrammarGenerator
from sentiment_analyzer import SentimentAnalyzer
from nltk.grammar import FeatureGrammar
from nltk.parse import FeatureEarleyChartParser
from nltk.tree import Tree
import sys
from contextlib import redirect_stdout

class Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.grammargenerator = GrammarGenerator()

    def parse_sentence(self, sentence, analysis_type):


        # Preprocessing the sentence
        sentence = sentence.strip()
        if sentence.endswith("."):
            sentence = sentence[:-1]
        sentence = sentence.replace("it's", "it is")
        sentence = sentence.replace(":", "")
        sentence = sentence.replace("plot", "")
        print(sentence)
        placeholder = "__HYPHEN__"
        sentence = sentence.replace('-', placeholder)

        tokenizer = WordPunctTokenizer()
        tokens = tokenizer.tokenize(sentence)
        tokens = [token.replace(placeholder, '-') for token in tokens]
        # tokens = [token.replace("'", 'is') for token in tokens]
        # tokens = [token.replace(''s'', '') for token in tokens]



        tagged_tokens = pos_tag(tokens)

        tokens[0] = tokens[0].lower()

        updated_fcfg_string = self.grammargenerator.update_grammar(sentence)
        updated_fcfg = FeatureGrammar.fromstring(updated_fcfg_string)

        parser = FeatureEarleyChartParser(updated_fcfg)

        print("the sentence is going to parse")
        print("tokens", tokens)


        trees = list(parser.parse(tokens))

        for tree in trees:
            convert_to_string_labels(tree)
            # tree.pretty_print()
        sentiment = SentimentAnalyzer().analyze_with_parse_trees(trees)
        print("sentiment: ", sentiment, "analysis_type: ", analysis_type)

        print("Trees are generated")

        # Assuming trees is a list of parse trees



        if trees:
            file_name = "Good.txt" if sentiment == analysis_type else "False.txt"
            with open(file_name, 'a') as file:
                file.write(f"Sentence: {sentence}\n")

                # Redirect stdout to the file
                with redirect_stdout(file):
                    trees[-1].pretty_print()

                file.write("\n\n")
        else:
            with open("False.txt", 'a') as file:
                file.write(f"Sentence: {sentence}\n")
                file.write("No valid parse found.\n\n")


        return sentiment





