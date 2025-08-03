import sqlite3
import string
import random
from flask import Flask, render_template, request, redirect, g

# --- Configuration ---
DATABASE = 'urls.db'
HOST = 'http://127.0.0.1:5000/' # Change to your domain when deploying

# --- Flask App Initialization ---
app = Flask(__name__)
app.config.from_object(__name__)

# --- Database Functions ---

def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(app.config['DATABASE'])
        g.sqlite_db.row_factory = sqlite3.Row # Allows accessing columns by name
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    """Initializes the database from the schema file."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """CLI command to initialize the database."""
    init_db()
    print('Initialized the database.')

# --- Helper Functions ---

def generate_short_id(num_chars=6):
    """Generates a random, unique short ID."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(num_chars))

# --- Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles the main page. Displays the form and, on POST,
    creates a new shortened URL.
    """
    if request.method == 'POST':
        long_url = request.form['long_url']
        if not long_url:
            return render_template('index.html', error="URL cannot be empty!")

        db = get_db()
        
        # Check if the URL has already been shortened
        existing_url = db.execute('SELECT short_id FROM urls WHERE long_url = ?', (long_url,)).fetchone()
        
        if existing_url:
            short_id = existing_url['short_id']
        else:
            # Generate a new short ID and ensure it's unique
            while True:
                short_id = generate_short_id()
                cursor = db.execute('SELECT id FROM urls WHERE short_id = ?', (short_id,))
                if cursor.fetchone() is None:
                    break
            
            # Insert new URL into the database
            db.execute('INSERT INTO urls (long_url, short_id) VALUES (?, ?)', (long_url, short_id))
            db.commit()

        short_url = HOST + short_id
        return render_template('index.html', short_url=short_url)

    return render_template('index.html')

@app.route('/<short_id>')
def redirect_to_url(short_id):
    """Redirects the short URL to the original long URL."""
    db = get_db()
    url_data = db.execute('SELECT long_url FROM urls WHERE short_id = ?', (short_id,)).fetchone()
    
    if url_data:
        # Redirect to the long URL
        return redirect(url_data['long_url'])
    else:
        # If the short ID is not found, return a 404 error
        return render_template('404.html'), 404

if __name__ == '__main__':
    # To run this app:
    # 1. In your terminal, run: flask --app app initdb
    # 2. Then run: flask --app app run
    app.run(debug=True)
