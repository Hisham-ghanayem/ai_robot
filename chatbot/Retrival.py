import spacy
from chatbot_full import *
#load the large english module
nlp = spacy.load('en_core_web_lg')

def extract_meaningful_words(text):
    doc = nlp(text)
#Keep only the rleated nouns and verbs and ignore the small words that does not
#have a big impact on the overall meaning
    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'ADJ', 'VERB', 'ADV','DATE', 'PROPN', 'NUM']]
    return keywords
#example
text = "I marrid my wife Samete on march 25 in 2020 during covid and we are 6 years marrid"
print(extract_meaningful_words(text))
