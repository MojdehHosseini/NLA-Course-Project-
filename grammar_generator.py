import re
import nltk
from nltk import word_tokenize, pos_tag, WordPunctTokenizer, sent_tokenize
from nltk.corpus import verbnet
from sentiment_analyzer import SentimentAnalyzer
from utils import adverb_to_adjective


class GrammarGenerator:

    def __init__(self):

        # Initializing SentimentAnalyzer to be used in update_fcfg method
        self.sentiment_analyzer = SentimentAnalyzer()
        # self.Utils = utils()

    def update_grammar(self, sentence):
        # Tokenize the sentence into words
        words = word_tokenize(sentence)

        # Replace '__HYPHEN__' in each word
        words = [word.replace('__HYPHEN__', '-') for word in words]

        overall_sentiment, sentiments_list = self.sentiment_analyzer.analyze_sentence(sentence)
        sentiments = dict(sentiments_list)

        # Perform POS tagging to categorize words
        tagged_words = pos_tag(words)

        # Identify singular and plural nouns
        singular_nouns = [word for word, tag in tagged_words if tag == 'NN']
        plural_nouns = [word for word, tag in tagged_words if tag == 'NNS']

        # Initialize lists to store nouns, verbs, adjectives, determiner, and prepositions
        noun_s = []
        noun_p = []
        verb_third = []
        pos_verb = []
        neg_verb = []
        nut_verb = []
        modal_verb = []
        pos_adjectives = []
        neg_adjectives = []
        adjectives = []
        adjComp = []
        pos_adverb = []
        neg_adverb = []
        adverb = []
        advComp = []
        advSupe = []
        determiner = []
        preposition = []
        properNoun = []
        personalPronoun = []
        possessivePronoun = []
        whPronouns = []
        cardinalNumber = []
        coordinatingConjunction = []

        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        # Categorize words based on their POS
        for word, pos in tagged_words:



            # Determine sentiment of the word
            # word_sentiment = self.sentiment_analyzer.sentiment_value(word)




            # Defaulting to 'neutral' if the word is not in the dictionary
            word_sentiment = sentiments.get(word.lower(), 'neutral')


            # Adding the singular and plural nouns for P3
            if pos.startswith('NN') and not pos.endswith('NP') and word not in days_of_week:  # Nouns_singular
                noun_s.append(word.lower())
            elif pos.startswith('NNS') and not pos.endswith('NP') and word not in days_of_week:  # Nouns_plural
                noun_p.append(word.lower())
            elif pos.startswith('NP') and word not in days_of_week:  # ProperNoun
                properNoun.append(word)
            elif pos.startswith('MD'):  # Modal Verb
                modal_verb.append(word)
            # Adding the third-person verbs for P3
            elif pos.startswith('VBZ'):  # Third-person Verbs
                verb_third.append(word)
            elif pos.startswith('VB') and not pos.endswith('Z'):  # Other Forms (including plural)
                if word_sentiment == "positive":
                    pos_verb.append(word.lower())
                elif word_sentiment == "negative":  # Other Forms (including plural)
                    neg_verb.append(word.lower())
                else:
                    nut_verb.append(word.lower())
            elif pos.startswith('J') and not pos.endswith('JR'):  # Adjectives
                if word_sentiment == "positive":
                    # print(word_sentiment)
                    pos_adjectives.append(word.lower())
                elif word_sentiment == "negative":
                    neg_adjectives.append(word.lower())
                else:
                    adjectives.append(word.lower())
            elif pos.startswith('D'):  # Determiner
                determiner.append(word.lower())
            elif pos.startswith('IN'):  # Preposition
                preposition.append(word.lower())
            elif pos.startswith('WP'):  # Wh-pronouns
                whPronouns.append(word.lower())
            elif pos.startswith('PRP') and not pos.endswith('$'):
                personalPronoun.append(word.lower())
            elif pos.startswith('PRP$'):  # PossessivePronoun
                possessivePronoun.append(word.lower())
            elif pos.startswith('RB'):  # Adverb
                # Generating The Sentiment Of ADVERB Based On ADJ
                adj = adverb_to_adjective(word)
                if word != "not" or "n't":
                    if sentiments.get(adj.lower(), 'neutral') == "positive":
                        pos_adverb.append(word.lower())
                    if sentiments.get(adj.lower(), 'neutral') == "negative":
                        neg_adverb.append(word.lower())
                    else:
                        adverb.append(word.lower())
            elif pos.startswith('RBR'):  # Adverb, comparative
                advComp.append(word.lower())
            elif pos.startswith('RBS'):  # Adverb, superlative
                advSupe.append(word.lower())
            elif pos.startswith('CD'):  # Cardinal Number
                cardinalNumber.append(word.lower())
            elif pos.startswith('JJR'):  # Adjective, comparative
                adjComp.append(word.lower())
            elif pos.startswith('CC'):  # Coordinating Conjunction
                coordinatingConjunction.append(word.lower())

        # Extract unique terminals
        Noun_s = set(noun_s)
        Noun_p = set(noun_p)
        Modal_verb = set(modal_verb)
        Verb_third = set(verb_third)
        Verb_pos = set(pos_verb)
        Verb_neg = set(neg_verb)
        Verb_nut = set(nut_verb)
        Adjectives_pos = set(pos_adjectives)
        Adjectives_neg = set(neg_adjectives)
        Adjectives = set(adjectives)
        Determiner = set(determiner)
        Preposition = set(preposition)
        ProperNoun = set(properNoun)
        PossessivePronoun = set(possessivePronoun)
        PersonalPronoun = set(personalPronoun)
        WhPronouns = set(whPronouns)
        Adverb = set(adverb)
        Adverb_pos = set(pos_adverb)
        Adverb_neg = set(neg_adverb)
        AdvComp = set(advComp)
        AdvSupe = set(advSupe)
        CardinalNumber = set(cardinalNumber)
        AdjComp = set(adjComp)
        CoorCon = set(coordinatingConjunction)

        # Extract unique terminals and ensure none are empty
        terminals = [Noun_s, Noun_p, Modal_verb, Verb_third, Verb_pos, Verb_neg, Verb_nut, Adjectives_pos,
                     Adjectives_neg, Adjectives, Determiner, Preposition, ProperNoun, PossessivePronoun,
                     PersonalPronoun, WhPronouns, Adverb,Adverb_pos,Adverb_neg, AdvComp, AdvSupe, CardinalNumber, AdjComp, CoorCon]

        for terminal in terminals:
            if not terminal:
                terminal.add('.')

        # Convert sets back to individual variables for further use
        Noun_s, Noun_p, Modal_verb, Verb_third, Verb_pos, Verb_neg, Verb_nut, Adjectives_pos, Adjectives_neg, Adjectives, Determiner, Preposition, ProperNoun, PossessivePronoun, PersonalPronoun, WhPronouns, Adverb,Adverb_pos,Adverb_neg, AdvComp, AdvSupe, CardinalNumber, AdjComp, CoorCon = terminals

        # Format the extracted words with double quotes and join with a space and pipe
        Noun_s_str = ' | '.join(f'"{word}"' for word in Noun_s)
        Noun_p_str = ' | '.join(f'"{word}"' for word in Noun_p)
        Modal_verb_str = ' | '.join(f'"{word}"' for word in Modal_verb)
        Verb_third_str = ' | '.join(f'"{word}"' for word in Verb_third)
        Verb_str_pos = ' | '.join(f'"{word}"' for word in Verb_pos)
        Verb_str_neg = ' | '.join(f'"{word}"' for word in Verb_neg)
        Verb_str_nut = ' | '.join(f'"{word}"' for word in Verb_nut)
        Adj_str_pos = ' | '.join(f'"{word}"' for word in Adjectives_pos)
        Adj_str_neg = ' | '.join(f'"{word}"' for word in Adjectives_neg)
        Adj_str = ' | '.join(f'"{word}"' for word in Adjectives)
        Det_str = ' | '.join(f'"{word}"' for word in Determiner)
        Pre_str = ' | '.join(f'"{word}"' for word in Preposition)
        Propn_str = ' | '.join(f'"{word}"' for word in ProperNoun)
        PossessivePronoun_str = ' | '.join(f'"{word}"' for word in PossessivePronoun)
        WhPron_str = ' | '.join(f'"{word}"' for word in WhPronouns)
        Adverb_str = ' | '.join(f'"{word}"' for word in Adverb)
        Adverb_pos_str = ' | '.join(f'"{word}"' for word in Adverb_pos)
        Adverb_neg_str = ' | '.join(f'"{word}"' for word in Adverb_neg)
        AdvComp_str = ' | '.join(f'"{word}"' for word in AdvComp)
        AdvSupe_str = ' | '.join(f'"{word}"' for word in AdvSupe)
        CardinalNumber_str = ' | '.join(f'"{word}"' for word in CardinalNumber)
        AdjComp_str = ' | '.join(f'"{word}"' for word in AdjComp)
        CoorCon_str = ' | '.join(f'"{word}"' for word in CoorCon)
        PersonPronoun_str = ' | '.join(f'"{word}"' for word in PersonalPronoun)



        # Print the categorized words
        print("Noun_sing:", Noun_s_str)
        print("Nouns_plu:", Noun_p_str)
        print("Verb_third:", Verb_third_str)
        print("Modal verb:", Modal_verb_str)
        print("Verb_other_pos form:", Verb_str_pos)
        print("Verb_other_neg form:", Verb_str_neg)
        print("Verb_other_nut form:", Verb_str_nut)
        print("Adjectives_pos:", Adj_str_pos)
        print("Adjectives_neg:", Adj_str_neg)
        print("Adjectives:", Adj_str)
        print("determiner:", Det_str)
        print("preposition:", Pre_str)
        print("propernoun:", Propn_str)
        print("Adverb:", Adverb_str)
        print("Adverb_pos:", Adverb_pos_str)
        print("Adverb_neg:", Adverb_neg_str)
        print("Comparative:", AdvComp_str)
        print("Superlative:", AdvSupe_str)
        print("cardinalNumber", CardinalNumber_str)
        print("AdjComp_str", AdjComp_str)
        print("CoorCon_str", CoorCon_str)
        print("PersonPrpnoun_str", PersonPronoun_str)

        grammar=self.create_grammar(Noun_s_str, Noun_p_str, Modal_verb_str, Verb_third_str, Verb_str_pos,
                            Verb_str_neg, Verb_str_nut, Adj_str_pos, Adj_str_neg, Adj_str, Det_str,
                            Pre_str, Propn_str, PossessivePronoun_str, WhPron_str, Adverb_str, Adverb_pos_str,
                            Adverb_neg_str, AdvComp_str, AdvSupe_str, CardinalNumber_str, AdjComp_str, CoorCon_str,
                            PersonPronoun_str)

        print("Grammar is generated")
        # print(grammar)
        return grammar

    def create_grammar(self,Noun_s_str, Noun_p_str, Modal_verb_str, Verb_third_str, Verb_str_pos, Verb_str_neg,
                            Verb_str_nut, Adj_str_pos, Adj_str_neg, Adj_str, Det_str, Pre_str, Propn_str,
                            PossessivePronoun_str, WhPron_str, Adverb_str,Adverb_pos_str,Adverb_neg_str, AdvComp_str, AdvSupe_str,
                            CardinalNumber_str,
                            AdjComp_str, CoorCon_str, PersonPronoun_str):


        # Adverb_str.remove("not","n't")

        # Define your grammar here with sentiment features
        grammar = f"""
                % start S
    
                # Sentence structure
                S[SENT=?s] -> NP[NUM=?n, PERS=?p,SENT=?sn] VP[NUM=?n, PERS=?p, SENT=?s,SUBCAT=?c]
                S[SENT=?s] -> NP[NUM=?nn, PERS=?pp,SENT=?sn] Modal VP[NUM=?n, PERS=?p, SENT=?s,SUBCAT=?c]|NP[NUM=?nn, PERS=?pp,SENT=?sn] Modal Negation VP[NUM=?n, PERS=?p, SENT=?s,SUBCAT=?c]
                S[SENT=?s] -> NP[NUM=?n, PERS=?p, SENT=?s]
            
                
                # Example: For the team [NP], winning [VP] is everything.
                S[SENT = ?s] -> 'for' NP[NUM=?n, PERS=?p, SENT=?sn] COMMA S
                
                # Use of Relative Clause
                S[SENT=?s] -> NP[NUM=?n, PERS=?p,SENT=?s] VP[NUM=?n, PERS=?p, SENT=?s,SUBCAT=?c] RelClause S[SENT=?s]
                S[SENT=?s] -> NP[NUM=?n, PERS=?p,SENT=?s] VP[NUM=?n, PERS=?p, SENT="neutral",SUBCAT=?c] RelClause S[SENT=?s]
                S[SENT=?s] -> NP[NUM=?n, PERS=?p,SENT=?s2] VP[NUM=?n, PERS=?p, SENT=?s,SUBCAT=?c] RelClause S[SENT="neutral"]
                
                # Example: The car, which is parked outside, belongs to my neighbor.
                S[SENT=?s] -> NP[NUM=?n, PERS=?p,SENT=?s2] COMMA RelClause COMMA VP[NUM=?n, PERS=?p, SENT=?s,SUBCAT=?c] 
    
            
                
                # AND
                S[SENT = ?s] -> NP[NUM=?n, PERS=?p, SENT=?s1] VP[NUM=?n, PERS=?p, SENT=?s,SUBCAT=?c] CC[+and] S[SENT = ?s]
                S[SENT = ?s] -> NP[NUM=?n, PERS=?p, SENT=?s1] VP[NUM=?n, PERS=?p, SENT="neutral",SUBCAT=?c] CC[+and] S[SENT = ?s]
                S[SENT = ?s] -> NP[NUM=?n, PERS=?p, SENT=?s1] VP[NUM=?n, PERS=?p, SENT=?s,SUBCAT=?c] CC[+and] S[SENT = "neutral"]
                S[SENT = ?s] -> NP[NUM=?n, PERS=?p, SENT=?s1] VP[NUM=?n, PERS=?p, SENT=?s,SUBCAT=?c] COMMA CC[+and] S[SENT = ?s]
                S[SENT = ?s] -> NP[NUM=?n, PERS=?p, SENT=?s1] VP[NUM=?n, PERS=?p, SENT="neutral",SUBCAT=?c] COMMA CC[+and] S[SENT = ?s]
                S[SENT = ?s] -> NP[NUM=?n, PERS=?p, SENT=?s1] VP[NUM=?n, PERS=?p, SENT=?s,SUBCAT=?c] COMMA CC[+and] S[SENT = "neutral"]
                S[SENT = ?s] -> NP[NUM=?n, PERS=?p, SENT=?s1] VP[NUM=?n, PERS=?p, SENT="neutral",SUBCAT=?c] COMMA [+and] S[SENT = ?s]
                S[SENT = ?s] -> NP[NUM=?n, PERS=?p, SENT=?s1] VP[NUM=?n, PERS=?p, SENT=?s ,SUBCAT=?c] COMMA S[SENT = neutral]
    
                # BUT
                S[SENT = ?s2] -> NP[NUM=?n, PERS=?p, SENT=?sn] VP[NUM=?n, PERS=?p, SENT=?s1,SUBCAT=?c] COMMA CC[+but] S[SENT = ?s2]
                S[SENT = ?s2] -> NP[NUM=?n, PERS=?p, SENT=?sn] VP[NUM=?n, PERS=?p, SENT=?s1,SUBCAT=?c] CC[+but] S[SENT = ?s2]
                # OR
                S[SENT = ?s2] -> NP[NUM=?n, PERS=?p, SENT=?sn] VP[NUM=?n, PERS=?p, SENT=?s1,SUBCAT=?c] CC[+or] S[SENT = ?s2]
                S[SENT = ?s2] -> NP[NUM=?n, PERS=?p, SENT=?sn] VP[NUM=?n, PERS=?p, SENT=?s1,SUBCAT=?c] COMMA CC[+or] S[SENT = ?s2]
                S[SENT = "neutral" ] -> NP[NUM=?n, PERS=?p, SENT=?sn] VP[NUM=?n, PERS=?p, SENT="positive",SUBCAT=?c] CC[+or] S[SENT = "negative"]|NP[NUM=?n, PERS=?p, SENT=?sn] VP[NUM=?n, PERS=?p, SENT="positive",SUBCAT=?c] COMMA CC[+or] S[SENT = "negative"]
                S[SENT = "neutral"] -> NP[NUM=?n, PERS=?p, SENT=?sn] VP[NUM=?n, PERS=?p, SENT="negative",SUBCAT=?c] CC[+or] S[SENT ="positive" ]|NP[NUM=?n, PERS=?p, SENT=?sn] VP[NUM=?n, PERS=?p, SENT="negative",SUBCAT=?c] COMMA CC[+or] S[SENT ="positive" ]
    
                ## Other CC
                S[SENT="positive"] -> S[SENT="positive"] CC[-and, -but, -or] S[SENT="positive"] | S[SENT="positive"] CC[-and, -but, -or] S[SENT="neutral"] | S[SENT="neutral"] CC[-and, -but, -or] S[SENT="positive"]
                S[SENT="negative"] -> S[SENT="negative"] CC[-and, -but, -or] S[SENT="negative"] | S[SENT="negative"] CC[-and, -but, -or] S[SENT=neutral] | S[SENT="neutral"] CC[-and, -but, -or] S[SENT="negative"]
                S[SENT="neutral"] -> S[SENT="neutral"] CC[-and, -but, -or] S[SENT="neutral"]
    
    
                S_THAT[SENT = ?s] -> NP[NUM=?n, PERS=?p, SENT=?sn] VP[NUM=?n, PERS=?p, SENT=?s,SUBCAT=?c] THAT S[SENT=?s]
                
    
            
                # Noun Phrase (NP) structure    
                NP[NUM=?n, PERS=?p, SENT=?s] -> N[NUM=?n, PERS=?p, SENT=?s]|NNP[NUM=?n, PERS=?p]|Det[NUM=?n]|PRP[NUM=?n, PERS=?p]
                NP[NUM=?n, PERS=?p, SENT=?s] -> PosPro NP[NUM=?n, PERS=?p, SENT=?s]| ADVP[SENT=?s2] NP[NUM=?n, PERS=?p, SENT=?s]
                
                # Use of ADJ in NP 
                NP[NUM=?n, PERS=?p, SENT=?s] -> ADJP[SENT=?s] NP[NUM=?n, PERS=?p, SENT=?s2]|ADJP[SENT=?s]
                NP[NUM=?n, PERS=?p, SENT=?s] -> ADJP[SENT=neutral] NP[NUM=?n, PERS=?p, SENT=?s]
                NP[NUM=?n, PERS=?p, SENT=?s] -> Det[NUM=?n] ADJP[SENT=?s] N[NUM=?n, PERS=?p] | N[NUM=?n, PERS=?p] NP[NUM=?n, PERS=?p, SENT=?s]
                
                # Use of ADJ in PP 
                NP[NUM=?n, PERS=?p, SENT=?s] -> Det[NUM=?n] N[NUM=?n, PERS=?p, SENT=?s] | Det[NUM=?n] NP[NUM=?n, PERS=?p, SENT=?s]| Det[NUM=?n] NP[NUM=?n, PER=?p, SENT=?s] PP
                NP[NUM=?n, PERS=?p, SENT=?s] -> NP[NUM=?n, PERS=?p, SENT=?s] OF NP[NUM=?n1, PERS=?p, SENT=?s2]
                NP[NUM=?n, PERS=?p, SENT=neutral] -> NP[NUM=?n, PERS=?p, SENT=positive] OF NP[NUM=?n1, PERS=?p, SENT=negative]|NP[NUM=?n, PERS=?p, SENT=negative] OF NP[NUM=?n, PERS=?p, SENT=positive]
    
                # Use of CC in NP
                NP[NUM=?n, PERS=?p, SENT=?s] -> NP[NUM=?n, PERS=?p, SENT=?s] CC[+and] NP[NUM=?n, PERS=?p, SENT=?s] | NP[NUM=?n, PERS=?p, SENT=neutral] CC[+and] NP[NUM=?n, PERS=?p, SENT=?s] | NP[NUM=?n, PERS=?p, SENT=?s] CC[+and] NP[NUM=?n, PERS=?p, SENT=neutral]
                NP[NUM=?n, PERS=?p, SENT=?s] -> NP[NUM=?n, PERS=?p, SENT=?s] CC[+or] NP[NUM=?n, PERS=?p, SENT=?s1]
                NP[NUM=?n, PERS=?p, SENT="neutral"] -> NP[NUM=?n, PERS=?p, SENT="positive"] CC[+or] NP[NUM=?n, PERS=?p, SENT="negative"] | NP[NUM=?n, PERS=?p, SENT="negative"] CC[+or] NP[NUM=?n, PERS=?p, SENT="positive"]
                NP[NUM=?n, PERS=?p, SENT=?s] -> NP[NUM=?n, PERS=?p, SENT=?s2] CC[+but] NP[NUM=?n, PERS=?p, SENT=?s] | NP[NUM=?n, PERS=?p, SENT=?s2] COMMA CC[+but] NP[NUM=?n, PERS=?p, SENT=?s]
                NP[NUM=?n, PERS=?p, SENT=?s] -> N[NUM=?n, PERS=?p, SENT=?s] COMMA NP[NUM=?n, PERS=?p, SENT=?s]| COMMA NP[NUM=?n, PERS=?p, SENT=?s]|ADJP[SENT=?s] COMMA NP[NUM=?n, PERS=?p, SENT=?s]
                
                # Nymbers
                NP[NUM=?n, PERS=?p, SENT=?s] -> Cardinal NP[NUM=?n, PERS=?p, SENT=?s]|Cardinal[NUM=?n]
                
                # Use of Relative Clause in NP
                NP[NUM=?n, PERS=?p, SENT=?s] -> Det[NUM=?n] NP[NUM=?n, PERS=?p, SENT=?s] RelClause[SENT=?s]
                NP[NUM=?n, PERS=?p, SENT=?s] -> Det[NUM=?n] NP[NUM=?n, PERS=?p, SENT="neutral"] RelClause[SENT=?s]
                NP[NUM=?n, PERS=?p, SENT=?s] -> Det[NUM=?n] NP[NUM=?n, PERS=?p, SENT=?s] RelClause[SENT="neutral"]
    
                # Relative Clause
                RelClause[SENT=?s] -> RelPro NP[NUM=?n, PERS=?p, SENT=?s2] VP[NUM=?n, PERS=?p, SENT=?s,SUBCAT=?c] | RelPro VP[NUM=?n, PERS=?p, SENT=?s,SUBCAT=?c] 
                RelClause[SENT=?s] -> RelPro NP[NUM=?n, PERS=?p, SENT=?s]
                # Example: The company that I work for is opening a new branch.  --- the house in which I live.
                RelClause[SENT=?s] -> Pre RelClause[SENT=?s]|RelPro NP[NUM=?n, PERS=?p, SENT=?s2] VP[NUM=?n, PERS=?p, SENT=?s,SUBCAT=?c] Pre
                
                # need to do: He told me about the summer he spent in Italy, which was the best time of his life. --- The movie we watched last night was very interesting.
                # Relative clause without relative pronoun
    
    
                # Nouns with number and person agreement
                N[NUM=sg, PERS=3, SENT=neutral] -> {Noun_s_str} | 'it' | 'she' | 'he' | 'story'
                N[NUM=pl, PERS=3, SENT=neutral] -> {Noun_p_str} | 'they'|"boys"
                N[NUM=sg, PERS=2, SENT=neutral] -> 'you'
    
    
                ########VERB TENSE
                #### PRESENT TENSE
                ##### Third person
                # V[ROOT=?t, SUBCAT=?s, VFORM='pres', NUM=3, PERS=sg] -> V[ROOT=?t, SUBCAT=?s, VFORM='base', IRREG='PRES-'] 's'
                # 
                # #### Other agreement
                # V[ROOT=?t, SUBCAT=?s, VFORM='pres', NUM=?n, PERS=?p] -> V[ROOT=?t, SUBCAT=?s, VFORM='base', IRREG='PRES-']
                # 
                # #### Present Participle
                # V[ROOT=?t, SUBCAT=?s, VFORM='ing'] -> V[ROOT=?t, SUBCAT=?s, VFORM='base'] 'ing'
                # 
                # #### Plural Nouns
                # N[ROOT=?t, AGR='3p'] -> N[ROOT=?t, AGR='3s', IRREG='PL-'] 's'
                
                
                ###### VERB SUBCAT
                VP[NUM=?n, PERS=?p, SENT=?s2,SUBCAT='_np_pp'] -> V[NUM=?n, PERS=?p, SENT=?s] NP[NUM=?nn, PERS=?pp, SENT=?s2] PP| V[NUM=?n, PERS=?p, SENT=?s] NP[NUM=?nn, PERS=?pp, SENT=?s2] PP ADVP| V[NUM=?n, PERS=?p, SENT=?s] ADVP NP[NUM=?nn, PERS=?pp, SENT=?s2] PP
                VP[NUM=?n, PERS=?p, SENT=?s,SUBCAT='_pp'] -> V[NUM=?n, PERS=?p, SENT=?s] PP|V[NUM=?n, PERS=?p, SENT=?s2] PP ADVP[SENT=?s] | V[NUM=?n, PERS=?p, SENT=?s] ADVP[SENT=?s] PP
                VP[NUM=?n, PERS=?p, SENT=?s2,SUBCAT='_adjp'] -> V[NUM=?n, PERS=?p, SENT=?s] ADJP[SENT=?s2]| V[NUM=?n, PERS=?p, SENT=?s] ADJP[SENT=?s2] ADVP | V[NUM=?n, PERS=?p, SENT=?s] ADVP ADJP[SENT=?s2]
                VP[NUM=?n, PERS=?p, SENT=?s2,SUBCAT='_np_adjp'] -> V[NUM=?n, PERS=?p, SENT=?s] NP[NUM=?nn, PERS=?pp, SENT=?s] ADJP[SENT=?s2] | V[NUM=?nn, PERS=?pp, SENT=?s] NP[NUM=?nn, PERS=?pp, SENT=?s] ADJP[SENT=?s2] ADVP | V[NUM=?nn, PERS=?pp, SENT=?s] ADVP NP[NUM=?nn, PERS=?pp, SENT=?s] ADJP[SENT=?s2]
                VP[NUM=?n, PERS=?p, SENT=?s,SUBCAT='_s:that'] -> V[NUM=?n, PERS=?p, SENT=?s2] S_THAT[SENT=?s]| V[NUM=?n, PERS=?p, SENT=?s2] S_THAT[SENT=?s] ADVP | V[NUM=?n, PERS=?p, SENT=?s2] ADVP[SENT=?s] S_THAT[SENT=?s]
                VP[NUM=?n, PERS=?p, SENT=?s,SUBCAT='none'] -> V[NUM=?n, PERS=?p, SENT=?s]|V[NUM=?n, PERS=?p, SENT=?s2] ADVP [SENT=?s]
                VP[NUM=?n, PERS=?p, SENT=?s2,SUBCAT='_np'] -> V[NUM=?n, PERS=?p, SENT=?s] NP[NUM=?nn, PERS=?pp, SENT=?s2]|V[NUM=?n, PERS=?p, SENT=?s] NP[NUM=?nn, PERS=?pp, SENT=?s2] ADVP[SENT=?s] | V[NUM=?n, PERS=?p, SENT=?s] ADVP NP[NUM=?nn, PERS=?pp, SENT=?s2]
                VP[NUM=?n, PERS=?p, SENT=?s,SUBCAT='_vp:inf'] -> V[NUM=?n, PERS=?p, SENT=?s] VP_INF|V[NUM=?n, PERS=?p, SENT=?s] VP_INF ADVP
                VP[NUM=?n, PERS=?p, SENT=?s,SUBCAT='_np_vp:inf'] -> V[NUM=?n, PERS=?p, SENT=?s] NP[NUM=?nn, PERS=?pp, SENT=?s2] VP_INF[NUM=?n2, PERS=?p2, SENT=?s, SUBCAT=?c2]|V[NUM=?n, PERS=?p, SENT=?s] NP[NUM=?nn, PERS=?pp, SENT=?s2] VP_INF[NUM=?n2, PERS=?p2, SENT=?s, SUBCAT=?c2] ADVP
                VP[NUM=?n, PERS=?p, SENT=?s,SUBCAT='_np_vp:ing'] -> V[NUM=?n, PERS=?p, SENT=?s] NP[NUM=?n, PERS=?p, SENT=?s2] VP_ING[NUM=?n, PERS=?p, SENT=?s2]|V[NUM=?n, PERS=?p, SENT=?s] NP[NUM=?nn, PERS=?pp, SENT=?s2] VP_ING[NUM=?n, PERS=?p, SENT=?s2] ADVP
                VP[NUM=?n, PERS=?p, SENT=?s,SUBCAT='_np_vp:base'] -> V[NUM=?n, PERS=?p, SENT=?s1] NP[NUM=?nn, PERS=?pp, SENT=?s] VP_BASE[NUM=?n2, PERS=?p2, SENT=?s2]|V[NUM=?n, PERS=?p, SENT=?s1] NP[NUM=?nn, PERS=?pp, SENT=?s] VP_BASE[NUM=?n2, PERS=?p2, SENT=?s2] ADVP
                VP[NUM=?n, PERS=?p, SENT='negative',SUBCAT='_to_be_negation'] -> HelperNegation[NUM=?n, PERS=?p, SENT='negative'] NP[NUM=?nn, PERS=?pp, SENT=?s]
                VP[NUM=?n, PERS=?p, SENT='positive',SUBCAT='_to_be_negation'] -> HelperNegation[NUM=?n, PERS=?p, SENT='negative'] NP[NUM=?nn, PERS=?pp, SENT='negative']
    
                
                
                #Verb Negation
                VP[NUM=?n, PERS=?p, SENT='positive',SUBCAT=?c] ->  VerbNegation[NUM=?n, PERS=?p] VP[NUM=?n2, PERS=?p2, SENT='negative',SUBCAT=?c]
                VP[NUM=?n, PERS=?p, SENT='negative',SUBCAT=?c] ->  VerbNegation[NUM=?n, PERS=?p] VP[NUM=?n2, PERS=?p2, SENT='positive',SUBCAT=?c]
                VP[NUM=?n, PERS=?p, SENT='negative',SUBCAT=?c] ->  VerbNegation[NUM=?n, PERS=?p] VP[NUM=?n2, PERS=?p2, SENT='neutral',SUBCAT=?c]
                
    
                # Modal
                VP[NUM=?n, PERS=?p, SENT=?s, SUBCAT=?c] -> Modal VP[NUM=?n, PERS=?p, SENT=?s, SUBCAT=?c]|Modal ADVP[SENT=?s1] VP[NUM=?n, PERS=?p, SENT=?s, SUBCAT=?c]
                
                # Passive
                #  VP[NUM=?n, PERS=?p, SENT=?s, SUBCAT=?c] -> Cop VP[NUM=?n, PERS=?p, SENT=?s, SUBCAT=?c]
                
                                  
                VP_INF[NUM=?n, PERS=?p, SENT=?s, SUBCAT=?c] -> TO VP[NUM=?n, PERS=?p, SENT=?s, SUBCAT=?c]
                VP_ING[NUM=?n, PERS=?p, SENT=?s2] -> V[+ing] NP[NUM=?n, PERS=?p, SENT=?s2]
                VP_BASE[NUM=?n, PERS=?p, SENT=?s2] -> V[NUM=?n, PERS=?p, SENT=?s] NP[NUM=?n, PERS=?p, SENT=?s2]
                
                # Use of CC in VP
                VP[NUM=?n, PERS=?p, SENT=?s, SUBCAT=?c] -> VP[NUM=?n, PERS=?p, SENT=?s, SUBCAT=?c] CC[+and] VP[NUM=?n, PERS=?p, SENT=?s, SUBCAT=?c] | VP[NUM=?n, PERS=?p, SENT="neutral", SUBCAT=?c] CC[+and] VP[NUM=?n, PERS=?p, SENT=?s, SUBCAT=?c]  |VP[NUM=?n, PERS=?p, SENT=?s, SUBCAT=?c] CC[+and] VP[NUM=?n, PERS=?p, SENT="neutral", SUBCAT=?c]
                VP[NUM=?n, PERS=?p, SENT=?s, SUBCAT=?c] -> VP[NUM=?n, PERS=?p, SENT=?s, SUBCAT=?c] CC[+or] VP[NUM=?n, PERS=?p, SENT=?s1, SUBCAT=?c]
                VP[NUM=?n, PERS=?p, SENT="neutral", SUBCAT=?c] -> VP[NUM=?n, PERS=?p, SENT="positive",  SUBCAT=?c] CC[+or] VP[NUM=?n, PERS=?p, SENT="negative", SUBCAT=?c] | VP[NUM=?n, PERS=?p, SENT="negative",  SUBCAT=?c] CC[+or] VP[NUM=?n, PERS=?p, SENT="positive",  SUBCAT=?c]
                VP[NUM=?n, PERS=?p, SENT=?s, SUBCAT=?c] -> VP[NUM=?n, PERS=?p, SENT=?s2, SUBCAT=?c] CC[+but] VP[NUM=?n, PERS=?p, SENT=?s,  SUBCAT=?c] | VP[NUM=?n, PERS=?p, SENT=?s2,  SUBCAT=?c] COMMA CC[+but] VP[NUM=?n, PERS=?p, SENT=?s,  SUBCAT=?c]
                VP[NUM=?n, PERS=?p, SENT=?s,  SUBCAT=?c] -> VP[NUM=?n, PERS=?p, SENT=?s,  SUBCAT=?c] COMMA VP[NUM=?n, PERS=?p, SENT=?s, SUBCAT=?c]| COMMA VP[NUM=?n, PERS=?p, SENT=?s, SUBCAT=?c]
                
                
                # Verbs with number and person agreement
                V[NUM=sg, SENT='neutral'] -> 'was' | 'gave' | 'has'|'is'
                V[NUM=pl, SENT='neutral'] -> 'were' | Cop[NUM=pl, PERS=?p]
                V[NUM=?n, PERS=?p, SENT='positive'] -> {Verb_str_pos}
                V[NUM=?n, PERS=?p, SENT='negative'] -> {Verb_str_neg}
                V[NUM=sg, PERS=3, SENT='neutral'] -> {Verb_third_str}
                V[NUM =?n, PERS=?p, SENT='neutral'] -> {Verb_str_nut}|"drink"
                
                
                VerbNegation[NUM=?n, PERS=?p] -> Helper[NUM=?n, PERS=?p] Negation 
                # This is only for TOBE verb
                HelperNegation[NUM=?n, PERS=?p, SENT='negative'] -> Helper[NUM=?n, PERS=?p] Negation
    
    
    
                    
                # Verb Phrase (VP) structure
                # VP[NUM=?n, PERS=?p, SENT=?s] -> V[NUM=?n, PERS=?p, SENT=?s]
                # VP[NUM=?n, PERS=?p, SENT=?s2] -> V[NUM=?n, PERS=?p, SENT=?s1] NP[NUM=?n, SENT=?s2]
                # VP[NUM=?n, PERS=?p, SENT=?s2] -> V[NUM=?n, PERS=?p, SENT=?s1] Adj[SENT=?s2]
                # VP[NUM=?n, PERS=?p, SENT=?s2] -> V[NUM=?n, PERS=?p, SENT=?s1] P NP[NUM=?n, SENT=?s2]
                # VP[NUM=?n, PERS=?p, SENT=?s] -> Modal V[NUM=?n, PERS=?p, SENT=?s] | Modal V[NUM=?n, PERS=?p, SENT=?s] NP
                # VP[NUM=?n, PERS=?p, SENT=?s2] -> V[NUM=?n, PERS=?p, SENT=?s1] NP Adj[SENT=?s2]
                # VP[NUM=?n, PERS=?p] -> Cop[NUM=?n, PERS=?p] NP
    
    
    
                # Determiners
                Det[NUM=sg] -> 'the' | 'this' | 'that' | 'a' | 'an'|'there'|'such'|'all'
                Det[NUM=pl] ->  'the' | 'these' | 'those'|'there'|'such'|'all'
    
                
                
    
                Negation -> 'not'| "n't"
                Helper[NUM=sg, PERS=3] -> 'does' | 'is' | 'was'|'has'|'may'|'can'|'would'
                Helper[NUM=pl, PERS=?p] -> 'do' | 'are' | 'were'|'have'|'may'|'can'|'would'
    
                # Copula verbs with number and person agreement for "to be"
                Cop[NUM=sg, PERS=3, SENT='neutral'] -> 'is' | 'was'
                Cop[NUM=pl, PERS=?p, SENT='neutral'] -> 'are' | 'were'
                Cop[NUM=sg, PER=1, SENT='neutral'] -> 'am' | 'was'
                
                # Modals
                Modal -> {Modal_verb_str}
                
    
                # Condition
                # Condition -> CompoundAdjective 
    
                # Adjective Phrases with sentiment
                ADJP[SENT=?s] -> Adj[SENT=?s] CC[+and] Adj[SENT=?s] | Adj[SENT=?s] CC[+and] ADJP[SENT=?s]
                ADJP[SENT=?s] -> Adj[SENT=?s] COMMA ADJP[SENT=?s]| Adj[SENT=?s]
                ADJP[SENT=?s] -> Adj CC[+but] Adj[SENT=?s]| Adj CC[+but] ADJP[SENT=?s]
                ADJP[SENT=?s] -> Adj COMMA CC[+but] Adj[SENT=?s] | Adj COMMA CC[+but] ADJP[SENT=?s]
                ADJP[SENT=?s] -> Adj[SENT=?s] CC[+or] Adj[SENT=?s]
                ADJP[SENT=neutral] -> Adj[SENT=positive] CC[+or] Adj[SENT=negative] | Adj[SENT=negative] CC[+or] Adj[SENT=positive]
    
                
                # Example: Highly intelligent
                ADJP[SENT=?s] -> ADVP[SENT=?s2] Adj[SENT=?s]
               
                # Adjective with Negation
                ADJP[SENT=?s] -> Adj[SENT=?s] CC[+but] Negation Adj|ADJP[SENT=?s] CC[+but] Negation Adj|Adj[SENT=?s] CC[+but] Negation ADJP
                ADJP[SENT=?s] -> Adj[SENT=?s] CC[+and] Negation Adj|ADJP[SENT=?s] CC[+and] Negation Adj|Adj[SENT=?s] CC[+and] Negation ADJP
                ADJP[SENT=?s] -> Adj[SENT=?s] CC[+or] Negation Adj|ADJP[SENT=?s] CC[+or] Negation Adj|Adj[SENT=?s] CC[+or] Negation ADJP
                
                
                Adj[SENT='positive'] -> {Adj_str_pos}|'compelling' | {self.sentiment_analyzer.formatted_positive_words} | 'compelling'
                Adj[SENT='negative'] ->   {Adj_str_neg}|{self.sentiment_analyzer.formatted_negative_words} |'low'|'silly'|"dull" | "hazard" | "mess"|"rancid"
                Adj[SENT='neutral'] -> {Adj_str}|"long"
    
    
                # Adverbial Phrase With Sentiment
                ADVP[SENT = ?s] -> adv[SENT = ?s2] adv[ SENT = ?s ]|adv[SENT = ?s]
                ADVP[SENT = ?s] -> adv[SENT = ?s] CC[+and] adv[SENT = ?s ]|adv[SENT = ?s ] CC[+or] adv[SENT = ?s]
                ADVP[SENT='neutral'] -> adv[SENT = 'negative'] CC[+or] adv[SENT = 'positive']|adv[SENT = 'positive'] CC[+or] adv[SENT = 'negative']
                ADVP[SENT=?s2] -> adv[SENT = ?s1] CC[+but] adv[SENT = ?s2]
    
    
                adv[+negation] -> 'not' | "n't"
                
                adv[SENT = 'neutral' ] ->{Adverb_str}
                adv[SENT = 'negative'] -> {Adverb_neg_str}
                adv[SENT = 'positive'] -> {Adverb_pos_str}
    
                # Relative Pronouns
                RelPro -> 'who' | 'whom' | 'that' | 'which' | 'where' | 'when'|{WhPron_str}
    
                # Preposition Phrase
                PP -> Pre NP[NUM=?n, PERS=?p, SENT=?s] | TO NP[NUM=?n, PERS=?p, SENT=?s]| LOC NP | MOT NP
                # PP_TO -> TO NP
                # PP_LOC -> LOC NP
                # PP_MOT -> MOT NP
                
                TO -> 'to'
                LOC -> 'at' | 'in'
                MOT -> 'to' | 'into'
                ING -> 'ing'
                OF -> 'of'
                Pre -> {Pre_str}
                
                
                # Coordinating Conjunction
                CC[+and, -but, -or] -> 'and' 
                CC[-and, +but, -or] -> 'but' | 'however' 
                CC[-and, -but, +or] -> 'or' | 'Or'
                CC[-and, -but, -or] -> 'because'
                # CC -> {CoorCon_str}
                
                
                # Punctuation
                COMMA ->','
                
                # Possessive Pronoun
                PosPro -> "my"|"your"|"his"|"her"|"its"|"our"|"their"
                
                
                # Person Pronoun
                PRP -> {PersonPronoun_str}
                
                # Proper Noun
                NNP ->{Propn_str}
                
                Cardinal[NUM=?n] ->{CardinalNumber_str}
                Cardinal[NUM=1] -> "one"
        """
        return grammar




