import sqlite3

def migrate_db():
    conn = sqlite3.connect('shortener.db')
    c = conn.cursor()
    try:
        c.execute('ALTER TABLE urls ADD COLUMN expiration_days INTEGER DEFAULT 30')
        c.execute('UPDATE urls SET expiration_days = 30 WHERE expiration_days IS NULL')
        conn.commit()
        print("Added expiration_days column and set default for existing rows.")
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    conn.close()

if __name__ == "__main__":
    migrate_db()