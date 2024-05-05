from flask import Blueprint, jsonify, request, abort
from models.models import db, Joke

# Initialize Blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/jokes/', methods=['POST'])
def create_joke():
    """
    Create a new joke in the database from a JSON request.
    Expects a JSON with a 'joke' key.

    Returns:
        JSON response with the new joke's ID and HTTP status 201.
    """
    data = request.json
    joke = Joke(joke=data['joke'])
    db.session.add(joke)
    db.session.commit()
    return jsonify({'id': joke.id}), 201

@api_bp.route('/jokes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def joke(id):
    """
    Dispatch to the appropriate function based on method type for joke operations.

    Args:
        id (int): The ID of the joke to manipulate.

    Returns:
        JSON response or abort with error depending on the operation.
    """
    print("joke related request received")
    if request.method == 'GET':
        return get_joke(id)
    elif request.method == 'PUT':
        return update_joke(id)
    elif request.method == 'DELETE':
        return delete_joke(id)

def get_joke(id):
    """
    Retrieve a joke by its ID if not marked as deleted.

    Args:
        id (int): The ID of the joke to retrieve.

    Returns:
        JSON response with joke details or 404 error if not found.
    """
    joke = Joke.query.filter_by(id=id, is_deleted=False).first()
    if joke:
        return jsonify({'id': joke.id, 'joke': joke.joke})
    else:
        abort(404, description="Joke not found")

def update_joke(id):
    """
    Update an existing joke's content if it's not marked as deleted.

    Args:
        id (int): The ID of the joke to update.

    Returns:
        JSON response with updated joke details or error if inappropriate content type or not found.
    """
    print("Attempting to update joke with ID:", id)  # Log ID
    if request.headers['Content-Type'] != 'application/json':
        print("Received headers:", request.headers)  # Log received headers
        abort(415, description="Unsupported Media Type")
    
    data = request.get_json()  # Safely get data
    print("Received data:", data)  # Log data
    
    joke = Joke.query.filter_by(id=id).first()
    if joke and not joke.is_deleted:
        joke.joke = data['joke']
        db.session.commit()
        return jsonify({'id': joke.id, 'joke': joke.joke})
    else:
        abort(404, description="Joke not found or deleted")

def delete_joke(id):
    """
    Mark a joke as deleted in the database.

    Args:
        id (int): The ID of the joke to delete.

    Returns:
        Empty response with HTTP status 204 or 404 error if not found.
    """
    print("delete_joke")
    joke = Joke.query.filter_by(id=id).first()
    if joke:
        joke.is_deleted = True
        db.session.commit()
        return '', 204
    else:
        abort(404, description="Joke not found")
