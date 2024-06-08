import os

from flask_principal import Principal, Permission, RoleNeed
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from collections import defaultdict
from datetime import datetime,  timedelta
from functools import wraps
import uuid
import base64
import random
import string
from sqlalchemy import create_engine, Table, MetaData

from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

# Configure application
app = Flask(__name__, static_folder='../static')
app.secret_key = b"\xd2F\xe0\xb97\xb08\xad\x13%\x8f'Q\xc9}A\xa6\xed\x92'L\xa3mO"

def string_to_datetime(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

app.jinja_env.filters["string_to_datetime"] = string_to_datetime

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
Session(app)

# Configure database
db_file = "messages.db"

# Check if the file exists
if not os.path.exists(db_file):
    print("Database file not found!")
    exit()

# Initialize the SQL object
db = SQL("sqlite:///" + db_file)

PREDEFINED_CATEGORIES = ['Theft', 'Vandalism', 'Assault', 'Burglary', 'Robbery', 'Harassment', 'Drug-related', 'Fraud', 'Suspect Spotted', 'Other']

# Create a function to generate a secure password hash
def generate_hash(password):
    return generate_password_hash(password)

    # Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Specify the login view

class User(UserMixin):
    # User class to work with Flask-Login
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    # Fetch the user from the database
    user = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    if user:
        user_data = user[0]
        return User(id=user_data['id'], username=user_data['username'], email=user_data['email'])
    return None

# Route for rendering the landing page (index.html)
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
   # Get the page number from the request parameters, default to 1 if not provided
    page = request.args.get('page', 1, type=int)
    # Set the number of reports per page
    per_page = 1000
    # Calculate the offset
    offset = (page - 1) * per_page

    # Query the database to retrieve reports for the current page
    reports = db.execute("SELECT id, category, timestamp, location, status, opened FROM reports ORDER BY timestamp DESC LIMIT ? OFFSET ?", per_page, offset)
    # Format timestamp to "24 Feb 2024"
    for report in reports:
        report['timestamp'] = datetime.strptime(report['timestamp'], '%Y-%m-%d %H:%M:%S').strftime('%d %b %Y')

    # Log activity for viewing the index page
    log_activity(db, session.get("user_id"), session.get("username"), "viewed index page", None)

    return render_template("index.html", reports=reports)


@app.route("/view_report/<int:report_id>", methods=["GET", "POST"])
def view_report(report_id):
    if request.method == "POST":
        action = request.form.get("action")

        if action == "open":
            # Update the report status as opened in the database
            db.execute("UPDATE reports SET opened = 1 WHERE id = :report_id", report_id=report_id)

            # Log activity
            log_activity(db, session.get("user_id"), session.get("username"), "report_opened", f"Report {report_id} opened")

    # Logic to fetch and display the full report
    report = db.execute("SELECT * FROM reports WHERE id = :id", id=report_id)

    # Fetch notes associated with the report ID
    notes = db.execute("SELECT note, timestamp AS note_timestamp FROM notes WHERE report_id = :report_id", report_id=report_id)

    for report in report:
        report['timestamp'] = datetime.strptime(report['timestamp'], '%Y-%m-%d %H:%M:%S').strftime('%d %b %Y')

    for note in notes:
        note['note_timestamp'] = datetime.strptime(note['note_timestamp'], '%Y-%m-%d %H:%M:%S').strftime('%d %b %Y @ %H:%M')
    if request.method == "POST":
        action = request.form.get("action")
        if action == "open":
            # Update the database to mark the report as opened
            db.execute("UPDATE reports SET opened = 1 WHERE id = :report_id", report_id=report_id)

    return render_template("view.html", report=report, notes=notes, report_id=report_id)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]
        session["full_name"] = rows[0]["full_name"]

        # Log activity
        log_activity(db, session["user_id"], session["username"], "login", f"User {session['username']} logged in")


        # Check user role and redirect accordingly
        if "AD" in session["username"]:
            return redirect(url_for('dashboard'))
        elif "FA" in session["username"]:
            return redirect(url_for('index'))
        else:
            return redirect(url_for('home'))  # Default redirect

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        # Extract user data from the form
        email = request.form["email"]
        full_name = request.form["full_name"]
        password = request.form["password"]
        role_id = int(request.form['role'])

        # Generate the force_no based on role
        if role_id in (1, 3, 8):
            force_no = ''.join(random.choices(string.digits, k=5)) + 'AD'  # Add 'AD' for admin and tech support
        elif role_id in (2, 4, 5, 6):
            force_no = ''.join(random.choices(string.digits, k=5)) + 'FA'  # Add 'FA' for Field Agents and investigators
        elif role_id in (7, 9, 10):
            force_no = ''.join(random.choices(string.digits, k=5)) + 'OP'  # Add 'OP' for Operational
        else:
            # Handle unsupported role_id (if necessary)
            flash('Unsupported role selected.', 'error')
            return render_template('create_user.html')

        # Use the force number as the username
        username = force_no

        # Hash the password
        hashed_password = generate_hash(password)

        # Check if the email or full name already exists in the database
        user_exists = db.execute("SELECT * FROM users WHERE email = ? OR full_name = ?", email, full_name)
        if user_exists:
            flash("User with this email or username already exists.", 'error')
            print("Flashing message")
            return render_template("create_user.html")

        # Insert user data into the database
        db.execute("INSERT INTO users (username, hash, role_id, email, full_name, force_no) VALUES (?, ?, ?, ?, ?, ?)",
                   username, hashed_password, role_id, email, full_name, force_no)

        # Log activity
        log_activity(db, session.get("user_id"), session.get("username"), "create_user:{force_no}")

        # Flash success message
        flash(f"Account created successfully! Your username is: {force_no}", 'success')
        return render_template("login.html", force_no=force_no)

    return render_template("create_user.html")

