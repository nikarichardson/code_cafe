import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
"""
A public endpoint that contains only the short version of the drink. 
"""
@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        selection = Drink.query.order_by(Drink.id).all()

        # uncomment the following after development 
        #if len(selection) == 0:
        #    abort(404)

        #drinks = [drink.short() for drink in selection]
        drinks = []
        for drink in selection:
          drinks.append(drink.short())

        return jsonify({
          'success': True,
          'drinks': drinks 
        })

    except: 
        abort(422)

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
"""
Returns the details of a drink, requiring the 'get:drinks-detail' permission
""" 
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drink_detail():
    try:
        selection = Drink.query.order_by(Drink.id).all()

        # uncomment the following after development 
        #if len(selection) == 0:
        #    abort(404)

        drinks = []
        for drink in selection:
          drinks.append(drink.long())

        return jsonify({
          'success': True,
          'drinks': drinks
        })

    except: 
        abort(422)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
"""
Create a new drink endpoint requires the 'post:drinks' permission. 
"""
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink():
    body = request.get_json()

    ## if no form data 
    if body == None:
        abort(404)

    new_recipe = body.get('recipe')
    new_title = body.get('title')

    try:
        new_drink = Drink(title=new_title, recipe=json.dumps(new_recipe))
        new_drink.insert()
            
        drink = []
        drink.append(new_drink.long())
    
        return jsonify({
          'success': True,
          'drinks': drink  
        })

    except: 
        abort(422) 


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
"""
Updates drink with <id> if the 'patch:drinks' permission is present in the payload. 
"""
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('delete:drinks')
def update_drink(drink_id):
    body = request.get_json()

    ## if no form data 
    if body == None:
        abort(404)
    
    updated_title = body.get('title')
    updated_recipe = body.get('recipe')

    old_drink = Drink.query.filter(Drink.id == drink_id).one_or_none() 

    if updated_title == None:
        updated_title = old_drink.title

    if updated_recipe == None: 
        updated_recipe = old_drink.recipe
    else:
        updated_recipe = json.dumps(updated_recipe) 

    try:
        Drink.query.filter(Drink.id == drink_id).update({'title': updated_title})
        Drink.query.filter(Drink.id == drink_id).update({'recipe': updated_recipe})

        updated_drink = Drink.query.filter(Drink.id == drink_id).one_or_none()  
        drink =[]

        drink.append(updated_drink.long())
    
        return jsonify({
          'success': True,
          'drinks': drink # or just append drink.long() ? 
        })

    except: 
        abort(422) 



'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
'''
Deletes a drink with <id> if user has 'delete:drinks' permission  
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(drink_id):
    try: 
      drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
  
      if drink is None:
        abort(404)

      drink.delete()

      return jsonify({
        'success': True,
        'delete': drink_id, 
      })

    except:
      abort(422)


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
404 Error: Resource cannot be found. 
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "not found"
                    }), 404


'''
401 Error: Request does not go through because user lacks valid authentication credentials for the desired resource
'''

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
                    "success": False, 
                    "error": 401,
                    "message": "unauthorized"
                    }), 401

'''
403 Error: Arises when trying to access a resource that you are not allowed to access. 
'''

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
                    "success": False, 
                    "error": 403,
                    "message": "forbidden"
                    }), 403



