from flask import render_template
from repositories import db

#@app.route('/')
def home():
    return render_template("home.html")