@app.route("/dashboard")
@login_required
def dashboard():

    # Log activity
    log_activity(db, session.get("user_id"), session.get("username"), "Opened Dshboard")
    return render_template("dashboard.html")


@app.route("/logout")
def logout():
    """Log user out"""
    username = session.get("username")
    # Log activity
    log_activity(db, session.get("user_id"), session.get("username"), "User logout", f"{username} logged out")

    session.clear()
    flash("Logged out!")
    return redirect("/")


# Define the route to process a report
@app.route("/report/<int:report_id>/process", methods=["GET", "POST"])
@login_required
def process(report_id):
    if request.method == "POST":
        # Example: Get additional form data (if any)
        assigned_to = request.form.get('assigned_to')
        notes = request.form.get('notes')
        priority = request.form.get('priority')

        # Example: Update the report in the database (replace this with your actual database update logic)
        result = db.execute("UPDATE reports SET assigned_to = :assigned_to, priority = :priority WHERE id = :report_id", assigned_to=assigned_to, priority=priority, report_id=report_id)

       # Log activity
        log_activity(db, session.get("user_id"), session.get("username"), "process_report", f"Processed report {report_id}")

        # Check if the update was successful
        if result:
            flash("Report {} processed successfully.".format(report_id))
        else:
            flash("Report {} not found.".format(report_id))

        # Redirect back to the dashboard or any other appropriate page
        return redirect(url_for('view_report', report_id=report_id))
    else:
        # Handle GET request (display processing form)
        return render_template('process.html', report_id=report_id)


@app.route("/report/<int:report_id>/add_notes", methods=["GET", "POST"])
@login_required
def add_notes(report_id):
    if request.method == "POST":
        # Get the form data
        new_note = request.form.get('notes').strip()

        if new_note:
            # Add timestamp to note
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Insert the new note into the database
            db.execute("INSERT INTO notes (report_id, note, timestamp) VALUES (:report_id, :note, :timestamp)",
                       report_id=report_id, note=new_note, timestamp=timestamp)

            # Log activity
            log_activity(db, session.get("user_id"), session.get("username"), "add_note", f"Added note to report {report_id}")

            # Flash message to indicate successful addition of note
            flash("Note added to Report {} successfully.".format(report_id), 'success')
        else:
            # Flash message to indicate that the note cannot be empty
            flash("Note cannot be empty.", 'error')

        return redirect(url_for("view_report", report_id=report_id))

    # If it's a GET request (page is being loaded), simply render the add_notes.html template
    return render_template("add_notes.html", report_id=report_id)


@app.route("/status/<int:report_id>", methods=["GET", "POST"])
@login_required
def status(report_id):
    if request.method == "POST":
        # Get the form data
        new_status = request.form.get('status')

        # Update the status in the database
        db.execute("UPDATE reports SET status = :status WHERE id = :report_id", status=new_status, report_id=report_id)

               # Log activity
        log_activity(db, session.get("user_id"), session.get("username"), "update_status", f"Updated status of report {report_id} to {new_status}")

        flash("Status confirmed.")

        # Redirect back to the view report page or any appropriate page
        return redirect(url_for("view_report", report_id=report_id))  # Adjust route name if needed

    # If it's a GET request (page is being loaded), render the status.html template
    return render_template("status.html", report_id=report_id)

