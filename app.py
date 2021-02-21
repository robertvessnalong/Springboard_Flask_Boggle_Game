from flask.helpers import url_for
from boggle import Boggle
from flask import Flask, request, session, render_template, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import json
import ast

boggle_game = Boggle()


app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY'] = 'abc123'
toolbar = DebugToolbarExtension(app)

@app.route('/')
def render_board():
    """ This will render board, set session for current board,
        and render template
    """   
    current_board = boggle_game.make_board()
    session['current_board'] = current_board
    return render_template('index.j2', boggle=current_board)
   
@app.route('/', methods=["POST"])
def check_and_update():
     """ This will take guess and check if it is a valid word inside
         of dictionary.
         This will return to result back to axios
    """   
     if request.method == "POST":
       res = request.data
       decode_res = res.decode("UTF-8")
       updated_res = ast.literal_eval(decode_res)
       check = boggle_game.check_valid_word(session['current_board'], updated_res['guess'])
       return jsonify({"result": check})
        

@app.route('/completed')
def render_completed():
    """ This will take current session and add
        every time user has completed the game
    
    
    """
    session['count'] = session.get('count', 0) + 1
    return render_template('completed.j2')

@app.route('/completed', methods=["POST"])
def update_score():
    """ This will take score sent from axios 
        and update the session.
        It will check if current score is higher
        than session score.
    
    
    """
    if request.method == "POST":
        res = request.data
        decode_res = res.decode("UTF-8")
        updated_res = ast.literal_eval(decode_res)
        if session.get('highest_score') is not None:
            if session['highest_score'] < updated_res['score']:
                session['highest_score'] = updated_res['score']
        else:
            session['highest_score'] = 0
        return render_template('completed.j2')
