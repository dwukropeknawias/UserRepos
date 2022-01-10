import app as user_repos
import json

def test_homepage():

    client = user_repos.app.test_client()
    url = '/'
    response = client.get(url)

    assert response.status_code == 200

def test_about():
    client = user_repos.app.test_client()
    url = '/about'
    response = client.get(url)

    assert response.status_code == 200

def test_login():
    client = user_repos.app.test_client()
    url = '/login'
    response = client.get(url)

    assert response.status_code == 302
    assert response.location.startswith('https://github.com/login/oauth/authorize')
    

def test_authorize_fail():
    client = user_repos.app.test_client()
    url = '/authorize'
    response = client.get(url)

    assert response.status_code == 400 # no token

def test_result():
    client = user_repos.app.test_client()
    url = '/result'
    response = client.get(url)

    assert response.status_code == 200 or response.status_code == 403 or response.status_code == 404# no token

