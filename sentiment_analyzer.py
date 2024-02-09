import nltk
from nltk import word_tokenize, pos_tag, WordPunctTokenizer, sent_tokenize
from nltk.corpus import opinion_lexicon
import re

from utils import load_afinn_sentiment_file, afinn_sentiment, classify_sentiment


class SentimentAnalyzer:
    def __init__(self):
        # Download the opinion lexicon and sentence polarity dataset
        nltk.download('opinion_lexicon')
        nltk.download('sentence_polarity')

        self.positive_words = opinion_lexicon.positive()
        self.negative_words = opinion_lexicon.negative()

        # Format the positive and negative words and store them as attributes
        self.formatted_positive_words = self.format_words_for_grammar(self.positive_words)
        self.formatted_negative_words = self.format_words_for_grammar(self.negative_words)

    # Function to format words for grammar
    def format_words_for_grammar(self, words):
        # Prepare each word to be in the correct format for the grammar
        return '|'.join(f"'{word}'" for word in words)

    def sentiment_value(self, word):

        if word.lower() in self.positive_words:
            return 'positive'
        elif word.lower() in self.negative_words:
            return 'negative'
        else:
            return 'neutral'

    def analyze_sentence(self, sent):
        # Tokenize the sentence
        tokens = word_tokenize(sent)

        # Assign sentiment to each word
        word_sentiments = [(word, self.sentiment_value(word)) for word in tokens]
        # print(word_sentiments)

        # Aggregate sentiment (example: count of negative and positive words)
        neg_count = sum(1 for _, sentiment in word_sentiments if sentiment == 'negative')
        pos_count = sum(1 for _, sentiment in word_sentiments if sentiment == 'positive')

        overall_sentiment = 'negative' if neg_count > pos_count else 'positive' if pos_count > neg_count else 'neutral'
        return overall_sentiment, word_sentiments

    def analyze_with_parse_trees(self, trees):
        # Implementation for analyzing sentiment from parse trees
        sentiment = []  # Initialize sentiment as a list

        if trees:
            for tree in trees:
                # Get sentiment from the root node of the last tree and append to the list
                tree_sentiment = self.get_sentence_sentiment(tree)
                sentiment.append(tree_sentiment)
                # print(tree_sentiment)
                tree_string = tree.pformat(margin=100)
                # print("tree string: ", tree_string)

        # Count positive and negative sentiments
        neg_count = sum(1 for item in sentiment if item == 'negative')
        pos_count = sum(1 for item in sentiment if item == 'positive')
        print("number of positive: ",pos_count,"number of negative: ", neg_count)

        if pos_count > neg_count:
            final_sentiment = "positive"
        elif neg_count > pos_count:
            final_sentiment = "negative"
        else:
            final_sentiment = "neutral"

        print("Final Sentiment:", final_sentiment)
        return final_sentiment

    # Function to extract the sentiment from the root node of the parse tree
    def get_sentence_sentiment(self,tree):
        if not isinstance(tree, nltk.Tree):
            print("Error: 'tree' is not an instance of nltk.Tree")
            return 'neutral'

        # Function to parse individual node label
        def parse_label(label):
            parts = label.split('\n')
            for part in parts:
                if 'SENT' in part:
                    return part.split('=')[1].strip().strip("'[] ")
            return None

        # Extract sentiment from the root node
        sentiment = parse_label(tree.label())
        if sentiment:
            return sentiment
        else:
            print("The 'SENT' key is not in the tree label for the root node.")
            return 'neutral'
    def AFINN_score(self,sentence):
        # Load the AFINN sentiment lexicon
        afinn = load_afinn_sentiment_file("AFINN-111.txt")
        # Assuming the AFINN is already loaded into `afinn`
        correct_predictions = 0


        sentiment_score = afinn_sentiment(sentence.lower().split(), afinn)
        print("sentiment_score: ",sentiment_score)
        predicted_label = classify_sentiment(sentiment_score)
        # print("predicted_label: ", predicted_label)

        return predicted_label,sentiment_score




