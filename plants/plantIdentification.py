import requests
import json
import os
import base64
import chardet
import logging
from dotenv import load_dotenv

load_dotenv()

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
  API_TOKEN = os.getenv("API_KEY")

  payload = json.dumps({
    "images": [image],
    "similar_images": True,
    "health": "all"
  })
  
  headers = {
    'Api-Key': API_TOKEN,
    'Content-Type': 'application/json'
  }
  # print("this is the API_Key", API_TOKEN)
  response = requests.request("POST", url, headers=headers, data=payload)
  # print("this is response",response.text)
  textJSON = json.loads(response.text)

  is_healthy_prob = textJSON.get("result", {}).get("is_healthy", {}).get("probability", None)
  is_plant = textJSON.get("result", {}).get("is_plant", {}).get("probability", None)
  # print("this is the probability that it is a plant", is_plant)
  # extracting top classification (with the highest probability)

  classifications = textJSON.get("result", {}).get("classification", {}).get("suggestions", [])
  if classifications:
      top_classification = max(classifications, key=lambda x: x.get("probability", 0))
      plant_name = top_classification.get("name")
      plant_probability = top_classification.get("probability")
  else:
      plant_name = None
      plant_probability = None
  return is_healthy_prob, plant_name, plant_probability, is_plant

#  identifyPlant(convBase64("tests/test_images/GoldenCactusPlant.jpeg"))