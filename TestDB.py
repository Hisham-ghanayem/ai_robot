import spacy
import pytextrank
nlp = spacy.load("en_core_web_lg")
nlp.add_pipe("textrank")

def extract_meaningful_phrases(user_input):
    doc = nlp(user_input)
    results = []
    # examine the top-ranked phrases in the document

    for phrase in doc._.phrases:
        results.append({
            "text": phrase.text,
            "rank": phrase.rank,
            "count": phrase.count,
        })
    return results
def extract_meaningful_words(user_input):
    doc = nlp(user_input)
    keywords = [
        token.lemma_.lower()
        for token in doc
        if token.pos_ in ["NOUN", "PROPN", "VERB", "ADJ", "NUM"]
        and not token.is_stop
        and not token.is_punct
    ]
    return keywords

if __name__ == "__main__":
    user_input = input("Enter a sentence to extract meaningful words: ")
    output_phrases = extract_meaningful_phrases(user_input)
    output_keywords = extract_meaningful_words(user_input)
    print(output_phrases)
    print(output_keywords)