# Route for displaying reports
@app.route('/report_details')
@login_required
def report_details():
    # Get page number from query parameter, default to 1 if not provided
    page = int(request.args.get('page', 1))
    # Number of reports per page
    per_page = 5
    # Calculate offset based on page number
    offset = (page - 1) * per_page
    # Fetch reports from the database
    reports = db.execute("SELECT id, description, category, location, timestamp, reference_number, status FROM reports ORDER BY timestamp DESC LIMIT ? OFFSET ?", per_page, offset)

    # Log activity
    log_activity(db, session.get("user_id"), session.get("username"), "view_reports", f"Viewed report details for page {page}")

    # Calculate total pages
    total_reports = db.execute("SELECT COUNT(*) FROM reports")[0]["COUNT(*)"]
    total_pages = (total_reports + per_page - 1) // per_page
    return render_template('report_details.html', reports=reports, page=page, total_pages=total_pages)

# Define a route to render the form for posting news and notices
@app.route('/post_news', methods=['GET'])
@login_required
def post_news_form():
    return render_template('post_news.html')

# Route to handle the form submission and post news and notices
@app.route('/post_news', methods=['POST'])
@login_required
def post_news():
    title = request.form.get('title')
    content = request.form.get('content')
    location = request.form.get('location')
    reporter = request.form.get('reporter')
    photo = request.files.get('photo')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Save photo as bytes
    if photo:
        photo_data = photo.read()
    else:
        photo_data = None

    # Execute SQL query to insert news into the database
    db.execute("INSERT INTO news (title, content, location, reporter, photo) VALUES (?, ?, ?, ?, ?)",
                title, content, location, reporter, photo_data)

    # Log activity
    log_activity(db, session.get("user_id"), session.get("username"), "post_news", f"Posted news: {title}")

    # Flash message for successful posting
    flash('Article posted successfully!', 'success')

    return render_template("headlines.html")



@app.route("/headlines")
@login_required
def headlines():
    # Fetch headlines from your database or another source
    title_query = db.execute("SELECT id, title, timestamp FROM news ORDER BY timestamp DESC LIMIT 4")
    titles = [{'id': row['id'], 'title': row['title'], 'timestamp': row['timestamp']} for row in title_query]

    # Log activity
    log_activity(db, session.get("user_id"), session.get("username"), "view_headlines", "Viewed headlines")

    return render_template("headlines.html", titles=titles)

@app.route('/article/<int:article_id>')
@login_required
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

@app.route('/edit_article/<int:article_id>', methods=["GET", "POST"])
@login_required
def edit_article(article_id):
    if request.method == "POST":
        # Get form data
        title = request.form.get('title')
        content = request.form.get('content')
        photo = request.files.get('photo')

        # Fetch the article from the database based on the article_id
        article = db.execute("SELECT * FROM news WHERE id = :id", id=article_id)

        if article:
            # If a new photo is provided, update the photo
            if photo:
                photo_data = photo.read()
                # Update photo in the database
                db.execute("UPDATE news SET photo = ? WHERE id = ?", photo_data, article_id)

            # Update title and content in the database
            db.execute("UPDATE news SET title = ?, content = ? WHERE id = ?", title, content, article_id)

            # Flash a success message
            flash('Article updated successfully', 'success')

            # Log activity
            log_activity(db, session.get("user_id"), session.get("username"), "edit_article", f"Edited article with ID {article_id}")

            return redirect(url_for('show_article', article_id=article_id))
        else:
            flash('Article not found', 'error')
            return redirect(url_for('show_article', article_id=article_id))
    else:
        # Fetch the article from the database based on the article_id
        article = db.execute("SELECT * FROM news WHERE id = :id", id=article_id)

        if article:
            # Since db.execute returns a list of dictionaries, get the first item
            article = article[0]
            return render_template('edit_article.html', article=article)
        else:
            # Handle case where article with given id is not found
            flash('Article not found', 'error')
            return redirect(url_for('show_article', article_id=article_id))

