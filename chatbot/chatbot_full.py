from ollama import chat
from db.memories import create_memory
from db.tasks import create_task

# ---------------------------
# Configuration
# ---------------------------

model = "phi3:mini"

system_prompt = """
Your name is Amir, an AI assistant developed by Hisham.
You are respectful, concise, and never hallucinate.
If you don't know something, say you don't know.
"""

history = [
    {
        "role": "system",
        "content": system_prompt
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
# Memory Intent Handler
# ---------------------------

def handle_memory(user_input):
    trigger = "save this to memory"

    if trigger in user_input.lower():
        cleaned = user_input.lower().replace(trigger, "").strip()
        return cleaned

    return None

def handle_task(user_input):
    trigger= "save this to task"
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

        # 1️⃣ Check memory intent FIRST
        memory_text = handle_memory(prompt)

        if memory_text:
            create_memory(
                memory_name="User Memory",
                memory_description=memory_text,
                memory_type="general"
            )

            print_response("Memory saved successfully.")
            continue
        # ️⃣ check task intent first
        task_text = handle_task(prompt)
        if task_text:
            create_task(
                task_name="User Task",
                task_description=task_text,
                status = "To Do"
            )

        # 2️⃣ Normal LLM Flow
        add_user_message(prompt)

        assistant_reply = call_model()

        print_response(assistant_reply)

        add_assistant_message(assistant_reply)


# ---------------------------
# Entry Point
# ---------------------------

if __name__ == "__main__":
    run_chatbot()