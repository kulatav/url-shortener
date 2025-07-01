from flask import Flask, request, redirect, render_template, url_for, flash
import sqlite3
import string
import random
import validators

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
                  clicks INTEGER DEFAULT 0)''')
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
            c.execute('INSERT INTO urls (original_url, short_code, clicks) VALUES (?, ?, 0)',
                      (original_url, short_code))
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
    c.execute('SELECT original_url FROM urls WHERE short_code = ?', (short_code,))
    result = c.fetchone()
    if result:
        c.execute('UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?', (short_code,))
        conn.commit()
        conn.close()
        return redirect(result[0])
    else:
        conn.close()
        flash('Short URL not found.', 'error')
        return redirect(url_for('index'))

# Admin view to list all URLs
@app.route('/admin')
def admin():
    conn = sqlite3.connect('shortener.db')
    c = conn.cursor()
    c.execute('SELECT original_url, short_code, clicks FROM urls')
    urls = c.fetchall()
    conn.close()
    return render_template('admin.html', urls=urls)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)