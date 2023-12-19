import pytest
from unittest.mock import mock_open, patch
import chardet
import base64
import json
import requests
from plants.plantIdentification import detect_encoding, convBase64, identifyPlant  
from unittest.mock import patch, MagicMock

# @pytest.fixture
# def mocker_chardet_detect(mocker):
#     return mocker.patch("chardet.detect", return_value={"encoding": "utf-8"})

# def test_detect_encoding(mocker_chardet_detect):
#     file_content = b"Sample content"
#     file_path = "test_file.txt"

#     # Using the mock_open to simulate file reading
#     with patch("builtins.open", mock_open(read_data=file_content)):
#         result = detect_encoding(file_path)

#     # Assertions
#     mocker_chardet_detect.assert_called_once_with(file_content)
#     assert result == "utf-8"

TEST_IMAGE_PATH = "plants/tests/test_images/GoldenCactusPlant.jpeg"

def test_convBase64_with_valid_image():
    expected_result = get_expected_result(TEST_IMAGE_PATH)
    result = convBase64(TEST_IMAGE_PATH)
    assert result == expected_result

def test_convBase64_with_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        convBase64("nonexistent/file/path.jpg")

# Helper function to calculate the expected result
def get_expected_result(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())
        encoded_image_str = encoded_image.decode('utf-8')
        return encoded_image_str

@pytest.mark.parametrize(
    "response_data, expected",
    [
        # Test case 1: Valid response
        (
            {
                "result": {
                    "is_healthy": {"probability": 0.95},
                    "classification": {
                        "suggestions": [{"name": "Rose", "probability": 0.9}]},
                    "is_plant": {"probability": 0.95}
                }
            },
            (0.95, "Rose", 0.9, 0.95)
        )
    ]
)

@patch('plantIdentification.requests.request')  
def test_identify_plant(mock_request, response_data, expected):
    # Create a mock response object
    mock_response = MagicMock()
    mock_response.text = json.dumps(response_data)

    # Set the mock object to return the mock response
    mock_request.return_value = mock_response

    # Call the function with a mock image string
    actual = identifyPlant("mock_image_string")

    # Assertion
    assert actual == expected

