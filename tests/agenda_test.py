import requests 
from config import settings
from faker import Faker
import random
import json
from tests.login import login_for_tests


# Test create agenda - Success Case
def test_create_agenda():
    
    url = settings.api_test_url
    
    response = login_for_tests('doctor')
    
    # Check the response
    assert response.status_code == 200
    assert response.json()['access_token'] != None

    headers = {
        'Authorization': 'Bearer ' + response.json()['access_token'],
        'Content-Type': 'application/json'
    }

    payload = json.dumps({
        "days": [
            {
           "time": "17:00",
           "date": "2022-10-20"
       },
       {
           "time": "17:20",
           "date": "2022-10-20"
       },
       {
           "time": "18:30",
           "date": "2022-10-21"
       }
        ]
    })
    
    response = requests.request("POST", url + 'api/v1/doctors/agenda', headers=headers,data=payload)


    # Check the response
    assert response.status_code == 200
    assert response.json()['detail']['status'] == 'ok'
    assert response.json()['detail']['status_code'] == 0