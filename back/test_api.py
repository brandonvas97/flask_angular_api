import pytest
from main import app, db, Book
import json
import uuid

@pytest.fixture
def client():
    """Fixture to create a test client and an in-memory database."""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    
    with app.app_context():
        db.create_all()
        yield app.test_client()  # Provide the test client
        db.session.remove()
        db.drop_all()

def test_get_all_books(client):
    """Test retrieving all books (GET /all)."""
    # Pre-insert a book into the database
    response_pre_insert = Book.query.all()
    data_pre_insert = len(response_pre_insert)
    with app.app_context():
        book = Book(id=uuid.uuid4().hex, title="Test Book", author="Author", read=False)
        db.session.add(book)
        db.session.commit()

    # Send request
    response = client.get("/all")
    
    # Assertions
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == data_pre_insert + 1
    assert data[3]["title"] == "Test Book"

def test_add_book(client):
    """Test adding a book (POST /add)."""
    new_book = {
        "title": "New Book",
        "author": "New Author",
        "read": True
    }

    # Send request
    response = client.post("/add", data=json.dumps(new_book), content_type="application/json")

    # Assertions
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "New Book"
    assert data["author"] == "New Author"
    assert data["read"] is True

    # Verify in database
    with app.app_context():
        book = Book.query.filter_by(title="New Book").first()
        assert book is not None
        assert book.author == "New Author"
        assert book.read is True

def test_edit_book(client):
    """Test editing a book (PUT /edit/<id>)."""
    with app.app_context():
        book = Book(id=uuid.uuid4().hex, title="Old Title", author="Old Author", read=False)
        db.session.add(book)
        db.session.commit()
        book_id = book.id  # Store the ID before exiting the context

    updated_data = {
        "title": "Updated Title",
        "author": "Updated Author",
        "read": True
    }

    # Send request
    response = client.put(f"/edit/{book_id}", data=json.dumps(updated_data), content_type="application/json")

    # Assertions
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Updated Title"
    assert data["author"] == "Updated Author"
    assert data["read"] is True

    # Verify in database with a new query inside an application context
    with app.app_context():
        updated_book = Book.query.get(book_id)
        assert updated_book is not None
        assert updated_book.title == "Updated Title"
        assert updated_book.author == "Updated Author"
        assert updated_book.read is True

def test_delete_book(client):
    """Test deleting a book (DELETE /delete/<id>)."""
    with app.app_context():
        book = Book(id=uuid.uuid4().hex, title="To Be Deleted", author="Author", read=False)
        db.session.add(book)
        db.session.commit()
        book_id = book.id  # Store the ID before exiting the context

    # Send request
    response = client.delete(f"/delete/{book_id}")

    # Assertions
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "To Be Deleted"

    # Verify in database with a new query inside an application context
    with app.app_context():
        deleted_book = Book.query.get(book_id)
        assert deleted_book is None  # Ensure it's deleted
