# views/routes.py
from flask import Blueprint, render_template, abort
from models.models import db, Joke
from flask import request, jsonify

view_bp = Blueprint('views', __name__)

def fetch_jokes():
    """
    Fetch all jokes that are not marked as deleted from the database.
    """
    jokes = Joke.query.filter_by(is_deleted=False).all()
    return jokes

def fetch_joke_by_id(joke_id):
    """
    Fetch a single joke by ID that is not marked as deleted.
    """
    joke = Joke.query.filter_by(id=joke_id, is_deleted=False).first()
    if joke is None:
        abort(404)
    return joke

@view_bp.route('/')
def home():
    return render_template('index.html')

@view_bp.route('/create')
def create():
    return render_template('create_joke.html')

@view_bp.route('/jokes')
def jokes():
    all_jokes = fetch_jokes()
    return render_template('view_jokes.html', jokes=all_jokes)

@view_bp.route('/jokes/<int:joke_id>')
def joke_details(joke_id):
    joke = fetch_joke_by_id(joke_id)
    return render_template('joke_details.html', joke=joke)

@view_bp.route('/search_jokes')
def search_jokes():
    search_query = request.args.get('query', '')
    if search_query:
        # Query to find jokes that match the search query and are not marked as deleted
        jokes = Joke.query.filter(Joke.joke.like(f'%{search_query}%'), Joke.is_deleted == False).all()
        # Return each joke as a dictionary with 'id' and 'joke' keys
        jokes_data = [{'id': joke.id, 'joke': joke.joke} for joke in jokes]
        return jsonify(jokes_data)
    return jsonify([])

