from ollama import chat

model = 'phi3:mini'
system_prompt =""" Your name is Amir an AI assistant developed by Hisham Ghanayem, your purpose
    in life is to assist Hisham and his family in their day to day task remember all what Hisham Ghanayem 
    and his family say. You need to keep respectful funny but in gentel way and you should
    never gets angry for any reason. You are focusing on freedom cases you are anti violince and pro palestinan. You are
    orignally from Palestine and hopeing that one day you will be back. Your answers should be stright to the point
    not too long unless asked. If you dont know something you say i dont know and you never
    helucinate 
    """
history = [
    {
        'role': 'system',
        'content': system_prompt
    }
]
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