def log_activity(db, user_id, username, action_type, details=None):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Retrieve user_id from session if available
    user_id = session.get("user_id", "Anonymous")
    username = session.get("username", "Anonymous")

    # Insert a new record into the audit_trail table
    db.execute("INSERT INTO audit_trail (timestamp, user_id, username, action_type, details) VALUES (?, ?, ?, ?, ?)",
           timestamp, user_id, username, action_type, details)

@app.route("/audit_trail", methods=["GET"])
@login_required
def view_audit_trail():
    audit_trail = db.execute("SELECT * FROM audit_trail ORDER BY timestamp DESC")
    return render_template("audit_trail.html", audit_trail=audit_trail)

@app.route("/faq")
@login_required
def faq():
    return render_template("faq.html")


@app.route("/search", methods=["GET"])
@login_required
def search_reports():

    # Render template with search results
    return render_template("search.html")


@app.route("/live_search", methods=["GET"])
@login_required
def live_search():
    query = request.args.get('query', '')
    if not query:
        return jsonify([])

    sql_query = """
    SELECT id, reference_number
    FROM reports
    WHERE reference_number LIKE :search_query
    LIMIT 10
    """

    results = db.execute(sql_query, {"search_query": f"%{query}%"}).fetchall()
    suggestions = [{"id": row['id'], "reference_number": row['reference_number']} for row in results]

    return jsonify(suggestions)

# Route to display and manage users
@app.route('/manage_users')
@login_required
def manage_users():
    # Fetch users' data along with their roles
    users = db.execute("SELECT users.id, users.status, users.username, users.email, users.full_name, roles.name AS role_name \
                        FROM users \
                        LEFT JOIN roles ON users.role_id = roles.id")

    # Fetch roles for the role selection dropdown
    roles = db.execute("SELECT id, name FROM roles")

    return render_template('manage_users.html', users=users, roles=roles)

# Route to suspend or make an account inactive
@app.route('/suspend_account/<int:user_id>', methods=['POST'])
@login_required
def suspend_account(user_id):
    # Get the new status from the form data
    new_status = request.form.get('status')

    # Execute a SQL UPDATE query to update the user's account status
    db.execute("UPDATE users SET status = :new_status WHERE id = :user_id", new_status=new_status, user_id=user_id)

    # Log activity for managing users
    user_id = session.get("user_id")
    username = session.get("username")
    log_activity(db, user_id, username, "edit_user", f"Edited user of ID {username}")

    return redirect(url_for('manage_users'))

# Route to change the role of a user
@app.route('/change_role/<int:user_id>', methods=['POST'])
@login_required
def change_role(user_id):
    role_id = request.form.get('role_id')

    # Check if the role ID exists in the roles table
    role = db.execute("SELECT id FROM roles WHERE id = :role_id", role_id=role_id)
    if not role:
        return "Role ID does not exist", 404

    # Execute a SQL UPDATE query to change the role of the user with the given user_id
    db.execute("UPDATE users SET role_id = :role_id WHERE id = :user_id", role_id=role_id, user_id=user_id)

    # Log activity for managing users
    user_id = session.get("user_id")
    username = session.get("username")
    log_activity(db, user_id, username, "edit_user", f"Edited user role of ID {username}")

    return redirect(url_for('manage_users'))

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

        # Optionally, you can flash a success message to be displayed on the support page
        flash("Message sent successfully!", "success")

        # Redirect the user back to the support page to display the success message
        return redirect(url_for("support"))
    else:
        # Render the support page template
        return render_template("support.html")

# Route for displaying queries
@app.route("/messages", methods=["GET", "POST"])
@login_required
def messages():
    # Get page number from query parameter, default to 1 if not provided
    page = int(request.args.get('page', 1))
    # Number of reports per page
    per_page = 5
    # Calculate offset based on page number
    offset = (page - 1) * per_page

    # Fetch  from the database
    messages = db.execute("SELECT id, sender_username, message_text, timestamp FROM support ORDER BY timestamp DESC LIMIT ? OFFSET ?", per_page, offset)

    log_activity(db, session.get("user_id"), session.get("username"), "view_messages", "Viewed messages")
    print(messages)

    # Calculate total pages
    total_messages = db.execute("SELECT COUNT(*) FROM support")[0]["COUNT(*)"]
    total_pages = (total_messages + per_page - 1) // per_page
    return render_template('messages.html', messages=messages, page=page, total_pages=total_pages)

if __name__ == "__main__":
    app.run(debug=True)
