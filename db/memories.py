import sqlite3

DB_NAME = "database.db"


# ------------------------------------
# Create table (run once at startup)
# ------------------------------------
def create_table():
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            memory_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            memory_name TEXT NOT NULL,
            memory_type TEXT,
            memory_description TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        """)
        db.commit()


# ------------------------------------
# CREATE
# ------------------------------------
def create_memory(memory_name, memory_description, memory_type=None, user_id=None):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO memory (memory_name, memory_description, memory_type, user_id)
            VALUES (?, ?, ?, ?)
        """, (memory_name, memory_description, memory_type, user_id))
        db.commit()
        return cursor.lastrowid


# ------------------------------------
# READ (All)
# ------------------------------------
def get_all_memory():
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM memory")
        return cursor.fetchall()


# ------------------------------------
# READ (Single)
# ------------------------------------
def get_memory(memory_id):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM memory WHERE memory_id = ?",
            (memory_id,)
        )
        return cursor.fetchone()


# ------------------------------------
# UPDATE
# ------------------------------------
def update_memory(memory_id, new_memory_name):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE memory SET memory_name = ? WHERE memory_id = ?",
            (new_memory_name, memory_id)
        )
        db.commit()


# ------------------------------------
# DELETE
# ------------------------------------
def delete_memory(memory_id):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute(
            "DELETE FROM memory WHERE memory_id = ?",
            (memory_id,)
        )
        db.commit()


# ------------------------------------
# Example Usage
# ------------------------------------
if __name__ == "__main__":
    create_table()

    # Create memory
    memory_id = create_memory(
        memory_name="Boxing Gym",
        memory_description="Went to boxing gym and trained for 1 hour",
        memory_type="activity"
    )
    print("Created memory:", memory_id)

    # Read all
    print("All memories:", get_all_memory())

    # Update
    update_memory(memory_id, "Boxing Training")
    print("After update:", get_memory(memory_id))

    # Delete
    delete_memory(memory_id)
    print("After delete:", get_all_memory())