import os

from flask_principal import Principal, Permission, RoleNeed
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from collections import defaultdict
from datetime import datetime
from functools import wraps
import uuid
import base64

from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

# Configure application
app = Flask(__name__, static_folder='../static')
app.secret_key = b'\x18\xe0#$t<\x83\xfbVO\xcd\xd3z\x16\xa2\xb4\xec{wW\xe1\xf6w\xa8'

def string_to_datetime(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

app.jinja_env.filters["string_to_datetime"] = string_to_datetime

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure database
db_file = os.path.abspath("messages.db")

# Check if the file exists
if not os.path.exists(db_file):
    print("Database file not found!")
    exit()

# Initialize the SQL object
db = SQL("sqlite:///" + db_file)

PREDEFINED_CATEGORIES = ['Theft', 'Vandalism', 'Assault', 'Burglary', 'Robbery', 'Harassment', 'Drug-related', 'Fraud', 'Suspect Spotted', 'Other']

# Route for rendering the landing page (index.html)
@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":

        # Log activity for viewing the index page
        log_activity(db, session.get("user_id"), session.get("username"), "viewed index page", None)
        return render_template("index.html")

@app.route("/incident_report", methods=["GET", "POST"])
def incident_report():
    if request.method == "GET":
        # Clear reference number from session if present
        session.pop('reference_number', None)

        # Check if the honeypot field is filled out
        if request.form.get("honeypot"):
            flash("Bot detected. Form submission rejected.", "error")
            return redirect("/incident_report")

        return render_template("incident_report.html", predefined_categories=PREDEFINED_CATEGORIES)
    elif request.method == "POST":
        if 'reference_number' in session:
            return redirect("/incident_report")

        category = request.form.get('category')
        description = request.form.get('description')
        location = request.form.get('location')
        anonymous = True if request.form.get('anonymous') == 'on' else False

        current_datetime = datetime.now()
        reference_number = current_datetime.strftime("%Y%m%d%H%M") + "_anon"

        db.execute("INSERT INTO reports (category, description, location, anonymous, reference_number) VALUES (?, ?, ?, ?, ?)",
           category, description, location, anonymous, reference_number)

        session['reference_number'] = reference_number

        # Log activity
        log_activity(db, session.get("user_id"), session.get("username"), "Submitted incident report", details=f"Anonymous user submitted an incident report with reference number: {reference_number}")

        # Clear form data from session after successful submission
        session.pop('category', None)
        session.pop('description', None)
        session.pop('location', None)
        session.pop('anonymous', None)

        return render_template("submitted.html", reference_number=reference_number)

@app.route("/track_report", methods=["GET", "POST"])
def track_report():
    if request.method == "GET":
        reference_number = request.args.get('reference_number')
        if reference_number:
            # Fetch incident report details from the database based on the reference number
            report_result = db.execute("SELECT * FROM reports WHERE reference_number = ?", reference_number)
            report = report_result[0]  # Access the first element directly

            # Check if the report exists
            if report:
                # Extract report_id from the fetched report
                report_id = report['id']

                # Fetch notes associated with the report_id
                notes_result = db.execute("SELECT note, timestamp AS note_timestamp FROM notes WHERE report_id = ?", report_id)
                notes = notes_result

                # Format timestamps of notes
                for note in notes:
                    note['note_timestamp'] = datetime.strptime(note['note_timestamp'], '%Y-%m-%d %H:%M:%S').strftime('%d %b %Y')

                # Log activity
                log_activity(db, session.get("user_id"), session.get("username"), "Viewed report details", details=f"User viewed details for report with reference number: {reference_number}")

                # Report found, render template with report details
                return render_template("track_report.html", report=report, notes=notes)
            else:
                # Report not found, display error message
                flash("Report with reference number {} not found.".format(reference_number), 'error')

        # No reference number provided or report not found, render template with tracking form
        return render_template("track_report.html", report=None)

@app.route("/faq")
def faq():
    return render_template("faq.html")


@app.route('/headlines')
def headlines():
    # Fetch headlines from your database or another source
    title_query = db.execute("SELECT id, title, timestamp FROM news ORDER BY timestamp DESC LIMIT 4")
    titles = [{'id': row['id'], 'title': row['title'], 'timestamp': row['timestamp']} for row in title_query]

    # Log activity
    log_activity(db, session.get("user_id"), session.get("username"), "view_headlines", "Viewed headlines")

    return render_template('headlines.html', titles=titles)


@app.route('/article/<int:article_id>')
def show_article(article_id):
    # Fetch the article from the database based on the article_id
    article = db.execute("SELECT * FROM news WHERE id = :id", id=article_id)

    if article:
        # Initialize a list to store formatted articles
        formatted_news = []
        # Fetch headlines for the carousel
        headlines = db.execute("SELECT title FROM news")


        # Loop through each fetched article
        for article_data in article:
            # Convert the published_at string to a datetime object
            timestamp = datetime.strptime(article_data['timestamp'], '%Y-%m-%d %H:%M:%S')
            # Format the datetime object to the desired format
            formatted_date = timestamp.strftime('%A %d %B %Y, %I:%M %p')
            # Update the article dictionary with the formatted date
            article_data['timestamp'] = formatted_date
            # Append the updated article to the formatted_news list
            formatted_news.append(article_data)

        # Log activity
        log_activity(db, session.get("user_id"), session.get("username"),"view_article", f"Viewed article with ID {article_id}")

        # Render the template with the list of formatted articles
        return render_template('news.html', articles=formatted_news)


def log_activity(db, user_id, username, action_type, details=None):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Retrieve user_id from session if available
    user_id = session.get("user_id", "Anonymous")
    username = session.get("username", "Anonymous")

    # Insert a new record into the audit_trail table
    db.execute("INSERT INTO audit_trail (timestamp, user_id, username, action_type, details) VALUES (?, ?, ?, ?, ?)",
           timestamp, user_id, username, action_type, details)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/support", methods=["GET", "POST"])
def support():
    if request.method == "POST":
        # Handle form submission
        message_text = request.form.get("message_text")
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Fetch the username from the session
        sender_username = session.get("username", "Anonymous")

        # Insert the message into the database
        db.execute("INSERT INTO messages (sender_username, message_text, timestamp) VALUES (?, ?, ?)",
                   sender_username, message_text, timestamp)

        # Log the access
        log_activity(db, session.get("user_id"), session.get("username"), "support_access", "Accessed the support page")

        flash("Message sent successfully!", "success")

        # Redirect the user back to the support page to display the success message
        return redirect(url_for("support"))
    else:
        # Render the support page template
        return render_template("support.html")

if __name__ == "__main__":
    app.run(debug=True)
