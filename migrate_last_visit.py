import sqlite3
from datetime import datetime

def migrate_db():
    conn = sqlite3.connect('shortener.db')
    c = conn.cursor()
    try:
        c.execute('ALTER TABLE visitors ADD COLUMN last_visit TEXT')
        # Update existing rows with a default timestamp (e.g., now)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute('UPDATE visitors SET last_visit = ? WHERE last_visit IS NULL', (current_time,))
        conn.commit()
        print("Added last_visit column and updated existing rows.")
    except sqlite3.OperationalError as e:
        print(f"Error: {e} (Column may already exist)")
    conn.close()

if __name__ == "__main__":
    migrate_db()
