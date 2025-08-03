Flask Link Shortener
A simple, yet powerful link shortening service built with Python and the Flask web framework. This application allows you to take any long URL and generate a short, easy-to-share link that redirects to the original destination. It uses an SQLite database to persistently store the links.

✨ Features
Shorten URLs: Convert long, cumbersome URLs into short and manageable links.

Persistent Storage: Uses an SQLite database to save all your shortened links.

Unique ID Generation: Creates a unique, random 6-character ID for each new URL.

Redirects: Seamlessly redirects users from the short link to the original long URL.

Duplicate Prevention: Checks if a URL has already been shortened and returns the existing short link to save space.

Simple Web Interface: A clean and minimal UI to input the long URL and get the shortened version.

404 Handling: Gracefully handles requests for short links that do not exist.

🚀 Getting Started
Follow these instructions to get a local copy up and running.

Prerequisites
Make sure you have Python and pip installed on your system. You will need to install Flask:

pip install Flask

Installation & Setup
Clone the repository (or download the files):

git clone <your-repository-url>
cd <repository-directory>

Create the schema.sql file:
This file is required to initialize the database schema. Create a file named schema.sql in the same directory as your Python script with the following content:

DROP TABLE IF EXISTS urls;
CREATE TABLE urls (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  long_url TEXT NOT NULL,
  short_id TEXT NOT NULL UNIQUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

Create the templates folder:
Your Flask application uses HTML templates. Create a templates folder and add the following files inside it:

index.html:

<!doctype html>
<title>URL Shortener</title>
<h1>URL Shortener</h1>
<form method=post>
  <input type=text name=long_url size=40 placeholder="Enter your long URL here">
  <input type=submit value=Shorten>
</form>
{% if error %}
  <p style="color:red;">{{ error }}</p>
{% endif %}
{% if short_url %}
  <p>Your shortened URL: <a href="{{ short_url }}">{{ short_url }}</a></p>
{% endif %}

404.html:

<!doctype html>
<title>Not Found</title>
<h1>404 - Not Found</h1>
<p>The requested URL was not found on the server.</p>

Initialize the Database:
Before running the application for the first time, you need to create the database file and its table. Run the following command in your terminal from the project directory:

flask --app "Link Shortener with a Database" initdb

This will create a urls.db file in your project directory.

Usage
Run the Flask Application:
Execute the following command to start the local development server:

flask --app "Link Shortener with a Database" run

Note: If you are in development, you can enable debug mode for live reloading and detailed error pages.

Open Your Browser:
Navigate to http://127.0.0.1:5000/ in your web browser.

Shorten a Link:
Enter a long URL into the input field and click "Shorten". The application will display the newly generated short link.

🔧 How It Works
The user submits a long URL through the web interface.

The application first checks if the URL already exists in the SQLite database.

If it exists, the existing short ID is retrieved.

If it's a new URL, a unique 6-character alphanumeric short_id is generated.

The new long_url and short_id pair is saved to the database.

The shortened URL (e.g., http://127.0.0.1:5000/aB1cD2) is returned to the user.

When a user visits a shortened URL, the application looks up the short_id in the database, retrieves the corresponding long_url, and performs a 302 redirect to the original destination.

📁 File Structure
.
├── Link Shortener with a Database.py  # Main Flask application logic
├── schema.sql                         # Database schema definition
├── urls.db                            # SQLite database file (generated)
└── templates/
    ├── index.html                     # Main page template
    └── 404.html                       # 404 error page template
