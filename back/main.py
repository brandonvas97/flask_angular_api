from flask import Flask, request, jsonify
from models import ma, Book, book_schema, books_schema
from database import db
from flasgger import Swagger
from flask_cors import CORS
import os
import uuid

app = Flask(__name__)
CORS(app)

app.config['SWAGGER'] = {
    "title": "Book API",
    "description": "API for managing books",
    "version": "1.0.0",
    "schemes": ["http"], 
}


swagger = Swagger(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ \
                os.path.join(basedir, 'db.sqlite3')


db.init_app(app)
ma.init_app(app)


with app.app_context():
    db.create_all()
    if Book.query.first() is None:
        default_books = [
            Book(id=uuid.uuid4().hex, title="On the Road", author="Jack Kerouac", read=True),
            Book(id=uuid.uuid4().hex, title="Bob", author="Harry Potter and the Philosopher's Stone", read=False),
            Book(id=uuid.uuid4().hex, title="Green Eggs and Ham", author="Dr. Seuss", read=True),
        ]
        db.session.bulk_save_objects(default_books)
        db.session.commit()

@app.route('/all', methods=["GET"])
def get_all_books():
    """
    Get all books
    ---
    tags:
      - Books
    summary: Retrieve all books from the database
    responses:
      200:
        description: A list of books
        schema:
          type: array
          items:
            properties:
              id:
                type: string
              title:
                type: string
              author:
                type: string
              read:
                type: boolean
    """
    books = Book.query.all()
    for book in books:
        if book.read is True:
            book.read = "Yes"
        else:
            book.read = "No"
    return books_schema.jsonify(books)

@app.route('/list/<id>', methods=["GET"])
def list_book(id):
    """
    List an existing book
    ---
    tags:
      - Books
    summary: List details of an existing book
    parameters:
      - name: id
        in: path
        required: true
        type: string
    responses:
      200:
        description: The obtained book
        schema:
            properties:
              id:
                type: string
              title:
                type: string
              author:
                type: string
              read:
                type: boolean
    """
    book = Book.query.get(id)
    if book is None:
        return jsonify({"Response":"Book not found"})

    return book_schema.jsonify(book)


@app.route('/add', methods=["POST"])
def add_book():
    """
    Add a new book
    ---
    tags:
      - Books
    summary: Add a new book to the collection
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            title:
              type: string
            author:
              type: string
            read:
              type: boolean
    responses:
      200:
        description: The created book
        schema:
            properties:
              id:
                type: string
              title:
                type: string
              author:
                type: string
              read:
                type: boolean
    """
    uuid1 = uuid.uuid4().hex
    title1 = request.json.get("title", None)
    author1 = request.json.get("author", None)
    read1 = request.json.get("read", None)
    if title1 is None or author1 is None or read1 is None:
        return jsonify({"Response":"Missing fields"})

    if type(read1) is not bool:
      if isinstance(read1, str):
          read1 = str.lower(read1)
          if read1 == 'false':
              read1 = False
          elif read1 == 'true':
              read1 = True
          else:
              return jsonify({"Response":"Not valid option in read field"})
      elif isinstance(read1, (int, float)):
          return jsonify({"Response":"Not valid option in read field"})
        
    new_book = Book(id=uuid1, title=title1, author=author1, read=read1)
    db.session.add(new_book)
    db.session.commit()
    return book_schema.jsonify(new_book)

@app.route('/edit/<id>', methods=["PUT"])
def edit_book(id):
    """
    Edit an existing book
    ---
    tags:
      - Books
    summary: Modify details of an existing book
    parameters:
      - name: id
        in: path
        required: true
        type: string
      - name: body
        in: body
        required: true
        schema:
          properties:
            title:
              type: string
            author:
              type: string
            read:
              type: boolean
    responses:
      200:
        description: The updated book
        schema:
            properties:
              id:
                type: string
              title:
                type: string
              author:
                type: string
              read:
                type: boolean
    """
    book = Book.query.get(id)
    title1 = request.json.get("title", None)
    author1 = request.json.get("author", None)
    read1 = request.json.get("read", None)

    if title1 is None or author1 is None or read1 is None:
        return jsonify({"Response":"Missing fields"})
    if book is None:
        return jsonify({"Response":"Book not found"})

    if type(read1) is not bool:
      if isinstance(read1, str):
          read1 = str.lower(read1)
          if read1 == 'false':
              read1 = False
          elif read1 == 'true':
              read1 = True
          else:
              return jsonify({"Response":"Not valid option in read field"})
      elif isinstance(read1, (int, float)):
          return jsonify({"Response":"Not valid option in read field"})

    book.title = title1
    book.author = author1
    book.read = read1
    db.session.commit()
    return book_schema.jsonify(book)

@app.route('/delete/<id>', methods=["DELETE"])
def delete_book(id):
    """
    Delete a book
    ---
    tags:
      - Books
    summary: Remove a book from the collection
    parameters:
      - name: id
        in: path
        required: true
        type: string
    responses:
      200:
        description: The deleted book
        schema:
            properties:
              id:
                type: string
              title:
                type: string
              author:
                type: string
              read:
                type: boolean
    """
    book = Book.query.get(id)
    if book is None:
        return jsonify({"Response":"Book not found"})
    
    db.session.delete(book)
    db.session.commit()
    return book_schema.jsonify(book)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)