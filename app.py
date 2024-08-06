from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from models import db, Book, Review

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/books', methods=['POST'])
def add_book():
    added_books = []
    data = request.get_json()
    print("Type of Data", type(data))
    if type(data) is dict:
        print('title', data['title'])
        print('author', data['author'])
        print('year_published', data['year_published'])
        print('genre', data['genre'])
        new_book = Book(title=data['title'], author=data['author'], year_published=data['year_published'], genre=data['genre'])
        db.session.add(new_book)
        added_books.append({'id': new_book.id, 'title': new_book.title, 'author': new_book.author})
        db.session.commit()
    elif type(data) is list:
        for item in data:
            if 'title' not in item or 'author' not in item:
                return jsonify({'error': 'Each book must have a title and author.'}), 400
    
            new_book = Book(title=item['title'], author=item['author'], year_published=item['year_published'], genre=item['genre'])
            db.session.add(new_book)
            added_books.append({'id': new_book.id, 'title': new_book.title, 'author': new_book.author})

        db.session.commit()
    return jsonify({'books': added_books}), 201

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({
        'title': book.title,
        'author': book.author,
        'summary': book.summary,
        'genre': book.genre,
        'year_published': book.year_published,
        'reviews': [{'rating': r.rating, 'review_text': r.review_text} for r in book.reviews]
    })

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    book = Book.query.get_or_404(book_id)
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    db.session.commit()
    return jsonify({'message': 'Book updated'})

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted'})

@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.get_json()
    print('data',data)
    new_review = Review(book_id=data['book_id'], rating=data['rating'], review_text=data['review_text'], user_id=data['user_id'])
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'id': new_review.id}), 201

@app.route('/books/<int:book_id>/reviews', methods=['GET'])
def get_reviews(book_id):
    reviews = Review.query.filter_by(book_id=book_id).all()
    return jsonify([{'rating': r.rating, 'review_text': r.review_text} for r in reviews])

@app.route('/books/<int:book_id>/summary', methods=['GET'])
def rating_summary(book_id):
    book = Book.query.get_or_404(book_id)
    reviews = Review.query.filter_by(book_id=book_id).all()
    if not reviews:
        return jsonify({'message': 'No reviews found'}), 404
    avg_rating = sum(r.rating for r in reviews) / len(reviews)
    return jsonify({'average_rating': avg_rating, 'review_count': len(reviews)})

if __name__ == '__main__':
    app.run(debug=True)
