from tests.login import login_for_tests
import json
from config import settings
import requests

# Test the token getter - Success case
def test_token_login_sucess():

    response = login_for_tests(user_type='patient')
    
    # Check the response
    assert response.status_code == 200
    assert response.json()['access_token'] != None
    assert response.json()['detail']['status'] == 'ok'
    assert response.json()['detail']['status_code'] == 0



# Test the token getter - Failed case (wrong password)
def test_token_login_failed():
    
    password = settings.password_test + 'abc'

    # Send the request
    response = login_for_tests(user_type='patient',password=password)
    
    # Check the response
    assert response.status_code == 401
    assert response.json()['detail']['status'] == 'Error'
    assert response.json()['detail']['status_code'] == 3
