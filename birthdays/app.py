import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Set secret key
app.secret_key = os.urandom(24)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle form submission to add a new birthday
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        try:
            month = int(month)
            day = int(day)
            if month < 1 or month > 12 or day < 1 or day > 31:
                raise ValueError
        except ValueError:
            flash("Please enter valid month (1-12) and day (1-31) values.")
            return redirect("/error")

        # Insert the new entry into the database
        db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)
        return redirect("/")

    else:
        # Retrieve all birthdays from the database
        birthdays = db.execute("SELECT * FROM birthdays")

        # Render the template with the modified birthdays list
        return render_template("index.html", birthdays=birthdays)

if __name__ == '__main__':
    app.run(debug=True)
