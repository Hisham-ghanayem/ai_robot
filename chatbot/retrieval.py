import re
import sqlite3
from config import DB_PATH
user_input = "what is my full time job and where do I work"
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
    keywords = [
        token.lemma_.lower()
        for token in doc
        if token.pos_ in ["NOUN", "PROPN", "VERB", "ADJ", "NUM"]
        and not token.is_stop
        and not token.is_punct
    ]
    return keywords


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

    text_phrases = []
    for phrase in phrases:
        phrase_text = phrase["text"].strip().lower()
        if phrase_text and len(phrase["text"]) > 2:
            text_phrases.append(phrase_text)

    cleaned_keywords = []
    for keyword in keywords:
        clean_keyword = str(keyword).strip().lower()
        if clean_keyword and len(keyword) > 2:
            cleaned_keywords.append(clean_keyword)

    combined_terms = cleaned_keywords + text_phrases
    return list(dict.fromkeys(combined_terms))


def _normalize_search_terms(user_input_or_terms):
    if isinstance(user_input_or_terms, str):
        return prepare_search_terms(analyze_query(user_input_or_terms))

    combined_terms = []
    for term in user_input_or_terms:
        clean_term = str(term).strip().lower()
        if clean_term:
            combined_terms.append(clean_term)

    return list(dict.fromkeys(combined_terms))


def global_search(user_input_or_terms):
    print(">>> ENTERED global_search")
    search_terms = _normalize_search_terms(user_input_or_terms)
    if not search_terms:
        return []

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]



    all_results = []

    for table in tables:
        print("Current Tables:", table)

        if table == "sqlite_sequence":
            print("skipped internal table", table)
            continue

        quoted_table = _quote_identifier(table)
        cursor.execute(f"PRAGMA table_info({quoted_table});")
        columns = [col[1] for col in cursor.fetchall()]

        print("all columns", columns)
        print("Looped tables:", table)
        for column in columns:
            quoted_column = _quote_identifier(column)
            for term in search_terms:
                query = (
                    f"SELECT {quoted_column} FROM {quoted_table} "
                    f"WHERE CAST({quoted_column} AS TEXT) LIKE ?"
                )

                try:
                    cursor.execute(query, (f"%{term}%",))
                except sqlite3.OperationalError:
                    continue

                matches = cursor.fetchall()
                for match in matches:
                    value = match[0]
                    if value is None:
                        continue
                    print(">>> ENTERED matches #############")
                    print("used table for this match is:",table)
                    print("used column for this match is:", column)
                    print("matches is:", value)

                    clean_value = str(value).strip()
                    if clean_value:
                        result ={
                            "table": table,
                            "column": column,
                            "matched_term": term,
                            "value": clean_value,
                        }
                        all_results.append(result)

    conn.close()
    return all_results



def build_context(search_results):
    if not search_results:
        return ""

    context = "Known information from memory:\n"
    for item in search_results:
        context += f"- {item}\n"

    return context
if __name__ == "__main__":
    user_input = "when did I start working for Lufthansa?"

    query_data = analyze_query(user_input)
    search_terms = prepare_search_terms(query_data)
    search_results = global_search(search_terms)
    context = build_context(search_results)


    print("USER INPUT:")
    print(user_input)

    print("\nQUERY DATA:")
    print(query_data)

    print("\nSEARCH TERMS:")
    print(search_terms)

    print("\nSEARCH RESULTS:")
    print(search_results)

    print("\nCONTEXT:")
    print(context)
    print("\nSTRUCTURED RESULTS:")
    for r in search_results:
        print(r)


