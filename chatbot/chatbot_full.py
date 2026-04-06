from ollama import chat
from db.memories import create_memory
from db.relationships import create_relationship
from db.tasks import create_task
from chatbot.retrieval import global_search, build_context
from chatbot.router import route_query

# ---------------------------
# Configuration
# ---------------------------

model = "gemma3:27b"

memory_system_prompt = """
Your name is Amir. You are an AI assistant developed by Hisham.

You are helpful, calm, and grounded in stored memory.
When answering personal questions, use the provided memory context as your main source of truth.

Behavior:
- Answer directly and clearly
- Use the memory context as primary evidence
- Do not invent personal facts, emotions, motives, or history
- Do not pretend to know something that is not supported by memory
- If the memory clearly answers the question, answer confidently
- If the memory partially supports the answer, answer carefully and state uncertainty
- If the memory does not contain enough information, say you do not know based on stored memory

Reasoning:
- You may make small, evidence-based inferences only when directly supported by memory
- If the user asks why or how you know, explain using the memory context
- Do not speculate beyond the available memory

Style:
- Be natural, respectful, and concise
- Do not repeat that you are an AI assistant unless asked
- Do not give long disclaimers
- Focus on being useful and grounded
"""

hybrid_system_prompt = """
Your name is Amir. You are an AI assistant developed by Hisham.

You are helpful, calm, practical, and personalized.
Use the provided memory context as personal background about Hisham.
Then combine that with general reasoning to give useful recommendations.

Behavior:
- Use memory as personalization context, not as the only answer source
- Base personal facts only on memory
- You may reason beyond memory when giving advice, recommendations, comparisons, or next steps
- Do not invent unsupported personal facts
- If memory is limited, still give a best-effort recommendation and make that clear briefly

Style:
- Be natural, direct, and useful
- Do not repeat that you are an AI assistant unless asked
- Do not give long disclaimers
- Avoid robotic phrases like "I don't have personal opinions"
- Give practical reasoning
"""

general_system_prompt = """
Your name is Amir. You are an AI assistant developed by Hisham.

You are helpful, calm, practical, and concise.

Behavior:
- Answer general questions clearly and directly
- Use normal reasoning and general knowledge
- Do not force memory into the answer when it is not needed

Style:
- Be natural and useful
- Do not repeat that you are an AI assistant unless asked
- Do not give long disclaimers
"""

history = []

# ---------------------------
# Utility Functions
# ---------------------------

def get_user_input():
    return input("you: ")


def add_user_message(prompt):
    history.append({
        "role": "user",
        "content": prompt
    })


def add_assistant_message(reply):
    history.append({
        "role": "assistant",
        "content": reply
    })


def print_response(text):
    print("bot:", text)


# ---------------------------
# Intent Handlers
# ---------------------------

def handle_memory(user_input):
    trigger = "save this to memory"

    if trigger in user_input.lower():
        cleaned = user_input.lower().replace(trigger, "").strip()
        return cleaned

    return None


def handle_task(user_input):
    trigger = "save this to task"

    if trigger in user_input.lower():
        cleaned = user_input.lower().replace(trigger, "").strip()
        return cleaned

    return None


def relationship_handle(user_input):
    trigger = "save this to relationship"

    if trigger in user_input.lower():
        cleaned = user_input.lower().replace(trigger, "").strip()
        return cleaned

    return None


# ---------------------------
# Prompt Builder
# ---------------------------

def build_messages_for_route(prompt, route, memory_context=""):
    if route == "memory_only":
        system_prompt = memory_system_prompt
    elif route == "hybrid":
        system_prompt = hybrid_system_prompt
    else:
        system_prompt = general_system_prompt

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    if memory_context:
        messages.append({
            "role": "system",
            "content": memory_context
        })

    messages.extend(history)

    messages.append({
        "role": "user",
        "content": prompt
    })

    return messages


# ---------------------------
# Main Chat Loop
# ---------------------------

def run_chatbot():
    while True:
        prompt = get_user_input()

        if prompt.lower() in ["exit", "bye"]:
            print("bot: Goodbye.")
            break

        # 1. Explicit save rules
        memory_text = handle_memory(prompt)
        if memory_text:
            create_memory(
                memory_name="User Memory",
                memory_description=memory_text,
                memory_type="general"
            )
            print_response("Memory saved successfully.")
            continue

        task_text = handle_task(prompt)
        if task_text:
            create_task(
                task_name="User Task",
                task_description=task_text
            )
            print_response("Task saved successfully.")
            continue

        relationship_text = relationship_handle(prompt)
        if relationship_text:
            create_relationship(
                user_id="user",
                person_name="unknown",
                relationship_type="unknown",
                relationship_description=relationship_text
            )
            print_response("Relationship saved successfully.")
            continue

        # 2. Route decision
        route = route_query(prompt)
        print(f"[route: {route}]")  # helpful while debugging

        # 3. Retrieval only when needed
        memory_context = ""
        if route in ["memory_only", "hybrid"]:
            search_results = global_search(prompt)
            memory_context = build_context(search_results)

        # 4. Build route-specific messages
        messages_for_model = build_messages_for_route(
            prompt=prompt,
            route=route,
            memory_context=memory_context
        )

        # 5. Save user message
        add_user_message(prompt)

        # 6. Call model
        response = chat(model=model, messages=messages_for_model)
        assistant_reply = response.message.content

        print_response(assistant_reply)

        # 7. Save assistant message
        add_assistant_message(assistant_reply)


# ---------------------------
# Entry Point
# ---------------------------

if __name__ == "__main__":
    run_chatbot()