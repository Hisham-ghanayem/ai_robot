import sqlite3


DB_NAME = "database.db"


# ------------------------------------
# Create table (run once at startup)
# ------------------------------------
def create_table():
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                display_name TEXT NOT NULL,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP
            );
        """)
        db.commit()


# ------------------------------------
# CREATE
# ------------------------------------
def create_user(display_name):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (display_name) VALUES (?)",
            (display_name,)
        )
        db.commit()
        return cursor.lastrowid


# ------------------------------------
# READ (All Users)
# ------------------------------------
def get_all_users():
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()


# ------------------------------------
# READ (Single User)
# ------------------------------------
def get_user_by_id(user_id):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )
        return cursor.fetchone()


# ------------------------------------
# UPDATE
# ------------------------------------
def update_user(user_id, new_display_name):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE users SET display_name = ? WHERE user_id = ?",
            (new_display_name, user_id)
        )
        db.commit()


# ------------------------------------
# DELETE
# ------------------------------------
def delete_user(user_id):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute(
            "DELETE FROM users WHERE user_id = ?",
            (user_id,)
        )
        db.commit()


# ------------------------------------
# Example Usage
# ------------------------------------
if __name__ == "__main__":
    create_table()

    user_id = create_user("Hisham")
    print("Created user:", user_id)

    print("All users:", get_all_users())

    update_user(user_id, "Hisham Updated")
    print("After update:", get_user_by_id(user_id))

    delete_user(user_id)
    print("After delete:", get_all_users())