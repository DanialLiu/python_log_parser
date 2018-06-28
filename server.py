from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO, emit
import logparser
# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

logs = []

def filter_log(level, tag, search):
    if level == 0 and not tag and not search:
        return logs
    result = []
    for l in logs:
        if 'level_num' in l and l['level_num'] < level:
            continue
        if 'tag' in l and tag and l['tag'] != tag:
            continue
        if 'text' in l and search and l['text'].find(search) == -1:
            continue
        result.append(l)
    print('filter log length:%d' % len(result))
    return result
@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@socketio.on('log_fetch', namespace='/log')
def log_fetch(message):
    try:
        print('log_fetch enter')
        level = 0
        tag = None
        search = None
        if 'level' in message:
            level = int(message['level'])
        if 'tag' in message:
            tag = message['tag']
        if 'search' in message:
            search = message['search']
        print('log_fetch level:%d tag:%s search:%s' % (level, tag, search))
        emit('log_fetch', {'data': filter_log(level, tag, search)})
    except Exception as e:
        raise e
    

@socketio.on('connect', namespace='/log')
def test_connect():
    emit('my_response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/log')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    logs = logparser.readlog("log.log")
    socketio.run(app, debug=True)
