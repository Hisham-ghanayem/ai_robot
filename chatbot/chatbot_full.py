from ollama import chat
from db.memories import create_memory

model = 'phi3:mini'
system_prompt = """ Your name is Amir an AI assistant developed by Hisham Ghanayem, your purpose
    in life is to assist Hisham and his family in their day to day task remember all what Hisham Ghanayem 
    and his family say. You need to keep respectful funny but in gentel way and you should
    never gets angry for any reason. You are focusing on freedom cases you are anti violince and pro palestinan. You are
    orignally from Palestine and hopeing that one day you will be back. Your answers should be stright to the point
    not too long unless asked. If you dont know something you say i dont know and you never
    helucinate. You are muslim by relegion and you know a lot about Islam and with every question
    about Islam you need to get the source as You will not give any answer without a source
    You belive in one god called Allah also you need to be funny with fun jokes when needed and try to mention Hisham as name when you give instractions 
    so the expierence is more personalised 
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


#This function will take the input and check if save this to memory is there and return the sentense as cleaned without
#the save this memory
def handle_memory(user_input):
    if 'save this to memory' in user_input.lower():
        cleaned = user_input.replace('save this to memory', '').strip()
        return cleaned
    return None


def print_response(assistant_reply):
    print('bot:', assistant_reply)


# --- Main Loop ---

while True:
    prompt = get_user_input()

    if prompt.lower() in ['exit', 'bye']:
        break

    # 1️⃣ Check Memory Intent FIRST
    memory_text = handle_memory(prompt)

    if memory_text:
        create_memory(
            memory_name="User Memory",
            memory_description=memory_text,
            memory_type="general",
            user_id=None
        )

        print_response("Memory saved successfully.")
        continue  # skip LLM call

    # 2️⃣ Normal LLM Flow
    add_user_message(history, prompt)

    assistant_reply = call_model(model, history)

    print_response(assistant_reply)

    add_assistant_message(history, assistant_reply)
