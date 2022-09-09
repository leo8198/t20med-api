import requests
from config import settings

# Login function for tests
def login_for_tests( user_type: str,password=None,username=None):

    # Login in the platform
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    if not password:
        password = settings.password_test

    if not username:
        username = settings.username_test
        
    url = settings.api_test_url
    query_string = {
        'user_type': user_type
    }

    data = 'grant_type=&username='+username+'&password='+password+'&scope=&client_id=&client_secret='

    response = requests.post(url + 'api/v1/login', headers=headers, data=data,params=query_string)

    return response