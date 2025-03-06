import uuid
from database import db
from flask_marshmallow import Marshmallow

ma = Marshmallow()

class Book(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(255))
    read = db.Column(db.Boolean())

    def __init__(self, id, title, author, read):
        self.id = id
        self.title = title
        self.author = author
        self.read = read

class BookSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "author", "read")

book_schema = BookSchema()
books_schema = BookSchema(many=True)