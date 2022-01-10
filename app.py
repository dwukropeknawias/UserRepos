from flask import Flask, render_template, redirect, url_for, session, request
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os
import sys
import requests
import json


load_dotenv()

app = Flask(__name__)

oauth = OAuth(app)

app.secret_key = 'secretkey'

github = oauth.register(
    name='github',
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)


@app.route("/")
def homepage():
    user = session.get('user')
    return render_template('index.html', user=user)


@app.route('/login')
def login():
   github = oauth.create_client('github')
   redirect_uri = url_for('authorize', _external=True)
   return github.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    github = oauth.create_client('github')
    token = github.authorize_access_token()
    user = github.get('user').json()
    if user:
        session['user'] = user
        session['token'] = token
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('token', None)
    return redirect('/')


@app.route('/about')
def about():
    user = session.get('user')
    return render_template("about.html", user=user)


@app.route("/result", methods=['POST'])
def result():

    user = session.get('user')

    username = request.form.get('github_username')

    selected_option = request.form.get('which_option') # string values: 1 - list repos, 2 - percentage of all languages

    token = session.get('token')

    if token:
        obt_headers = {'Authorization': 'token ' + token['access_token']}
        payload = {'per_page': 100, 'sort': 'created'}
        response = requests.get(f"https://api.github.com/users/{username}/repos", headers=obt_headers, params=payload)
    else:
        payload = {'sort': 'created'}
        response = requests.get(f"https://api.github.com/users/{username}/repos", params=payload) #not logged in user can get only 30 (default)

    if response.status_code == 404:
        error_message1 = "User Not Found"
        error_message2 = "Sorry but there is not such user on GitHub with username dwukropeknawias"
        return render_template("error.html", user=user, error_message1=error_message1, error_message2=error_message2)

    elif response.status_code == 403:
        error_message1 = "Error 403"
        error_message2 = "API rate limit exceeded for your IP address. Check docs \
        for more information - https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting"
        return render_template("error.html", user=user, error_message1=error_message1, error_message2=error_message2)

    elif response.status_code == 200:
    
        repos_names = []   
        percent_lang = {}
        all_langs_in_repo = []
       
        for ind, r in enumerate(response.json()):
            repos_names.append(r['name'])
            if token:
                obt_headers = {'Authorization': 'token ' + token['access_token']}
                lang_response = requests.get(r['languages_url'], headers=obt_headers) #listing languages also needs to hit .../languages endpoint
            else:
                lang_response = requests.get(r['languages_url'])
            for key in lang_response.json():
                if key not in percent_lang:
                    percent_lang[key] = int(lang_response.json()[key])
                else:
                    percent_lang[key] += int(lang_response.json()[key])
            all_langs_in_repo.append(list(lang_response.json().keys()))
        
        values_sum = sum(percent_lang.values())

        percent_lang = {k: v for k, v in sorted(percent_lang.items(), reverse=True, key=lambda item: item[1])}

        percent_lang = {k: round(v / values_sum * 100, 2) for k, v in percent_lang.items()}
        
        if selected_option == '1':
            return render_template('repos.html', repos_names=repos_names, all_langs_in_repo=all_langs_in_repo,
                                     zip=zip, user=user, username=username)

        elif selected_option == '2':
            return render_template('languages.html', percent_lang=percent_lang, user=user, username=username)

    else:
        error_message1 = "Unknown error"
        error_message2 = "Something went wrong - try again later"
        return render_template("error.html", user=user, error_message1=error_message1, error_message2=error_message2)




