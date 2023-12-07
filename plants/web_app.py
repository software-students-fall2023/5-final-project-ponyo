"""Web app"""
import os
import logging
import sys
from flask import Flask, flash, request, session, redirect, url_for
from pymongo.errors import ConnectionFailure
from pymongo import MongoClient
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

try:
    client = MongoClient(os.getenv("DATABASE_CONNECTION_STRING"))
    db = client[os.getenv("DATABASE_NAME")]
    users_collection = db[os.getenv("COLLECTION_NAME")]
    client.admin.command('ping')
except ConnectionFailure as e:
    print(f"MongoDB connection failed: {e}")
    sys.exit(1)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = users_collection.find_one({"username": username})
    
    if user and bcrypt.check_password_hash(user['password'], password):
        session['username'] = user['username']
        return redirect(url_for('view_mainscreen'))
    else:
        flash("Incorrect login credentials.")
        return redirect(url_for('generate_login_page'))

@app.route('/createprofile', methods=['POST'])
def create_profile():
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = users_collection.find_one({"username": username})

    if user:
        flash("Username already exists.")
        return redirect(url_for('generate_create_profile_page'))
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        users_collection.insert_one({"username": username, "password": hashed_password})
        flash("Profile created successfully.")
        return redirect(url_for('generate_login_page'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

