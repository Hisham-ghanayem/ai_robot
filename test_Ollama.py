import spacy
import pytextrank

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe("textrank")


def extract_meaningful_phrases(doc):
    results = []

    for phrase in doc._.phrases:
        results.append({
            "text": phrase.text,
            "rank": phrase.rank,
            "count": phrase.count,
        })

    return results


def extract_meaningful_words(doc):
    keywords = [
        token.lemma_.lower()
        for token in doc
        if token.pos_ in ["NOUN", "PROPN", "VERB", "ADJ", "NUM"]
        and not token.is_stop
        and not token.is_punct
    ]

    return keywords


def analyze_query(user_input):
    doc = nlp(user_input)

    return {
        "phrases": extract_meaningful_phrases(doc),
        "keywords": extract_meaningful_words(doc),
    }


if __name__ == "__main__":
    user_input = input("Enter a sentence: ")
    result = analyze_query(user_input)
    print(result["phrases"])
    print(result["keywords"])