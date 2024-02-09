from nltk.corpus import sentence_polarity
import nltk
from nltk.corpus import sentence_polarity
from grammar_generator import GrammarGenerator
from sentiment_analyzer import SentimentAnalyzer
from parser import Parser
from utils import custom_sentence_splitter
from nltk.corpus import movie_reviews

def main():
    # Load sentences from the provided data file
    file_path = 'Data.txt'  # Replace with the path to your data file
    with open(file_path, 'r') as file:
        data_sentences = file.readlines()

    # Assuming each line in the file is a separate sentence
    # Optionally, you could apply custom_sentence_splitter if the file contains longer texts
    sentences = [sentence.strip() for sentence in data_sentences]

    # Create an instance of the SentimentAnalyzer class
    sentiment_analyzer = SentimentAnalyzer()

    correct_predictions = 0

    # Process each sentence in the file
    for sentence in sentences:
        print("Generating grammar for the sentence...")
        grammar = GrammarGenerator().update_grammar(sentence)

        print("Parsing the sentence...")
        # Assuming analysis_type is known; modify as needed
        analysis_type = 'negative'

        true_label = Parser(grammar).parse_sentence(sentence, analysis_type)

        # Predict sentiment using SentimentAnalyzer
        predicted_label, sentiment_score = sentiment_analyzer.AFINN_score(sentence)

        # Write results to file
        with open("affin", 'a') as file:
            file.write(f"Sentence: {sentence}\n")
            file.write(f"True label: {true_label}\n")
            file.write(f"Predicted label: {predicted_label}\n")
            file.write(f"Sentiment score: {sentiment_score}\n")

        if predicted_label == true_label:
            correct_predictions += 1

    # Calculate and print accuracy
    accuracy = correct_predictions / len(sentences)
    print("Accuracy:", accuracy)

    with open("affin", 'a') as file:
        file.write(f"Accuracy: {accuracy}\n")
        file.write("\n\n")

if __name__ == "__main__":
    main()
