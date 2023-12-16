"""Web app"""
import os
import sys
import base64
import logging
from flask import Flask, flash, request, session, redirect, url_for, render_template, jsonify
from pymongo.errors import ConnectionFailure
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from plantIdentification import identifyPlant

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
            return redirect(url_for('view_index'))
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
        return redirect(url_for('view_index'))

@app.route('/index')
def view_index():
    return render_template('index.html')

@app.route('/plants')
def view_plants():
    return render_template('plants.html')

@app.route('/account')
def view_account():
    return render_template('account.html')

@app.route('/uploadplant')
def view_uploadplant():
    return render_template('uploadplant.html')

@app.route("/data_processing", methods=["POST"])
def data_output():
    """handles post request of photo that was collected on page"""
    try:
        image_data = request.json["image"]  # extracting base64 image data
        image_binary = base64.b64decode(image_data.split(",")[1])  # decode the image

        json_plant_info = identifyPlant(image_binary)
        return json_plant_info
    except ConnectionError as error:
        logging.error("Error uploading image: %s", error)
        return jsonify({"error": "Error uploading image"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

