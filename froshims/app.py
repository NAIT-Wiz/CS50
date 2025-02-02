from flask import Flask, render_template, request

app = Flask(__name__)

SPORTS =["Basketball", "Soccer", "Ultimate"]

@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS)


@app.route("/register", methods=["POST"])
def register():
    if not request.form.get("name")or not request.form.get("sport"):
        return render_template("failure.html")
    return render_template("success")
