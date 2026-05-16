import re
import sqlite3
from config import DB_PATH
from operator import itemgetter

try:
    import spacy
except ImportError:
    spacy = None

try:
    import pytextrank  # noqa: F401
except ImportError:
    pytextrank = None


MODEL_CANDIDATES = ("en_core_web_lg", "en_core_web_sm")
_nlp = None


def _get_nlp():
    global _nlp

    if _nlp is not None:
        return _nlp

    if spacy is None:
        return None

    for model_name in MODEL_CANDIDATES:
        try:
            _nlp = spacy.load(model_name)
            break
        except OSError:
            continue

    if _nlp is None:
        _nlp = spacy.blank("en")

    if pytextrank is not None and "textrank" not in _nlp.pipe_names:
        try:
            _nlp.add_pipe("textrank")
        except Exception:
            pass

    return _nlp


def _fallback_keywords(user_input):
    return re.findall(r"[A-Za-z0-9]+", user_input.lower())


def _quote_identifier(identifier):
    return '"' + identifier.replace('"', '""') + '"'


def extract_meaningful_words(doc):
    return [
        token.lemma_.lower()
        for token in doc
        if token.pos_ in ["NOUN", "PROPN", "VERB", "ADJ", "NUM"]
        and not token.is_stop
        and not token.is_punct
    ]


def extract_meaningful_phrases(doc):
    results = []

    if not hasattr(doc._, "phrases"):
        return results

    for phrase in doc._.phrases:
        results.append({
            "text": phrase.text,
            "rank": phrase.rank,
            "count": phrase.count,
        })

    return results


def analyze_query(user_input):
    user_input = user_input.strip()
    if not user_input:
        return {"phrases": [], "keywords": []}

    nlp = _get_nlp()
    if nlp is None:
        return {"phrases": [], "keywords": _fallback_keywords(user_input)}

    doc = nlp(user_input)
    keywords = extract_meaningful_words(doc)
    phrases = extract_meaningful_phrases(doc)

    if not keywords:
        keywords = _fallback_keywords(user_input)

    return {
        "phrases": phrases,
        "keywords": keywords,
    }


def prepare_search_terms(query_data):
    keywords = query_data["keywords"]
    phrases = query_data["phrases"]

    text_phrases = [
        phrase["text"].strip().lower()
        for phrase in phrases
        if phrase["text"].strip() and len(phrase["text"]) > 2 # To dope all words that its length less than 2 characters
    ]

    cleaned_keywords = [
        str(keyword).strip().lower()
        for keyword in keywords
        if str(keyword).strip() and len(keyword) > 2 # To dope all words that its length less than 2 characters
    ]

    combined_terms = cleaned_keywords + text_phrases
    return list(dict.fromkeys(combined_terms)) #Return a list of non duplicate keywords


def build_term_importance(query_data):
    term_importance = {}

    # High importance (TextRank phrases)
    for phrase in query_data["phrases"]:
        text = phrase["text"].lower().strip()
        rank = phrase["rank"]

        if text:
            term_importance[text] = rank * 10
    print('Rank is here:', rank, text)

    # Fallback keywords
    for keyword in query_data["keywords"]:
        keyword = keyword.lower().strip()

        if keyword and keyword not in term_importance:
            term_importance[keyword] = 1

    return term_importance








def compute_score(value, term_importance):
    value = value.lower()
    score = 0

    for term, weight in term_importance.items():
        if term in value:
            score += weight

    return score


def global_search(user_input):
    print(">>> ENTERED global_search")

    query_data = analyze_query(user_input)
    search_terms = prepare_search_terms(query_data)
    term_importance = build_term_importance(query_data)

    if not search_terms:
        return []

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    all_results = []

    for table in tables:
        if table.startswith("sqlite_"):
            continue

        quoted_table = _quote_identifier(table)

        cursor.execute(f"PRAGMA table_info({quoted_table});")
        columns = [col[1] for col in cursor.fetchall()]

        for column in columns:
            quoted_column = _quote_identifier(column)

            for term in search_terms:
                query = f"""
                    SELECT {quoted_column}
                    FROM {quoted_table}
                    WHERE CAST({quoted_column} AS TEXT) LIKE ?
                """

                try:
                    cursor.execute(query, (f"%{term}%",))
                except sqlite3.OperationalError:
                    continue

                matches = cursor.fetchall()

                for match in matches:
                    value = match[0]
                    if value is None:
                        continue

                    clean_value = str(value).strip()
                    if not clean_value:
                        continue

                    score = compute_score(clean_value, term_importance)

                    result = {
                        "table": table,
                        "column": column,
                        "matched_term": term,
                        "value": clean_value,
                        "score": score
                    }

                    all_results.append(result)

    conn.close()
    return all_results


def build_context(top_3_results):
    if not top_3_results:
        return ""

    context = "Known information from memory:\n"
    for item in top_3_results:
        context += f"- {item['value']}\n"

    return context

def sort_results(search_results):
    sorted_results = sorted(search_results, key=lambda k: k["score"], reverse=True)
    return sorted_results

if __name__ == "__main__":
    user_input = "when did I start working for Lufthansa?"

    search_results = global_search(user_input)
    sorted_results = sort_results(search_results)
    top_3_results = sorted_results[:3]
    context = build_context(search_results)

    print("\nSEARCH RESULTS:")
    for r in search_results:
        print(r)

    print("\nCONTEXT:")
    print(context)
    print(sorted_results)
    print("\nTOP 3 RESULTS:")
    print(top_3_results)