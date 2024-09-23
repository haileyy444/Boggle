from flask import Flask, render_template, request, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

boggle_game = Boggle()


@app.route("/")
def home():
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    plays = session.get("plays", 0)
    return render_template("app.html", board=board, highscore=highscore, plays=plays)



@app.route("/check-word")
def check_word():
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)
    # if response == "good": 
    #     return jsonify({'result': response, 'word': word})
    return jsonify({'result': response})




@app.route("/post-score", methods =["POST"])
def postScore():
    print("Printing scores")
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    plays = session.get("plays", 0)
    session['plays'] = plays+1
    session['highscore'] = max(score, highscore)
    return jsonify(brokeRecord=score > highscore)





if __name__ == "__main__":
    app.run(debug=True, port=5000)