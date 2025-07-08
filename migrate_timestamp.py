import sqlite3
from datetime import datetime

def migrate_db():
    conn = sqlite3.connect('shortener.db')
    c = conn.cursor()
    try:
        # Add created_at column without default
        c.execute('ALTER TABLE urls ADD COLUMN created_at TEXT')
        # Update existing rows with current timestamp
        c.execute('UPDATE urls SET created_at = ? WHERE created_at IS NULL', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),))
        conn.commit()
        print("Added created_at column and updated existing rows.")
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    conn.close()

if __name__ == "__main__":
    migrate_db()