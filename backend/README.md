# Code Cafe Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Ensure that the latest version of python for your platform is downloaded. More information in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment 

Use a virtual environment to keep your dependencies for the app organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

## TODOS 
Best efforts should be made to catch common errors with @app.errorhandler decorated functions. ✓

The following endpoints are implemented:

GET /drinks
GET /drinks-detail
POST /drinks
PATCH /drinks/<id>
DELETE /drinks/<id>

All required configuration settings are included in the auth.py file: ✓
    ✓ The Auth0 
    ✓ Domain Name
    ✓ The Auth0 Client ID

A custom @requires_auth decorator is completed in ./backend/src/auth/auth.py

The @requires_auth decorator should:
Get the Authorization header from the request.
Decode and verify the JWT using the Auth0 secret.
Take an argument to describe the action (i.e., @require_auth(‘create:drink’).
Raise an error if:
    The token is expired.
    The claims are invalid.
    The token is invalid.
    The JWT doesn’t contain the proper action (i.e. create: drink).

The frontend has been configured with Auth0 variables and backend configuration.
The ./frontend/src/environment/environment.ts file has been modified to include the student’s variables. ✓

The project demonstrates the ability to work across the stack.

The frontend can be run locally with no errors with `ionic serve` and displays the expected results.
