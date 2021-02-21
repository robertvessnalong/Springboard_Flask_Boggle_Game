from boggle import Boggle
from flask import session
from app import app
from unittest import TestCase

boggle_game = Boggle()

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class BoggleGameTest(TestCase):

    def test_board_render(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text = True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<li>', html)

    def test_check_and_update(self):
        with app.test_client() as client:
            res = client.post('/', data={
                'guess' : 'H'
            })
            html = res.get_data(as_text = True)
            self.assertEqual(res.status_code, 200)
            self.assertAlmostEqual('[]', html)

    def test_completed(self):
        with app.test_client() as client:
            res = client.get('/completed')
            html = res.get_data(as_text = True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2>', html)

    def test_post_completed(self):
        with app.test_client() as client:
            res = client.post('/completed', data={
                'score': 4
            })
            html = res.get_data(as_text = True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<p>Your highest score is 4</p>', html)