import nltk
from nltk.corpus import verbnet
from nltk import CFG


# Ensure you have the relevant NLTK data downloaded
nltk.download('verbnet')

# Example: finding subcategorization frames for a verb
verb = "was"
classes = verbnet.classids(lemma=verb)

if not classes:
    print(f"No data found for verb: {verb}")
else:
    for cls in classes:
        vclass = verbnet.vnclass(cls)
        print(f"Verb Class: {cls}")
        for frame in vclass.findall('FRAMES/FRAME'):
            # Extracting the frame description
            description = frame.find('DESCRIPTION').attrib
            primary = description.get('primary')
            secondary = description.get('secondary')
            xtag = description.get('xtag')
            print(f"Frame: {primary}, {secondary}, {xtag}")


def verbnet_frame_to_cfg_rule(verb):
    """
    Convert VerbNet frames for a given verb into CFG rules.
    """
    rules = set()
    classes = verbnet.classids(lemma=verb)

    if not classes:
        print(f"No data found for verb: {verb}")
        return rules

    for cls in classes:
        vclass = verbnet.vnclass(cls)
        for frame in vclass.findall('FRAMES/FRAME'):
            description = frame.find('DESCRIPTION').attrib
            primary = description.get('primary')

            if primary:
                # Convert VerbNet frame to CFG rule
                # This conversion logic should be adapted based on your grammar's structure and needs
                rule = f"VP -> V {primary.replace('-', ' ')}"
                rule = f"VP[NUM=?n, PERSON=?p, ] -> V[NUM=?n, PERSON=?p, VFORM=?f, SENT=?s] {primary.replace('-', ' ')}[ROLE='object']"
                rules.add(rule)

    return rules

# Example usage for the verb 'give'
verb = 'was'
cfg_rules = verbnet_frame_to_cfg_rule(verb)
print(cfg_rules)

# Define additional rules for your grammar
additional_rules = """
    S -> NP VP
    NP -> 'John' | 'Mary' | 'the book'
    V -> 'give'
    PP -> P NP
    P -> 'to'
"""

# Combine the rules
grammar_rules = '\n'.join(cfg_rules) + '\n' + additional_rules
grammar = CFG.fromstring(grammar_rules)
print(grammar)