# Code Cafe Coffee Shop Backend

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

## Endpoints
**GET '/drinks'**
- Fetches the short description of all the drinks in the menu. A public endpoint.  
- Request Arguments: None 
- Returns: 
```
{
    'success': True,
    'drinks': drinks
}
```
where drinks is an array containing the short representation of all drinks. 
- Errors: Results in 404 error if no questions found. If a problem has arisen with the query and the questions cannot be retrieved, results in a 422 error. 


**GET '/drinks-details'**
- Returns the details of all drinks in the database, requiring the 'get:drinks-detail' permission. Public users cannot access this endpoint. 
- Request Arguments: None
- Returns:
```
{
    'success': True,
    'drinks': drinks
}
```
 where drinks is an array containing the long representation of all the drinks. 
 - Errors: Aborts in 404 error if no drinks can be found. If an error arises in retrieving the drinks, aborts in 422 error.  

 **POST '/drinks'**
- Creates a new drink which requires the 'post:drinks' permission. 
- Request Arguments: None 
- Returns:
```
{
    'success': True,
    'drinks': [drink.long()]  
}
```
where drink is the newly created drink and **drink.long()** returns the long (i.e. complete) representation of the drink. 
- Errors: If no form data is found, aborts in 404 error. If there is an issue with creating the new drink, it will abort in a 422 error. 

**PATCH '/drinks/<int:drink_id>'** 
- Updates drink with <id> if the 'patch:drinks' permission is present in the payload. Only **Managers** can edit drinks. 
- Request Arguments: drink_id 
- Returns:
```
{
    'success': True,
    'drinks': [drink.long()]  
}
```
wheredrink.long() is the complete description of the drink updated.
- Errors: If no form data has been found, it will abort in a 404 error. If there is a problem updating the drink in question through the database connection, it will result in a 422 error. 

**DELETE '/drinks/<int:drink_id>'** 
- Deletes a drink with <id> if user has 'delete:drinks' permission. Only **Managers** have this permission.
- Request Arguments: drink_id 
- Returns: Returns the id of the deleted question when successful. 
 ```
{
    'success': True,
    'delete': drink_id, 
}
```
- Errors: If any failure has resulted from the querying, it will abort in a 422 error. If the drink to be deleted does not exist, it will abort in a 404 error. 

## Error Handling
Errors are returned as JSON objects. See an example error handler below.

```
{
"success": False, 
"error": 422,
"message": "unprocessable"
}, 422
```

This api will return the following errors: 
* **401:** Unauthorized
* **404:** Resource Not Found
* **422:** Not Processable 
* **500:** Internal Server Error
* **403:** Forbidden
