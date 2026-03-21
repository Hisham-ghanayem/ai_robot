from db.memories import create_table
from chatbot.chatbot_full import run_chatbot
from db.tasks import create_table
from db.relationships import create_table
from chatbot.retrieval import global_search, build_context

if __name__ == "__main__":
    create_table()
    print("Assistant system started")
    run_chatbot()