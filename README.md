# URL Shortener Web App

A simple Python web application built with Flask to shorten URLs and redirect to original links, with SQLite storage.

## Features
- Shorten long URLs via a web form with custom expiration periods (1-90 days).
- Redirect from short URLs to original URLs (expires after specified period).
- Track total clicks, unique visitors, and last visit time per URL.
- View all shortened URLs with click counts, unique visitors, last visit time, creation timestamps, expiration periods, and status in an admin page.
- Input validation for URLs and expiration days.
- Persistent storage using SQLite.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/kulatav/url-shortener.git
   cd url-shortener

2. Create and activate a virtual environment:
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
    pip install -r requirements.txt
    
4. Run the application:
    python app.py
    Open http://localhost:5000 in your browser.

    Usage
        Enter a URL and expiration period (1-90 days, default 30) in the form to get a shortened link.
        Visit the shortened link (e.g., http://localhost:5000/abc123) to redirect to the original URL.
        Access /admin to view all shortened URLs, their click counts, creation timestamps, expiration periods, and status.

5. Exit the virtual environment (if needed):
    deactivate

## Demo
![URL SHORTENER Demo](url-shortener-demo.gif)
![Screenshot home page](home_page_url_shortner_app.png)
![Screenshot home page on click](home_page_on_click_url_shortner_app.png)
![Screenshot admin view](admin_view_url_shortner_app.png)

## License  
MIT License