from chatbot.chatbot_full import run_chatbot
from db.memories import create_table as create_memories_table
from db.relationships import create_table as create_relationships_table
from db.tasks import create_table as create_tasks_table
from db.users import create_table as create_users_table


def initialize_database():
    create_users_table()
    create_memories_table()
    create_tasks_table()
    create_relationships_table()


if __name__ == "__main__":
    initialize_database()
    print("Assistant system started")
    run_chatbot()