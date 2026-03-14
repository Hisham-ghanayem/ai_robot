#connect the python file to Ollama library
import ollama
#t stores the entire conversation in order so the LLM
#can see previous messages.
history = []
#Define the LLM model you want to use
model = "gemma3:4b"
#Wihle the script is running then it is true therefore define the following
#Prompt as Hisham and strip it so no strange characters
while True:
    prompt = input("Hisham: ").strip()
#If the prompt includes the world exit or quite break the loop
    if prompt.lower() in ('exit', 'quit'):
        break
#Give the role set for the chatbot by starting with the user
#Each message variable has role and cotnet (content was defined up as an input)
    message = {
        "role": "user",
        "content": prompt
    }
#With every prompt append the prompt to the history list
    history.append(message)
#To be honest here i dont udnerstand why we put this print before defining
#bot message but in general this is an empty print immediatly appears after
#user prompt with flush to true to ensure all input is running immediatly
    print("bot :", end="", flush=True)
#The bote message variable is defined but it is empty for now as we are sitting
#up all the ingerians before calling the LLM response
    bot_message_content = ""
#Define a new variable response that calls Ollama Model connecting it to history
#list and insure to stream it
    response = ollama.chat(model=model, messages=history, stream=True)
#for loop in response(The Ollama resposne) to add content to the populated message
#then print the message immdediatly
    for chunk in response:
        bot_message_content += chunk.message.content
        print(chunk.message.content, end="", flush=True)
#Move to next line once response is populated
    print()

#I dont kow why do we have the bot_message at the end or what its benefit
    bot_message = {
        "role": "Assistant",
        "content": bot_message_content
    }
    history.append(bot_message)
