import sqlite3

def migrate_db():
    conn = sqlite3.connect('shortener.db')
    c = conn.cursor()
    try:
        c.execute('ALTER TABLE urls ADD COLUMN clicks INTEGER DEFAULT 0')
        conn.commit()
        print("Added clicks column to urls table.")
    except sqlite3.OperationalError as e:
        print(f"Error: {e} (Column may already exist)")
    conn.close()

if __name__ == "__main__":
    migrate_db()
