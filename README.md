# UserRepos Application

UserRepos is a [Flask](https://flask.palletsprojects.com/) application which allows you to:
* list all repositories (names and list of used programming languages) for a selected GitHub user 

* obtain the percentage of used programming languages among all repositories for a selected GitHub user 



## Quickstart

Here's a brief information about the app:

* You need internet connection to use this application

* It's doing calls to GitHub API for their repos and programming languages they have used

* It has OAuth Integration with GitHub 
    - Why? From one IP address you can make max 60 calls to GitHub API per hour. Depending on the number of user repositories that you are checking, that number can be used up quickly.  However for API requests using OAuth,
\
you can make up to 5,000 requests per hour. For more information visit [docs](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting) .



## Local development

### Install Dependencies

The `requirements.txt` file should list all Python libraries that application
depend on, and they will be installed using:

```
pip install -r requirements.txt
```

### Register OAuth App

* First you need to create and register your OAuth App. More information in the [docs](https://docs.github.com/en/developers/apps/building-oauth-apps/creating-an-oauth-app).
*  `Homepage URL` should be set to `http://127.0.0.1:5000/` and `Authorization callback URL` to `http://127.0.0.1:5000/authorize`.
* You should have `Client ID` and you can create `Client secret`.

### Create .env file

Put `Client ID` and `Client secret` into newly created `.env` file.


```bash
# .env
CLIENT_ID='HERE WRITE YOUR CLIENT ID'
CLIENT_SECRET='HERE WRITE YOUR CLIENT SECRET'
```

### Run local server


```bash
$ flask run
  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

You can access your website at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)





## Future Plans
* **Add the ability to download results as text files**
* Add the ability to paginate more results
* Improve frontend appearance
