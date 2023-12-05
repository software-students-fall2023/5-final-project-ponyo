import requests
import json
import os
import base64
import chardet

def detect_encoding(file_path):
    """Figures out encoding"""
    with open(file_path, "rb") as file:
        result = chardet.detect(file.read())
    return result["encoding"]


def convBase64(image_path):
  with open(image_path, "rb") as image_file:
        # Encode the image file to base64
        encoded_image = base64.b64encode(image_file.read())
        # Convert bytes to a string (optional)
        encoded_image_str = encoded_image.decode('utf-8')
        return encoded_image_str

def identifyPlant(image):
  url = "https://plant.id/api/v3/identification"
  script_dir = os.path.dirname(os.path.abspath(__file__))
  API_TOKEN = os.getenv("API_TOKEN")
  if not API_TOKEN:
    FILE_PATH_API = os.path.join(script_dir, "config.json")
    encodingAPI = detect_encoding(FILE_PATH_API)
    with open(FILE_PATH_API, "r", encoding=encodingAPI) as f:
        configs = json.load(f)
        API_TOKEN = configs["api_token"]

  payload = json.dumps({
    "images": [image],
    "similar_images": True,
    "health": "all"
  })
  headers = {
    'Api-Key': 'RnK0QKj0txGAa0MlQiNkFHk33IvDHiU3KLTy7zSfV1NbsiJpAu',
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  textJSON = json.loads(response.text)
  print("Possible Diseases:")
  diseases = textJSON.get("result").get("disease").get("suggestions")
  for i in diseases:
     print("    "+i.get("name"),i.get("probability"))


  print("Plant Classification:")
  classification = textJSON.get("result").get("classification").get("suggestions")
  for i in classification:
     print("    "+i.get("name"),i.get("probability"))
     similar_images = i.get("similar_images")
     for x in similar_images:
        print("        -"+x.get("url"))

image = convBase64("images/GoldenCactusPlant.jpeg")
identifyPlant(image)