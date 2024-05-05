import unittest
from flask import url_for
from flask_testing import TestCase
from flaskblog import app, db
from flaskblog.models import User, Post

class IntegrationTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        return app

    def setUp(self):
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register_login(self):
        response = self.client.post(url_for('register'), data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }, follow_redirects=True)

        self.assert200(response)
        self.assertIn(b'Account created!', response.data)

        response = self.client.post(url_for('login'), data={
            'email': 'test@example.com',
            'password': 'testpassword'
        }, follow_redirects=True)

        self.assert200(response)
        self.assertIn(b'Welcome, testuser!', response.data)

    def test_create_update_delete_post(self):
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()

        self.client.post(url_for('login'), data={
            'email': 'test@example.com',
            'password': 'testpassword'
        })

        response = self.client.post(url_for('create_post'), data={
            'title': 'New Post',
            'content': 'This is a new post'
        }, follow_redirects=True)

        self.assert200(response)
        self.assertIn(b'Post created!', response.data)

        post = Post.query.filter_by(title='New Post').first()
        post_id = post.id

        response = self.client.post(url_for('update_post', post_id=post_id), data={
            'title': 'Updated Post',
            'content': 'This post has been updated'
        }, follow_redirects=True)

        self.assert200(response)
        self.assertIn(b'Post updated!', response.data)

        response = self.client.post(url_for('delete_post', post_id=post_id), follow_redirects=True)

        self.assert200(response)
        self.assertIn(b'Post deleted!', response.data)

if __name__ == '__main__':
    unittest.main()