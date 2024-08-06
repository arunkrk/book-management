from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    genre = db.Column(db.Text, nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    reviews = db.relationship('Review', backref='book', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
