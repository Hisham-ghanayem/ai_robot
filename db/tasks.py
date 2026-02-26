import sqlite3


DB_NAME = "database.db"


# ------------------------------------
# Create table (run once at startup)
# ------------------------------------
def create_table():
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                
                task_name TEXT,
                task_description TEXT,
                status TEXT,
                priority INTEGER DEFAULT 1,
                created_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                assigned_to TEXT ,
                assignee TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            );
        """)
        db.commit()


# ------------------------------------
# CREATE
# ------------------------------------
def task_name(task_name):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO tasks (task_name) VALUES (?)", (task_name,))
        db.commit()
        return cursor.lastrowid


# ------------------------------------
# READ (All Users)
# ------------------------------------
def get_all_tasks():
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM tasks')
        return cursor.fetchall()

def create_task(task_name):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute("""" INSERT INTO tasks (task_name) VALUES (?)""", (task_name,))
        db.commit()
        return cursor.lastrowid
# ------------------------------------
# READ (Single User)
# ------------------------------------
def get_task_by_id(task_id):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM tasks WHERE task_id = ?",
            (task_id,)
        )
        return cursor.fetchone()


# ------------------------------------
# UPDATE
# ------------------------------------
def update_task(task_id, new_task_name):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE tasks SET task_name = ? WHERE task_id = ?",
            (new_task_name, task_id)
        )
        db.commit()


# ------------------------------------
# DELETE
# ------------------------------------
def delete_task(task_id):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute(
            "DELETE FROM tasks WHERE task_id = ?",
            (task_id,)
        )
        db.commit()


# ------------------------------------
# Example Usage
# ------------------------------------
if __name__ == "__main__":
    create_table()

    task_id = create_task("Learn German")
    print("Created task:", task_id)

    print("All task:",  get_all_tasks())

    update_task(task_id, "task Updated")
    print("After update:", get_task_by_id(task_id))

    delete_task(task_id)
    print("After delete:", get_all_tasks())