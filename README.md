# NLA_project
# NLA_project: Advanced Sentiment Analysis System

## Project Overview
This project aims to develop an advanced sentiment analysis system that goes beyond traditional models by incorporating feature grammar to handle more complex cases. The enhanced system is specifically tailored to analyze movie reviews, not only determining the overall sentiment but also identifying the stance towards specific named entities mentioned in the text (e.g., actors, directors).

## Objectives
- **Feature Grammar Integration**: Implement feature grammar to enhance understanding and analysis of complex sentence structures and idioms.
- **Baseline Comparison**: Evaluate the performance of the enhanced system against a baseline sentiment analysis model.
- **Stance Identification**: Expand the system's capability to identify the reviewer's stance towards specific named entities in movie reviews.

## Data
- Guided by examples in NLTK data > sentence polarity > rt-polarity.neg.
- Simplified data samples from Project 3, focusing on complex, longer sentences.
- Consultation with the movie reviews dataset in NLTK for further data samples.

## Description
- Extension of feature grammar for NLTK’s Feature-Based Earley’s Chart parser (`FeatureEarleyChartParser`).
- The aim is to develop a grammar with wider coverage, minimal acceptance of ungrammatical information, and integration of sentiment and discourse relation information.
  
## Suggested Coverage
1. Declarative sentences with sentiment-bearing words.
2. Inclusion of relative clauses.
3. Conjunctions (and, or, but) of sentiment-bearing adjectives or nouns.
4. Conjunctions (and, or, but) of sentiment-bearing sentences.

## SSAP Baseline
- Utilization of aFinn Simplest Sentiment Analysis in Python (SSAP).
- Performance recording of SSAP on sentences from Projects 3 and 4.
- Comparison of SSAP with the developed system in both tabular form and error analysis.

## Deliverables
- `Good.txt`: Sentences correctly parsed and labeled by the grammar.
- `False.txt`: Sentences not correctly parsed or labeled.
- Annotated grammar in `.pdf` format.
- Comprehensive report covering all aspects of the project.
- Demo file in `.pdf` format illustrating the program on examples.
