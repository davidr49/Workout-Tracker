import requests
from datetime import datetime
import os
APP_ID = os.environ['NUTRITIONIX_APP_ID']
APP_KEY = os.environ['NUTRITIONIX_API_KEY']
NUTRITIONIX_API_ENDPOINT = os.environ['NUTRITIONIX_ENDPOINT']
SHEETY_API_ENDPOINT = os.environ['SHEETY_ENDPOINT']
today = datetime.now()
today_formatted = today.strftime("%d/%m/%Y")
time_formatted = datetime.now().strftime("%H:%M:%S")


headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
    "x-remote-user-id": "0",
    "Content-Type": "application/json"

}

nurtitionix_params = {
    "query": input("What exercise have you done today?"),
    "gender": "male",
    "weight_kg": 80,
    "height_cm": 180,
    "age": 30
}

response = requests.post(url=NUTRITIONIX_API_ENDPOINT, headers=headers, json=nurtitionix_params)
response.raise_for_status()
response_json = response.json()

sheety_params = {
    "workout": {
        "date": today_formatted,
        "time": time_formatted,
        "exercise": response_json['exercises'][0]['name'].title(),
        "duration": response_json['exercises'][0]['duration_min'],
        "calories": response_json['exercises'][0]['nf_calories']

    }
}

sheety_headers = {
    "Authorization": os.environ['SHEETY_TOKEN']

}

sheety_post = requests.post(url=SHEETY_API_ENDPOINT, json=sheety_params, headers=sheety_headers)
sheety_post.raise_for_status()

