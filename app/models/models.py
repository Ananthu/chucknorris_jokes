from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Joke(db.Model):
    """
    Model class for a Joke.

    Attributes:
        id (int): Unique identifier for each joke, serves as the primary key.
        joke (str): The text of the joke, limited to 500 characters and cannot be null.
        is_deleted (bool): Flag to indicate whether the joke has been deleted, defaults to False.
        created_at (datetime): Timestamp for when the joke was created, defaults to the current UTC time.
        updated_at (datetime): Timestamp for the last update of the joke, updates on every change to the record.

    Methods:
        serialize(): Returns a dictionary of the joke data, suitable for JSON serialization.
    """

    # Columns definition
    id = db.Column(db.Integer, primary_key=True)
    joke = db.Column(db.String(500), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def serialize(self):
        """
        Serialize the joke instance to a dictionary.

        Returns:
            dict: A dictionary containing the joke's details, suitable for JSON serialization,
                  including the creation and last updated timestamps in ISO format.
        """
        return {
            'id': self.id,
            'joke': self.joke,
            'is_deleted': self.is_deleted,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
