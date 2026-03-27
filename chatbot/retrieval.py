import sqlite3
import spacy
import pytextrank

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe("textrank")


def extract_meaningful_words(doc):
    """
    Take the user's sentence and return useful search words.
    We keep nouns, proper nouns, verbs, adjectives, and numbers.
    """
    keywords = [
        token.lemma_.lower()
        for token in doc
        if token.pos_ in ["NOUN", "PROPN", "VERB", "ADJ", "NUM"]
        and not token.is_stop
        and not token.is_punct
    ]
    return keywords


def extract_meaningful_phrases(doc):
    """
    Take the user's sentence and return useful phrases with rank and count.
    """
    results = []

    for phrase in doc._.phrases:
        results.append({
            "text": phrase.text,
            "rank": phrase.rank,
            "count": phrase.count,
        })

    return results


def analyze_query(user_input):
    """
    Call both keywords and phrases functions and return both results.
    """
    doc = nlp(user_input)

    return {
        "phrases": extract_meaningful_phrases(doc),
        "keywords": extract_meaningful_words(doc),
    }


def global_search(user_input):
    """
    Search all tables and all text-like columns in the SQLite database
    using extracted keywords and phrases from the user input.

    Returns:
        list[str]: matching text values from the database
    """
    doc = nlp(user_input)

    keywords = extract_meaningful_words(doc)
    phrases = extract_meaningful_phrases(doc)
    phrase_text = [item["text"] for item in phrases]

    output_results = keywords + phrase_text

    if not output_results:
        return []

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    all_results = []

    for table in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        columns_info = cursor.fetchall()
        columns = [col[1] for col in columns_info]

        for column in columns:
            for word in output_results:
                try:
                    query = f"SELECT {column} FROM {table} WHERE {column} LIKE ?"
                    cursor.execute(query, (f"%{word}%",))
                    matches = cursor.fetchall()

                    for match in matches:
                        value = match[0]

                        if value is not None:
                            value = str(value).strip()
                            if value:
                                all_results.append(value)

                except sqlite3.OperationalError:
                    continue

    conn.close()

    unique_results = list(dict.fromkeys(all_results))
    return unique_results


def build_context(search_results):
    """
    Convert raw database matches into clean prompt context for the LLM.
    """
    if not search_results:
        return ""

    context = "Known information from memory:\n"

    for item in search_results:
        context += f"- {item}\n"

    return context