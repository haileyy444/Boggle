from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home(self):
        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('plays'))
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)


    def test_words(self):
        with self.client.session_transaction() as sesh:
            sesh['board'] = [["C", "A", "T"]]
        response = self.client.get('/check-word?word=cat')
        self.assertEqual(response.json['result'], 'good')


    def test_wrong_word(self):
        self.client.get('/')
        response = self.client.get('/check-word?word=wrong')
        self.assertEqual(response.json['result'], 'not-on-board')

    def not_word(self): 
        self.client.get('/')
        response = self.client.get('/check-word?word=dsfddegefwew')
        self.assertEqual(response.json['result'], 'not-word')