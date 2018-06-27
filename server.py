from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO, emit
# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@socketio.on('command', namespace='/log')
def test_message(message):
    print('command:' + message['data'])
    #emit('my_response', {'data': message['data']})

@socketio.on('my broadcast event', namespace='/log')
def test_message(message):
    emit('my_response', {'data': message['data']}, broadcast=True)

@socketio.on('connect', namespace='/log')
def test_connect():
    emit('my_response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/log')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)