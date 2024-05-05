from flask import Blueprint, jsonify, request, abort
from models.models import db, Joke

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/jokes/', methods=['POST'])
def create_joke():
    data = request.json
    joke = Joke(joke=data['joke'])
    db.session.add(joke)
    db.session.commit()
    return jsonify({'id': joke.id}), 201

@api_bp.route('/jokes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def joke(id):
    print("joke related request received")
    if request.method == 'GET':
        return get_joke(id)
    elif request.method == 'PUT':
        return update_joke(id)
    elif request.method == 'DELETE':
        return delete_joke(id)



def get_joke(id):
    joke = Joke.query.filter_by(id=id, is_deleted=False).first()
    if joke:
        return jsonify({'id': joke.id, 'joke': joke.joke})
    else:
        abort(404, description="Joke not found")

def update_joke(id):
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
    print("delete_joke")
    joke = Joke.query.filter_by(id=id).first()
    if joke:
        joke.is_deleted = True
        db.session.commit()
        return '', 204
    else:
        abort(404, description="Joke not found")
