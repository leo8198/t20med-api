import requests 
from config import settings
from faker import Faker
import random
import json


# Test get all specialties - Success Case
def test_get_specialties():
    
    url = settings.api_test_url
    
    headers = {
    'Content-Type': 'application/json'
    }
    
    response = requests.request("GET", url + 'api/v1/doctors/specialties', headers=headers)


    # Check the response
    assert response.status_code == 200
    assert response.json()['detail']['status'] == 'ok'
    assert response.json()['detail']['status_code'] == 0
    assert response.json()['data'] != {}

# Test to get the Doctors agenda - Success Case
def test_get_agenda():
    
    url = settings.api_test_url
    
    headers = {
    'Content-Type': 'application/json'
    }

    specialty_id = 1
    
    response = requests.request("GET", url + f'api/v1/doctors/specialties/{specialty_id}', headers=headers)


    # Check the response
    assert response.status_code == 200
    assert response.json()['detail']['status'] == 'ok'
    assert response.json()['detail']['status_code'] == 0
    assert response.json()['data'] != []