import sqlite3

def migrate_db():
    conn = sqlite3.connect('shortener.db')
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS visitors
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      short_code TEXT NOT NULL,
                      visitor_ip TEXT NOT NULL,
                      UNIQUE(short_code, visitor_ip),
                      FOREIGN KEY (short_code) REFERENCES urls (short_code))''')
        conn.commit()
        print("Created visitors table.")
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    conn.close()

if __name__ == "__main__":
    migrate_db()