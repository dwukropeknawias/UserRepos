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
    

def test_result_with_get():
    client = user_repos.app.test_client()
    url = '/result'
    response = client.get(url)

    assert response.status_code == 405 


