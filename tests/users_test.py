from tests.login import login_for_tests
import json
from config import settings
import requests
from faker import Faker 
import random
from tests.crud import CrudHelper
from database.models.doctors import Doctor
from tests.file_data import file_data_jpeg

# Test the patient creator - Success case
def test_create_patient():

    url = settings.api_test_url

    faker = Faker()

    payload = json.dumps({
    "name": faker.name(),
    "email": faker.email(),
    "password": "test123",
    "cpf": str(random.randint(11111111,99999999)),
    "phone_number": faker.phone_number(),
    "crm": str(random.randint(111111,999999)),
    "crm_state": "SP"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    query_params = {
        'user_type': 'patient'
    }

    response = requests.request("POST", url + 'api/v1/users', headers=headers, data=payload, params=query_params)


    # Check the response
    assert response.status_code == 200
    assert response.json()['detail']['status'] == 'ok'
    assert response.json()['detail']['status_code'] == 0



# Test the token getter - Failed case (wrong password)
def test_create_doctor():
    
    url = settings.api_test_url

    faker = Faker()

    payload = json.dumps({
    "name": faker.name(),
    "email": faker.email(),
    "password": "test123",
    "cpf": str(random.randint(11111111,99999999)),
    "phone_number": faker.phone_number(),
    "crm": str(random.randint(111111,999999)),
    "crm_state": "SP"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    query_params = {
        'user_type': 'doctor'
    }

    response = requests.request("POST", url + 'api/v1/users', headers=headers, data=payload, params=query_params)


    # Check the response
    assert response.status_code == 200
    assert response.json()['detail']['status'] == 'ok'
    assert response.json()['detail']['status_code'] == 0

# Test the send of the doctor documents - Success Case
def test_sign_up_documents():
    
    url = settings.api_test_url


    payload = json.dumps({
        "data": [
            {
                "file_name": str(random.randint(11111111,99999999)) + '.jpeg',
                "file_type": "rg_photo_front",
                "file_data": file_data_jpeg
            }
        ]
    })

    # Do the login to get the token
    username = CrudHelper().get_last_result(Doctor).email
    password = "test123"

    response = login_for_tests('doctor',password,username)
    
    # Check the response
    assert response.status_code == 200
    assert response.json()['access_token'] != None

    headers = {
        'Authorization': 'Bearer ' + response.json()['access_token'],
        'Content-Type': 'application/json'
    }


    response = requests.request("POST", url + 'api/v1/users/documents', headers=headers, data=payload)


    # Check the response
    assert response.status_code == 200
    assert response.json()['detail']['status'] == 'ok'
    assert response.json()['detail']['status_code'] == 0