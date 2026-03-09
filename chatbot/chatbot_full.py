from ollama import chat

model = 'phi3:mini'
history = []

# --- Functions ---

def get_user_input():
    return input('you: ')

def add_user_message(history, prompt):
    history.append({
        'role': 'user',
        'content': prompt
    })

def call_model(model, history):
    response = chat(model=model, messages=history)
    return response.message.content

def add_assistant_message(history, assistant_reply):
    history.append({
        'role': 'assistant',
        'content': assistant_reply
    })

def print_response(assistant_reply):
    print('bot:', assistant_reply)

# --- Main Loop ---

while True:
    prompt = get_user_input()

    if prompt.lower() in ['exit', 'bye']:
        break

    add_user_message(history, prompt)

    assistant_reply = call_model(model, history)

    print_response(assistant_reply)

    add_assistant_message(history, assistant_reply)