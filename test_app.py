import unittest
import json
from app import app, db, Book, Review

class BookManagementTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.config.from_object('config.TestConfig')
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        """Set up a fresh database session for each test."""
        self.client = self.app.test_client()

    def tearDown(self):
        """Rollback the database changes after each test."""
        db.session.remove()
        db.drop_all()
        db.create_all()

    def test_add_book(self):
        response = self.client.post('/books', json={'title': 'Book 1', 'author': 'Author 1', 'genre': 'Fiction', 'year_published': 2021})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('books', data)

    def test_add_books_list(self):
        books = [
            {'title': 'Book 2', 'author': 'Author 2', 'genre': 'Non-Fiction', 'year_published': 2020},
            {'title': 'Book 3', 'author': 'Author 3', 'genre': 'Science Fiction', 'year_published': 2019}
        ]
        response = self.client.post('/books', json=books)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('books', data)

    def test_get_book(self):
        book = Book(title='Book 4', author='Author 4', genre='Fantasy', year_published=2018)
        db.session.add(book)
        db.session.commit()
        response = self.client.get(f'/books/{book.id}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['title'], 'Book 4')
        self.assertEqual(data['author'], 'Author 4')
        self.assertEqual(data['genre'], 'Fantasy')
        self.assertEqual(data['year_published'], 2018)

    def test_update_book(self):
        book = Book(title='Book 5', author='Author 5', genre='Horror', year_published=2017)
        db.session.add(book)
        db.session.commit()
        response = self.client.put(f'/books/{book.id}', json={'title': 'Updated Book 5', 'genre': 'Thriller'})
        self.assertEqual(response.status_code, 200)
        updated_book = Book.query.get(book.id)
        self.assertEqual(updated_book.title, 'Updated Book 5')

    def test_delete_book(self):
        book = Book(title='Book 6', author='Author 6', genre='Romance', year_published=2016)
        db.session.add(book)
        db.session.commit()
        response = self.client.delete(f'/books/{book.id}')
        self.assertEqual(response.status_code, 200)
        deleted_book = Book.query.get(book.id)
        self.assertIsNone(deleted_book)

    def test_add_review(self):
        book = Book(title='Book 8', author='Author 8', genre='History', year_published=2014)
        db.session.add(book)
        db.session.commit()
        review_data = {'rating': 5, 'review_text': 'Great book!', 'user_id': 1, 'book_id': book.id}
        response = self.client.post('/reviews', json=review_data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', data)

    def test_get_reviews(self):
        book = Book(title='Book 9', author='Author 9', genre='Adventure', year_published=2013)
        db.session.add(book)
        db.session.commit()
        review = Review(rating=4, review_text='Good read', book_id=book.id, user_id=1)
        db.session.add(review)
        db.session.commit()
        response = self.client.get(f'/books/{book.id}/reviews')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['rating'], 4)
        self.assertEqual(data[0]['review_text'], 'Good read')

    def test_rating_summary(self):
        book = Book(title='Book 10', author='Book Author', genre='Mystery', year_published=2012)
        db.session.add(book)
        db.session.commit()
        reviews = [
            Review(rating=3, review_text='Okay', book_id=book.id, user_id=1),
            Review(rating=5, review_text='Excellent', book_id=book.id, user_id=2)
        ]
        db.session.add_all(reviews)
        db.session.commit()
        response = self.client.get(f'/books/{book.id}/summary')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['average_rating'], 4.0)
        self.assertEqual(data['review_count'], 2)

if __name__ == '__main__':
    unittest.main()
