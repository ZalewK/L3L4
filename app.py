from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, BookSchema
from service import BookService
import json

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

migrate = Migrate(app, db)

db.init_app(app)

with app.app_context():
    db.create_all()

with open('appsettings.json') as config_file:
    app_settings = json.load(config_file)

base_url = app_settings['ApiSettings']['BaseUrl']
resource_endpoint = app_settings['ApiSettings']['ResourceEndpoint']
error_endpoint = app_settings['ApiSettings']['ErrorEndpoint']

books_endpoint = f'{resource_endpoint}'
book_withid_endpoint = f'{resource_endpoint}/<int:book_id>'
error_endpoint = f'{error_endpoint}'

@app.route(books_endpoint, methods=['GET'])
def get_books():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    paginated_books = BookService.get_all_books(page, per_page)

    return jsonify(paginated_books)

@app.route(book_withid_endpoint, methods=['GET'])
def get_book(book_id):
    book = BookService.get_book_by_id(book_id)
    if book:
        return jsonify(book)
    else:
        return jsonify({'message': 'Book not found'}), 400


@app.route(books_endpoint, methods=['POST'])
def add_book():
    data = request.get_json()

    book_schema = BookSchema()

    validation_errors = book_schema.validate(data)
    if validation_errors:
        return jsonify({'message': 'Not enough input data!', 'errors': validation_errors}), 400
    
    title = data.get('title')
    author = data.get('author')

    new_book = BookService.add_book(title, author)

    return jsonify(new_book)

@app.route(book_withid_endpoint, methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')

    updated_book = BookService.update_book(book_id, title, author)

    if updated_book:
        return jsonify(updated_book)
    else:
        return jsonify({'message': 'Book not found'}), 400


@app.route(book_withid_endpoint, methods=['DELETE'])
def delete_book(book_id):
    deleted_book = BookService.delete_book(book_id)
    if deleted_book:
        return jsonify(deleted_book)
    else:
        return jsonify({'message': 'Book not found'}), 400
    
@app.route(error_endpoint, methods=['GET'])
def simulate_error():
    try:
        raise Exception("Error test")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        BookService.clear_and_initialize_data()
    app.run(debug=True)
