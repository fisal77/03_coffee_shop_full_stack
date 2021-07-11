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
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO - (DONE) implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks')
# @requires_auth() no need because public
def get_drinks():
    drinks = Drink.query.all()
    if len(drinks) == 0:
        abort(404)

    drink_list = [drink.short() for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': drink_list
    })


'''
@TODO - (DONE) implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    # print(payload)
    drinks = Drink.query.all()
    drinks_detail_list = [drink.long() for drink in drinks]
    if len(drinks_detail_list) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'drinks': drinks_detail_list
    })


'''
@TODO - (DONE) implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_new_drink(payload):
    json_body = request.get_json()
    title_input = json_body.get('title', None)
    recipe_input = json_body.get('recipe', None)

    # Before: [{'name': 'Esspresso', 'color': 'brown', 'parts': 2}]
    # After: [{"name": "Esspresso", "color": "brown", "parts": 2}]
    if not str(recipe_input).startswith('[') \
            and not str(recipe_input).endswith(']'):
        recipe_input = '[' + str(recipe_input).replace("'", '"') + ']'
    else:
        recipe_input = str(recipe_input).replace("'", '"')

    print(recipe_input)

    try:
        is_title_exist = Drink.query.filter(Drink.title == title_input).one_or_none()
        if is_title_exist is None:
              print('is_title_exist is None')
              inserted_drink = Drink(title=title_input, recipe=recipe_input)
              inserted_drink.insert()
              inserted_drink = Drink.query.filter(Drink.title == title_input).all()
              print("OK-DEBUG")
              drink = [drink_row.long() for drink_row in inserted_drink]
              return jsonify({
                  'success': True,
                  'drinks': drink
              })
        else:
            abort(422)
    except:
        abort(422)


'''
@TODO - (DONE) implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if drink is not None:
        json_body = request.get_json()
        title_input = json_body.get('title')
        recipe_input = json_body.get('recipe')

        if not str(recipe_input).startswith('[') \
                and not str(recipe_input).endswith(']'):
            recipe_input = '[' + str(recipe_input).replace("'", '"') + ']'
        else:
            recipe_input = str(recipe_input).replace("'", '"')
                
        drink.title = title_input
        drink.recipe = recipe_input
        drink.update()
        updated_drink = Drink.query.filter(Drink.id == drink_id).all()
        print("OK-DEBUG")
        drink = [drink_row.long() for drink_row in updated_drink]
        return jsonify({
            'success': True,
            'drinks': drink
        })
    else:
        abort(404)


'''
@TODO - (DONE) implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        if drink is None:
            abort(404)
        drink.delete()

        return jsonify({
            'success': True,
            'delete': drink_id
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
@TODO - (DONE) implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO -(DONE) implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def not_found(error):
  return jsonify({
    "success": False,
    "error": 404,
    "message": "resource not found"
    }), 404


@app.errorhandler(400)
def bad_request(error):
  return jsonify({
    "success": False,
    "error": 400,
    "message": "bad request"
    }), 400



'''
@TODO - (DONE) implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(401)
def auth_error(error):
  return jsonify({
    "success": False,
    "error": 401,
    "message": "Unauthorized"
    }), 401


@app.errorhandler(403)
def auth_error(error):
  return jsonify({
    "success": False,
    "error": 403,
    "message": "Unauthorized"
    }), 403