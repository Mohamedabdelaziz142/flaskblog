import unittest
from flaskblog import app, db
from flaskblog.models import User, Post

class FlaskBlogTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

        user = User(username='testuser', email='test@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login(self):
        response = self.app.post('/login', data={
            'email': 'test@example.com',
            'password': 'testpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, testuser!', response.data)

        response = self.app.post('/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login unsuccessful', response.data)

    def test_create_post(self):
        self.app.post('/login', data={
            'email': 'test@example.com',
            'password': 'testpassword'
        }, follow_redirects=True)

        response = self.app.post('/post/new', data={
            'title': 'New Post',
            'content': 'This is a new post'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post created!', response.data)

        response = self.app.post('/post/new', data={
            'title': '',
            'content': 'This is a new post'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Title is required', response.data)

    def test_delete_post(self):
        self.app.post('/login', data={
            'email': 'test@example.com',
            'password': 'testpassword'
        }, follow_redirects=True)

        post = Post(title='Test Post', content='This is a test post', author_id=1)
        db.session.add(post)
        db.session.commit()

        response = self.app.post(f'/post/{post.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post deleted!', response.data)

    def test_update_post(self):
        self.app.post('/login', data={
            'email': 'test@example.com',
            'password': 'testpassword'
        }, follow_redirects=True)

        post = Post(title='Test Post', content='This is a test post', author_id=1)
        db.session.add(post)
        db.session.commit()

        response = self.app.post(f'/post/{post.id}/update', data={
            'title': 'Updated Post',
            'content': 'This post has been updated'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post updated!', response.data)

        response = self.app.post(f'/post/{post.id}/update', data={
            'title': '',
            'content': 'This post has been updated'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Title is required', response.data)

if __name__ == '__main__':
    unittest.main()