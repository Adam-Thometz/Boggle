from boggle import Boggle
from flask import Flask, request, render_template, jsonify, session
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Protest_The_Hero'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# app.debug = True

# toolbar = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def show_boggle_board():
    """Show Boggle board"""
    board = boggle_game.make_board()
    session['board'] = board
    high_score = session.get('high_score', 0)
    plays = session.get('plays', 0)

    return render_template('boggle.html', board = board, high_score = high_score, plays = plays)

@app.route('/check')
def check_for_valid_guess():
    """Check if word is in the dictionary"""
    # import pdb
    # pdb.set_trace()
    word = request.args['word']
    board = session['board']
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})

@app.route('/post-score', methods=['POST'])
def post_score():
    """Post the final score when the game finishes and update high score if needed"""
    score = request.json['score']
    high_score = session.get('high_score', 0)
    plays = session.get('plays', 0)

    session['plays'] = plays + 1
    session['high_score'] = max(score, high_score)

    return jsonify(brokeRecord = score > high_score)