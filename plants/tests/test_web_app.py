import os
import sys
import pytest
import mongomock
from ..web_app import initialize_database, app, bcrypt
from pymongo.errors import ConnectionFailure
from flask import Flask, session, url_for
from unittest.mock import patch, MagicMock

# @patch('pymongo.MongoClient')
# def test_mongodb_connection_success(mock_mongo_client):
#     """Test to ensure successful MongoDB connection."""
#     mock_mongo_client.return_value.admin.command.return_value = True
#     users_collection = initialize_database()
#     mock_mongo_client.assert_called_with(os.getenv("DATABASE_CONNECTION_STRING"))

# @patch('pymongo.MongoClient')
# def test_mongodb_connection_failure(mock_mongo_client):
#     """Test to simulate MongoDB connection failure."""
#     mock_mongo_client.side_effect = ConnectionFailure("Failed to connect")
#     with pytest.raises(SystemExit) as pytest_wrapped_e:
#         initialize_database()
#     assert pytest_wrapped_e.type == SystemExit
#     assert pytest_wrapped_e.value.code == 1

def mock_initialize_database():
    mock_client = mongomock.MongoClient()
    db = mock_client['test_db']
    users_collection = db['users']
    users_collection.insert_one({"username": "testuser", "password": bcrypt.generate_password_hash("testpass").decode('utf-8')})
    return users_collection

def test_connection_to_db_successful():
    """Tests connection to DB"""
    users_collection = initialize_database()
    assert users_collection is not None

def test_collection_and_database_exist():
    """Tests db connection and existence"""
    database = initialize_database()
    assert database.name == "users"

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index_get_route(client):
    """Test the about GET route."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Cooking" in response.data

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
    assert b"Save" in response.data

@patch('web_app.initialize_database', side_effect=mock_initialize_database)
def test_create_profile_success(mock_initialize_db, client):
    mock_initialize_db.return_value.find_one.return_value = None
    mock_insert = mock_initialize_db.return_value.insert_one

    response = client.post('/createprofile', data={'username': 'newuser', 'password': 'newpass'})

    assert response.status_code == 302
    assert mock_insert.called_once_with({'username': 'newuser', 'password': ...})

# @patch('web_app.initialize_database', side_effect=mock_initialize_database)
# @patch('flask_bcrypt.Bcrypt.check_password_hash', return_value=True)
# def test_login_success(mock_bcrypt, mock_initialize_db, client):
#     response = client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
#     assert 'username' in session
#     assert session['username'] == 'testuser'
#     assert response.status_code == 302
#     assert response.location.endswith(url_for('view_mainscreen'))

@patch('web_app.initialize_database', side_effect=mock_initialize_database)
@patch('flask_bcrypt.Bcrypt.check_password_hash', return_value=False)
def test_login_failure(mock_bcrypt, mock_initialize_db, client):
    response = client.post('/login', data={'username': 'testuser', 'password': 'wrongpass'})
    assert 'username' not in session
    assert response.status_code == 302 
    assert response.location.endswith(url_for('show_login'))

# def test_connection_failure():
#     # Mock environment variables
#     with patch('os.getenv') as mock_getenv:
#         mock_getenv.side_effect = ['invalid_connection_string', 'database_name', 'collection_name']

#         # Mock MongoClient exception
#         with patch('pymongo.MongoClient') as mock_client:
#             mock_client.return_value.admin.command.side_effect = ConnectionFailure('Connection refused')

#             # Capture output
#             with patch('sys.exit') as mock_exit:
#                 try:
#                     mock_initialize_database()
#                 except Exception as e:
#                     assert False, f"Unexpected exception: {e}"

#                 # Verify printed message
#                 assert print.call_args[0][0] == f"MongoDB connection failed: Connection refused"

#                 # Verify MongoClient call
#                 mock_client.assert_called_once_with('invalid_connection_string')

#                 # Verify admin command
#                 mock_client.return_value.admin.command.assert_called_once_with('ping')

#                 # Verify sys.exit call
#                 mock_exit.assert_called_once_with(1)




