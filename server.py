from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@socketio.on("start game")
def start_game(game_settings):
    print(game_settings['mapName'])
    print(game_settings['agentOneType'])
    print(game_settings['agentOneName'])
    print(game_settings['agentTwoType'])
    print(game_settings['agentTwoName'])

@socketio.on("update state")
def update_state(new_state):
    emit("update state", new_state)

@socketio.on('connect')
def test_connect():
    print("Connected")

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    print("Server is up running at http://127.0.0.1:5000")
    socketio.run(app)

