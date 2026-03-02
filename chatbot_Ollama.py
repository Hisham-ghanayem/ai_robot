import ollama
history = []
model = "phi3:mini"
while True:
    prompt = input("Hisham: ").strip()
    if prompt.lower() in ('exit', 'quit'):
        break

    message = {
        "role": "user",
        "content": prompt
    }
    history.append(message)
    print("bot :", end="", flush=True)
    bot_message_content = ""
    response = ollama.chat(model=model, messages=history, stream=True)

    for chunk in response:
        bot_message_content += chunk.message.content
        print(chunk.message.content, end="", flush=True)

    print()


    bot_message = {
        "role": "bot",
        "content": bot_message_content
    }
    history.append(bot_message)
