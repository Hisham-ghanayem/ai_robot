from ollama import chat
from db.memories import create_memory
from db.relationships import create_relationship
from db.tasks import create_task
from chatbot.retrieval import global_search, build_context

# ---------------------------
# Configuration
# ---------------------------

model = "gemma3:27b"

base_system_prompt = """
Your name is Amir, an AI assistant developed by Hisham.
You are respectful, concise, and never hallucinate.
If you don't know something, say you don't know. When answering questions about stored memory:

- ONLY use the provided memory context
- DO NOT speculate or add assumptions
- DO NOT say "seems", "appears", or similar uncertain language
- DO NOT add extra explanations
- If the answer exists in memory, return it clearly and directly

Example:
Memory: "Samete is my wife"
User: "Who is Samete?"
Answer: "Samete is your wife."
"""

history = [
    {
        "role": "system",
        "content": base_system_prompt
    }
]

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


def call_model():
    response = chat(model=model, messages=history)
    return response.message.content


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
# Main Chat Loop
# ---------------------------

def run_chatbot():
    while True:
        prompt = get_user_input()

        # Exit condition
        if prompt.lower() in ["exit", "bye"]:
            print("bot: Goodbye.")
            break

        # 1. Memory save
        memory_text = handle_memory(prompt)
        if memory_text:
            create_memory(
                memory_name="User Memory",
                memory_description=memory_text,
                memory_type="general"
            )
            print_response("Memory saved successfully.")
            continue

        # 2. Task save
        task_text = handle_task(prompt)
        if task_text:
            create_task(
                task_name="User Task",
                task_description=task_text
            )
            print_response("Task saved successfully.")
            continue

        # 3. Relationship save
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

        # 4. Retrieval step
        search_results = global_search(prompt)
        memory_context = build_context(search_results)

        # 5. Build temporary message list for this turn
        messages_for_model = [
            {
                "role": "system",
                "content": base_system_prompt
            }
        ]

        # Add memory context only if something useful was found
        if memory_context:
            messages_for_model.append({
                "role": "system",
                "content": memory_context
            })

        # Add previous conversation history except the first system prompt
        messages_for_model.extend(history[1:])

        # Add current user prompt
        messages_for_model.append({
            "role": "user",
            "content": prompt
        })

        # Save user message into history
        add_user_message(prompt)

        # Call model using the temporary messages_for_model
        response = chat(model=model, messages=messages_for_model)
        assistant_reply = response.message.content

        print_response(assistant_reply)

        add_assistant_message(assistant_reply)


# ---------------------------
# Entry Point
# ---------------------------

if __name__ == "__main__":
    run_chatbot()