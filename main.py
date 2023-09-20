import requests
from datetime import datetime
import os

NUTRITIONIX_API_ENDPOINT = 'https://trackapi.nutritionix.com/v2/natural/exercise'
MY_GENDER = 'male'
MY_WEIGHT = 104
MY_HEIGHT = 198
MY_AGE = 18

NUTRITIONIX_APP_ID = os.environ['APP_ID']
NUTRITIONIX_API_KEY = os.environ['API_KEY']
SHEET_API_ENDPOINT = os.environ['SHEET_API_ENDPOINT']
SHEET_TOKEN = os.environ['SHEET_TOKEN']

nutritionix_params = {
    'query': input('How did you exercise today? '),
    'gender': MY_GENDER,
    'weight_kg': MY_WEIGHT,
    'height_cm': MY_HEIGHT,
    'age': MY_AGE
}

nutritionix_headers = {
    'x-app-id': NUTRITIONIX_APP_ID,
    'x-app-key': NUTRITIONIX_API_KEY,
}

nutritionix_response = requests.post(url=NUTRITIONIX_API_ENDPOINT, json=nutritionix_params, headers=nutritionix_headers)
nutritionix_response.raise_for_status()
response_data = nutritionix_response.json()

today = datetime.now()
formatted_date = today.strftime('%d/%m/%Y')
formatted_time = today.strftime('%X')

for exercise in response_data['exercises']:
    sheety_params = {
        'workout': {
            'date': formatted_date,
            'time': formatted_time,
            'exercise': exercise['name'].title(),
            'duration': exercise['duration_min'],
            'calories': exercise['nf_calories']
        }
    }

    sheety_headers = {
        'Authorization': SHEET_TOKEN
    }

    sheety_response = requests.post(url=SHEET_API_ENDPOINT, json=sheety_params, headers=sheety_headers)
    sheety_response.raise_for_status()
