import os


from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import usd, apology, login_required, lookup

from collections import defaultdict

# Configure application
app = Flask(__name__)

from datetime import datetime


def string_to_datetime(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")


def apology(message, code=400):
    return render_template("apology.html", top="Sorry!", bottom=message), code


app.jinja_env.filters["string_to_datetime"] = string_to_datetime


# Custom filter
app.jinja_env.filters["usd"] = usd


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def validate_password(password):
    # Password must have at least one letter, one number, and one symbol
    if not (
        any(char.isalpha() for char in password)
        and any(char.isdigit() for char in password)
        and any(not char.isalnum() for char in password)
    ):
        return (
            False,
            "Password must have at least one letter, one number, and one symbol",
        )
    else:
        return True, None


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = :user_id", user_id=user_id
    )
    user_cash = db.execute(
        "SELECT cash FROM users WHERE id = :user_id", user_id=user_id
    )[0]["cash"]
    total_value = user_cash

    # Create a dictionary to store total shares for each symbol
    total_shares = defaultdict(int)

    # Calculate total value of user's stocks and sum shares with the same symbol
    for transaction in transactions:
        symbol = transaction["symbol"]
        transaction["current_price"] = lookup(symbol)["price"]
        transaction["total_value"] = (
            transaction["current_price"] * transaction["shares"]
        )

        if transaction["transaction_type"] == "buy":
            total_shares[symbol] += transaction["shares"]
            total_value += transaction["total_value"]
        elif transaction["transaction_type"] == "sell":
            total_shares[symbol] -= transaction["shares"]
            total_value -= transaction["total_value"]

    # Convert total_shares dictionary back to a list of transactions
    transactions = [
        {
            "symbol": symbol,
            "shares": shares,
            "current_price": lookup(symbol)["price"],
            "total_value": shares * lookup(symbol)["price"],
        }
        for symbol, shares in total_shares.items()
    ]

    # Calculate grand total
    grand_total = total_value
    return render_template(
        "index.html",
        title="C$50 Finance",
        transactions=transactions,
        cash=user_cash,
        total_value=total_value,
        grand_total=grand_total,
    )


