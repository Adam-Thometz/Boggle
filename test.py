from random import sample
from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class BoggleTests(TestCase):
    def setUp(self):
        self.client = app.test.client()
        app.config['TESTING'] = True

    def test_make_board(self):
        """Make sure the game and other HTML display"""
        
        with self.client:
            res = self.client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Welcome to Boggle</h1>', html)
            self.assertIn('board', session)

    def test_check_for_valid_guess(self):
        """Check that a word is valid and found on the board"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["H", "O", "G", "U", "Y"],
                                 ["A", "N", "G", "R", "Y"],
                                 ["M", "A", "N", "G", "O"],
                                 ["B", "I", "N", "G", "O"],
                                 ["Y", "M", "O", "R", "E"]]
                
                res = self.client.get('/check-word?word=hog')
                self.assertEqual(res.json['result'], 'ok')
    
    def test_not_on_board(self):
        """Check if word is on the board"""
        self.client.get('/')
        res = self.client.get('/check?word=impossible')
        self.assertEqual(res.json['result'], 'not-on-board')
    
    def test_not_word(self):
        """Check if word is in dictionary"""
        self.client.get('/')
        res = self.client.get('/check?word=bfehjribfhiersbfihebrdf')
        self.assertEqual(res.json['result'], 'not-word')