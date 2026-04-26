def route_query(user_input):
    text = user_input.strip().lower()

    hybrid_clues = [
        "should i",
        "what should i",
        "what should be my",
        "for me",
        "recommend",
        "best for me",
        "fits me",
        "career path",
        "based on",
        "help me choose",
        "help me decide",
        "which should i",
        "which is better for me",
        "what should i buy",
        "what should i focus on",
        "what should i learn next",
        "what should i work on next",
    ]

    memory_clues = [
        "who is my",
        "what is my",
        "when is my",
        "what do you know about my",
        "what did i tell you",
        "what was the",
        "tell me about my",
        "when did i",
        "where do i live",
    ]

    print("TEXT:", repr(text))
    print("MEMORY CLUES:", memory_clues)
    print("MEMORY MATCHES:", [clue for clue in memory_clues if clue in text])

    if any(clue in text for clue in hybrid_clues):
        return "hybrid"

    if any(clue in text for clue in memory_clues):
        return "memory_only"

    return "general_only"


if __name__ == "__main__":
    print("FINAL ROUTE:", route_query("where do i live"))