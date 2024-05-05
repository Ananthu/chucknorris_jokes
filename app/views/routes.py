# views/routes.py
from flask import Blueprint, render_template, abort, request, jsonify
from models.models import db, Joke

view_bp = Blueprint('views', __name__)

def fetch_jokes():
    """
    Fetch all jokes from the database that are not marked as deleted.

    Returns:
        list: A list of Joke instances that are active (not deleted).
    """
    jokes = Joke.query.filter_by(is_deleted=False).all()
    return jokes

def fetch_joke_by_id(joke_id):
    """
    Fetch a single joke by its ID, ensuring it is not marked as deleted.
    If the joke does not exist, it aborts the request with a 404 error.

    Args:
        joke_id (int): The ID of the joke to retrieve.

    Returns:
        Joke: The Joke instance if found.
    """
    joke = Joke.query.filter_by(id=joke_id, is_deleted=False).first()
    if joke is None:
        abort(404)
    return joke

@view_bp.route('/')
def home():
    """
    Render the home page of the application.
    """
    return render_template('index.html')

@view_bp.route('/create')
def create():
    """
    Render the page to create a new joke.
    """
    return render_template('create_joke.html')

@view_bp.route('/jokes')
def jokes():
    """
    Display all jokes that are not deleted in a list format.
    """
    all_jokes = fetch_jokes()
    return render_template('view_jokes.html', jokes=all_jokes)

@view_bp.route('/jokes/<int:joke_id>')
def joke_details(joke_id):
    """
    Display the details of a specific joke based on its ID.

    Args:
        joke_id (int): The ID of the joke to display.
    """
    joke = fetch_joke_by_id(joke_id)
    return render_template('joke_details.html', joke=joke)

@view_bp.route('/search_jokes')
def search_jokes():
    """
    Search for jokes that contain the provided query string and are not deleted.

    Returns:
        JSON: A list of jokes that match the search criteria.
    """
    search_query = request.args.get('query', '')
    if search_query:
        jokes = Joke.query.filter(Joke.joke.like(f'%{search_query}%'), Joke.is_deleted == False).all()
        jokes_data = [{'id': joke.id, 'joke': joke.joke} for joke in jokes]
        return jsonify(jokes_data)
    return jsonify([])

