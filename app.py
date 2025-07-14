from flask import Flask, request, redirect, render_template, url_for, flash
import sqlite3
import string
import random
import validators
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "supersecretkey"  # For flash messages

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('shortener.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  original_url TEXT NOT NULL,
                  short_code TEXT NOT NULL UNIQUE,
                  clicks INTEGER DEFAULT 0,
                  created_at TEXT)''')
    conn.commit()
    conn.close()

# Generate a random short code
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Home page to shorten URLs
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        # Validate URL
        if not validators.url(original_url):
            flash('Invalid URL. Please enter a valid URL.', 'error')
            return render_template('index.html')
        
        conn = sqlite3.connect('shortener.db')
        c = conn.cursor()
        
        # Check if URL already exists
        c.execute('SELECT short_code FROM urls WHERE original_url = ?', (original_url,))
        result = c.fetchone()
        if result:
            short_code = result[0]
        else:
            # Generate unique short code
            short_code = generate_short_code()
            while True:
                c.execute('SELECT short_code FROM urls WHERE short_code = ?', (short_code,))
                if not c.fetchone():
                    break
                short_code = generate_short_code()
            c.execute('INSERT INTO urls (original_url, short_code, clicks, created_at) VALUES (?, ?, 0, ?)',
                      (original_url, short_code, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
        
        conn.close()
        short_url = url_for('redirect_url', short_code=short_code, _external=True)
        return render_template('index.html', short_url=short_url)
    
    return render_template('index.html')

# Redirect short URL to original and increment clicks
@app.route('/<short_code>')
def redirect_url(short_code):
    conn = sqlite3.connect('shortener.db')
    c = conn.cursor()
    c.execute('SELECT original_url, created_at FROM urls WHERE short_code = ?', (short_code,))
    result = c.fetchone()
    if result:
        original_url, created_at = result
        # Check if URL is expired (30 days)
        created_time = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
        if datetime.now() - created_time > timedelta(days=30):
            conn.close()
            flash('This URL has expired.', 'error')
            return redirect(url_for('index'))
        c.execute('UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?', (short_code,))
        conn.commit()
        conn.close()
        return redirect(original_url)
    else:
        conn.close()
        flash('Short URL not found.', 'error')
        return redirect(url_for('index'))

# Admin view to list all URLs
@app.route('/admin')
def admin():
    conn = sqlite3.connect('shortener.db')
    c = conn.cursor()
    c.execute('SELECT original_url, short_code, clicks, created_at FROM urls')
    urls = c.fetchall()
    # Add expiration status
    urls_with_status = [
        (original_url, short_code, clicks, created_at,
         'Expired' if datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S') < datetime.now() - timedelta(days=30) else 'Active')
        for original_url, short_code, clicks, created_at in urls
    ]
    conn.close()
    return render_template('admin.html', urls=urls_with_status)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)