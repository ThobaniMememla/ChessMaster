from flask import Flask, jsonify, request
from flask_cors import CORS
import chess
import chess.engine

app = Flask(__name__)
CORS(app)

# Initialize the chess board
board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci("stockfish") 

@app.route('/api/move', methods=['POST'])
def make_move():
    data = request.json
    user_move = data.get('move')

    try:
        board.push_san(user_move)
        ai_move = engine.play(board, chess.engine.Limit(time=1.0))
        board.push(ai_move.move)

        return jsonify({
            'board': board.fen(),
            'ai_move': ai_move.move.uci()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/reset', methods=['POST'])
def reset_game():
    global board
    board = chess.Board()
    return jsonify({'board': board.fen()})

if __name__ == '__main__':
    app.run(debug=True)
