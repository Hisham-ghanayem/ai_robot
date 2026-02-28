import sqlite3

DB_NAME = "database.db"


# ------------------------------------
# Create Table
# ------------------------------------
def create_table():
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS relationships (
                relationship_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                person_name TEXT NOT NULL,
                relationship_type TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
        """)
        db.commit()


# ------------------------------------
# CREATE
# ------------------------------------
def create_relationship(user_id, person_name, relationship_type):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO relationships (user_id, person_name, relationship_type)
            VALUES (?, ?, ?)
        """, (user_id, person_name, relationship_type))
        db.commit()
        return cursor.lastrowid


# ------------------------------------
# READ ALL
# ------------------------------------
def get_all_relationships():
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM relationships")
        return cursor.fetchall()


# ------------------------------------
# READ SINGLE
# ------------------------------------
def get_relationship_by_id(relationship_id):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM relationships WHERE relationship_id = ?",
            (relationship_id,)
        )
        return cursor.fetchone()


# ------------------------------------
# UPDATE
# ------------------------------------
def update_relationship(relationship_id, new_person_name, new_relationship_type):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute("""
            UPDATE relationships
            SET person_name = ?, relationship_type = ?
            WHERE relationship_id = ?
        """, (new_person_name, new_relationship_type, relationship_id))
        db.commit()


# ------------------------------------
# DELETE
# ------------------------------------
def delete_relationship(relationship_id):
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute(
            "DELETE FROM relationships WHERE relationship_id = ?",
            (relationship_id,)
        )
        db.commit()


# ------------------------------------
# Example Usage
# ------------------------------------
if __name__ == "__main__":
    create_table()

    # Example assumes user_id = 1 exists in users table
    relationship_id = create_relationship(
        user_id=1,
        person_name="Ahmad",
        relationship_type="Friend"
    )
    print("Created relationship:", relationship_id)

    print("All relationships:", get_all_relationships())

    update_relationship(relationship_id, "Ahmad", "Best Friend")
    print("After update:", get_relationship_by_id(relationship_id))

    delete_relationship(relationship_id)
    print("After delete:", get_all_relationships())