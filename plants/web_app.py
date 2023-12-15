"""Web app"""
import os
import sys
from flask import Flask, flash, request, session, redirect, url_for, render_template
from pymongo.errors import ConnectionFailure
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = os.getenv('FLASK_SECRET_KEY')


def initialize_database():
    try:
        client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))
        db = client[os.getenv("DATABASE_NAME")]
        users_collection = db[os.getenv("COLLECTION_NAME")]
        client.admin.command('ping')
        return users_collection
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        sys.exit(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def show_login():
    """get/post page for login page"""
    if request.method == "GET":
        return render_template("login.html")
    else:
        users_collection = initialize_database()
        username = request.form.get('username')
        password = request.form.get('password')

        user = users_collection.find_one({"username": username})

        if user and bcrypt.check_password_hash(user['password'], password):
            session['username'] = user['username']
            return redirect(url_for('view_mainscreen'))
        else:
            flash("Incorrect login credentials.")
            return redirect(url_for('show_login'))

@app.route("/createprofile", methods=["GET"])
def show_createprofile():
    return render_template("createprofile.html")

@app.route('/createprofile', methods=['POST'])
def create_profile():
    users_collection = initialize_database()
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = users_collection.find_one({"username": username})

    if user:
        flash("Username already exists.")
        return redirect(url_for('create_profile'))
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        users_collection.insert_one({"username": username, "password": hashed_password})
        flash("Profile created successfully.")
        return redirect(url_for('show_login'))

@app.route('/mainscreen')
def view_mainscreen():
    return render_template('mainscreen.html')

@app.route('/account')
def account():
    return render_template('account.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

