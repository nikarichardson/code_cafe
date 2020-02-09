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
Uncomment the following line to initialize the database
'''
# db_drop_and_create_all()

"""
A public endpoint that contains only the short version of the drink.
"""
@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        selection = Drink.query.order_by(Drink.id).all()

        # uncomment the following after development
        if len(selection) == 0:
            abort(404)

        drinks = []
        for drink in selection:
            drinks.append(drink.short())

        return jsonify({
          'success': True,
          'drinks': drinks
        })

    except:
        abort(422)


"""
Returns the details of all drinks in the database.
"""
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drink_detail():
    try:
        selection = Drink.query.order_by(Drink.id).all()

        # uncomment the following after development
        if len(selection) == 0:
            abort(404)

        drinks = []
        for drink in selection:
            drinks.append(drink.long())

        return jsonify({
            'success': True,
            'drinks': drinks
        })

    except:
        abort(422)


"""
Creates a new drink which requires the 'post:drinks' permission.
"""
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink():
    body = request.get_json()

    # if no form data
    if body is None:
        abort(404)

    new_recipe = body.get('recipe')
    new_title = body.get('title')

    try:
        drink = Drink(title=new_title, recipe=json.dumps(new_recipe))
        drink.insert()

        return jsonify({
          'success': True,
          'drinks': [drink.long()]
        })

    except:
        abort(422)


"""
Updates drink with <id> if the 'patch:drinks' permission is present.
"""
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('delete:drinks')
def update_drink(drink_id):
    body = request.get_json()

    # if no form data
    if body is None:
        abort(404)

    updated_title = body.get('title')
    updated_recipe = body.get('recipe')

    old_drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if updated_title is None:
        updated_title = old_drink.title

    if updated_recipe is None:
        updated_recipe = old_drink.recipe
    else:
        updated_recipe = json.dumps(updated_recipe)

    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        drink.title = updated_title
        drink.recipe = updated_recipe

        drink.update()

        return jsonify({
          'success': True,
          'drinks': [drink.long()]
        })

    except:
        abort(422)


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


# Error Handling

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
401 Error: User lacks valid authentication credentials for the desired resource
'''


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
                    "success": False,
                    "error": 401,
                    "message": "unauthorized"
                    }), 401


'''
403 Error: Access to resource is forbidden.
'''


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
                    "success": False,
                    "error": 403,
                    "message": "forbidden"
                    }), 403


'''
500 Error: Arises in other cases.
'''


@app.errorhandler(500)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 500,
                    "message": "internal server error"
                    }), 500
