import dotenv
import requests
from datetime import *
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv()

APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")
sheet_api_url = os.getenv("sheet_api_url")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")


exercise_text = input("What exercise did you do today?")
GENDER = "MALE"
WEIGHT_KG = "72.5"
HEIGHT_CM = "190.0"
AGE = "28"

# Construct the API endpoint URL
api_url = 'https://trackapi.nutritionix.com/v2/natural/exercise'


# Set up the parameters
params = {
    'query': exercise_text,
    'gender': GENDER,
    'weight_kg': WEIGHT_KG,
    'height_cm': HEIGHT_CM,
    'age': AGE,
}

header = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,

}

# Make the HTTP request
response = requests.post(api_url, json=params, headers=header)
data = response.json()
response.raise_for_status()

# adding data to sheety

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in data["exercises"]:
    sheet_inputs = {
        "sheet1": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    headers = {
        "Authorization": BEARER_TOKEN
    }

    sheet_response = requests.post(sheet_api_url, json=sheet_inputs, headers=headers)

    print(sheet_response.text)


