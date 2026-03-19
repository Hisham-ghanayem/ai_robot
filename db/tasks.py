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
                task_name TEXT NOT NULL,
                task_description TEXT,
                status TEXT CONSTRAINT my_check check(status in ('To Do','In Progress', 'Done')) DEFAULT 'To Do',
                created_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                assigned_to TEXT ,
                importance REAL CHECK (importance >= 0 AND importance <= 1) DEFAULT 0.5,
                urgency REAL CHECK (urgency >= 0 AND urgency <= 1) DEFAULT 0,
                due_date DATETIME NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            );
        """)
        db.commit()



# ------------------------------------
# READ (All tasks)
# ------------------------------------
def get_all_tasks():
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM tasks')
        return cursor.fetchall()

# ------------------------------------
# Create task by instering task name
# ------------------------------------

def create_task(task_name, task_description, status=None):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute(" INSERT INTO tasks (task_name, task_description,status) VALUES (?,?,?)", (task_name,task_description, status))
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
# UPDATE task name based on task_id
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
# DELETE task based on its id
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