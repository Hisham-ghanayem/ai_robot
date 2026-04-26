def route_query(user_input):
    """
    Decide whether the user question is:
    - hybrid: needs memory + general reasoning
    - memory_only: asks for stored personal facts
    - general_only: normal world knowledge / general questions
    """
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
        "based on what you know about me",
        "what do you think my",
        "do i need to do"

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
        "what do i do",
        "what sport do i do"
    ]

    # Hybrid must win first, because some hybrid questions also contain memory wording
    if any(clue in text for clue in hybrid_clues):
        return "hybrid"

    if any(clue in text for clue in memory_clues):
        return "memory_only"

    return "general_only"