from flask import render_template

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol or not shares:
            return render_template("apology.html", top="Must provide symbol and shares", bottom="400"), 400

        # Validate shares input
        try:
            shares = float(shares)
            if shares <= 0 or not shares.is_integer():
                raise ValueError
            shares = int(shares)
        except ValueError:
            return render_template("apology.html", top="Shares must be a positive integer", bottom="400"), 400

        # Lookup current price of the stock
        quote = lookup(symbol)
        if not quote:
            return render_template("apology.html", top="Invalid symbol", bottom="400"), 400

        # Calculate total cost
        total_cost = quote["price"] * shares

        # Check if user has enough cash
        user_cash = db.execute(
            "SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"]
        )[0]["cash"]
        if total_cost > user_cash:
            return render_template("apology.html", top="Not enough cash", bottom="400"), 400

        # Update user's cash
        db.execute(
            "UPDATE users SET cash = cash - :total_cost WHERE id = :user_id",
            total_cost=total_cost,
            user_id=session["user_id"],
        )

        # Update user's portfolio
        db.execute(
            "INSERT INTO portfolio (user_id, symbol, shares) VALUES (:user_id, :symbol, :shares) "
            "ON CONFLICT(user_id, symbol) DO UPDATE SET shares = shares + :shares",
            user_id=session["user_id"],
            symbol=symbol,
            shares=shares,
        )

        # Insert transaction into history
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, total_cost, transaction_type) "
            "VALUES (:user_id, :symbol, :shares, :price, :total_cost, 'buy')",
            user_id=session["user_id"],
            symbol=symbol,
            shares=shares,
            price=quote["price"],
            total_cost=total_cost,
        )

        # Redirect to index
        flash("Bought!")
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = :user_id",
        user_id=session["user_id"],
    )
    return render_template("history.html", transactions=transactions)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash("Logged In!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    flash("Logged out!")
    return redirect("/")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")
    elif request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return render_template("apology.html", top="Please provide a symbol", bottom="400"), 400

        # Lookup the stock price
        quote = lookup(symbol)
        if quote is None:
            return render_template("apology.html", top="Invalid symbol", bottom=""), 400

        # Render quoted.html template with the quote data
        return render_template("quoted.html", symbol=symbol, price=quote)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate username and password
        if not username or not password or password != confirmation:
            return apology("invalid username and/or password", 400)

        # Check if username already exists
        if db.execute(
            "SELECT * FROM users WHERE username = :username", username=username
        ):
            return apology("username already exists")

        # Insert new user into database
        db.execute(
            "INSERT INTO users (username, hash, cash) VALUES (:username, :hash, :cash)",
            username=username,
            hash=generate_password_hash(password),
            cash=16000.00,
        )

        flash("Registered!")
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        # Ensure symbol and shares are provided
        if not symbol or not shares:
            return apology("must provide symbol and shares", 400)

        # Lookup the stock symbol
        quote = lookup(symbol)

        # Ensure the symbol is valid
        if quote is None:
            return apology("invalid symbol", 400)

        # Query user's stocks
        user_id = session["user_id"]
        user_stocks = db.execute(
            "SELECT * FROM portfolio WHERE user_id = :user_id AND symbol = :symbol",
            user_id=user_id,
            symbol=symbol,
        )

        # Ensure user has enough shares to sell
        if not user_stocks or user_stocks[0]["shares"] < shares:
            return apology("not enough shares")

        # Calculate total sale amount
        total_sale_amount = quote["price"] * shares

        # Insert transaction into history
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, total_cost, transaction_type) "
            "VALUES (:user_id, :symbol, :shares, :price, :total_cost, 'sell')",
            user_id=session["user_id"],
            symbol=symbol,
            shares=shares,
            price=quote["price"],
            total_cost=total_sale_amount,
        )

        # Update user's cash balance
        db.execute(
            "UPDATE users SET cash = cash + :total_sale_amount WHERE id = :user_id",
            total_sale_amount=total_sale_amount,
            user_id=session["user_id"],
        )

        # Update user's stocks
        db.execute(
            "UPDATE portfolio SET shares = shares - :shares WHERE user_id = :user_id AND symbol = :symbol",
            shares=shares,
            user_id=session["user_id"],
            symbol=symbol,
        )
        flash("Sold!")
        return redirect("/")

    else:
        # Fetch user's stocks for the sell form
        user_id = session["user_id"]
        user_stocks = db.execute(
            "SELECT * FROM portfolio WHERE user_id = :user_id", user_id=user_id
        )
        return render_template("sell.html", user_stocks=user_stocks)


@app.route("/add_float", methods=["GET", "POST"])
@login_required
def add_float():
    if request.method == "GET":
        return render_template("add_float.html")
    elif request.method == "POST":
        # Retrieve the amount from the form
        amount_str = request.form.get("amount")

        # Check if the input amount is provided
        if not amount_str:
            flash("Please provide an amount to add.")
            return render_template("add_float.html")

        # Check if the input amount is a valid number
        try:
            amount = float(amount_str)
        except (TypeError, ValueError):
            flash("Please provide a valid amount to add.")
            return render_template("add_float.html")

        # Check if the amount is positive
        if amount <= 0:
            flash("Please provide a positive amount to add.")
            return render_template("add_float.html")

        # Update the user's cash balance in the database
        user_id = session["user_id"]
        db.execute(
            "UPDATE users SET cash = cash + :amount WHERE id = :user_id",
            amount=amount,
            user_id=user_id,
        )

        # Provide feedback to the user
        flash(f"You have successfully added ${amount:.2f} to your account.")
        return redirect("/")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        # Retrieve form data
        username = session["user_id"]
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        # Check if current password matches
        user = db.execute("SELECT * FROM users WHERE id = :id", id=username)
        if not check_password_hash(user[0]["hash"], current_password):
            return apology("Invalid current password", 403)

        # Check if new password meets requirements
        is_valid, error_message = validate_password(new_password)
        if not is_valid:
            return apology(error_message, 400)

        # Check if new password and confirmation match
        if new_password != confirm_password:
            return apology("New password and confirmation do not match", 400)

        # Update password hash in the database
        db.execute(
            "UPDATE users SET hash = :hash WHERE id = :id",
            hash=generate_password_hash(new_password),
            id=username,
        )

        flash("Password changed successfully")
        return redirect("/")

    return render_template("change_password.html")


if __name__ == "__main__":
    app.run(debug=True)
