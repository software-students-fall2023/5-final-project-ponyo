import os
import sys
import pytest
import mongomock
import base64
from plants.web_app import initialize_database, app, bcrypt
# from pymongo.errors import ConnectionFailure
from flask import Flask, session, url_for
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

# load_dotenv()
# DATABASE_CONNECTION_STRING = os.getenv("DATABASE_CONNECTION_STRING")

# def database_connection_string():
#     """DB connection string"""
#     return DATABASE_CONNECTION_STRING

# def mock_initialize_database():
#     mock_client = mongomock.MongoClient()
#     db = mock_client['test_db']
#     users_collection = db.get_collection("users")
#     users_collection.insert_one({"username": "testuser", "password": bcrypt.generate_password_hash("testpass").decode('utf-8')})
#     return db,users_collection

# # @patch('plants.web_app.initialize_database', side_effect=mock_initialize_database)
# def test_connection_to_db_successful():
#     """Tests connection to DB"""
#     db, users_collection = initialize_database(database_connection_string())
#     assert db is not None
#     assert users_collection is not None

# # # @patch('plants.web_app.initialize_database', side_effect=mock_initialize_database)
# def test_collection_and_database_exist():
#     """Tests db connection and existence"""
#     db, users_collection = initialize_database(database_connection_string())
#     assert users_collection.name == "users"
#     assert db.name == "ponyo_plant"

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "no body no crime"
    with app.test_client() as client:
        yield client

def test_index_get_route(client):
    """Test the about GET route."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Ponyo" in response.data

def test_login_get_route(client):
    """Test the login GET route."""
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data

def test_login_post_route(client):
    """Test the login POST route."""
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data

def test_createprofile_get_route(client):
    """Test the createprofile GET route."""
    response = client.get("/createprofile")
    assert response.status_code == 200
    assert b"Ponyo" in response.data

def test_logout_redirects(client):
    """Test that logout redirects to the index page."""
    response = client.get('/logout')
    assert response.status_code == 302  # redirect status code
    assert response.location.endswith(url_for('index'))  #  checking redirection

def test_view_uploadplant_redirects_when_not_logged_in(client):
    """Test that /uploadplant redirects to login page when user is not logged in."""
    response = client.get('/uploadplant')
    assert response.status_code == 302  # redirect status code
    assert response.location.endswith(url_for('show_login'))  # checking redirection

def test_view_plants_with_real_image(client):
    TEST_IMAGE_PATH = "plants/tests/test_images/GoldenCactusPlant.jpeg"
    with open(TEST_IMAGE_PATH, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    # mocking the identifyPlant function
    with patch('plants.web_app.identifyPlant') as mock_identify_plant:
        # Set the mock to return a predefined value
        mock_identify_plant.return_value = (0.85, "Mocked Plant", 0.95)
        headers = {'Content-Type': 'application/json'}
        response = client.post('/view_plants', json={"image": encoded_string}, headers=headers)
        assert response.status_code == 200

# @patch('plants.web_app.initialize_database', side_effect=mock_initialize_database)
# def test_create_profile_success(mock_initialize_db, client):
#     mock_initialize_db.return_value.find_one.return_value = None
#     mock_insert = mock_initialize_db().return_value.insert_one

#     response = client.post('/createprofile', data={'username': 'newuser', 'password': 'newpass'})

#     assert response.status_code == 302
#     assert mock_insert.called_once_with({'username': 'newuser', 'password': ...})


# @patch('plants.web_app.initialize_database', side_effect=mock_initialize_database)
# @patch('flask_bcrypt.Bcrypt.check_password_hash', return_value=False)
# def test_login_failure(mock_bcrypt, mock_initialize_db, client):
#     response = client.post('/login', data={'username': 'testuser', 'password': 'wrongpass'})
#     assert 'username' not in session
#     assert response.status_code == 302 
#     assert response.location.endswith(url_for('show_login'))





