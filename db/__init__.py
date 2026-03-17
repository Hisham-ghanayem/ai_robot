from db.memories import create_table
from chatbot.chatbot_full import run_chatbot

if __name__ == "__main__":
    create_table()
    print("Assistant system started")
    run_chatbot()