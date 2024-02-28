from flask import Flask, render_template, request, jsonify
from threading import Thread, Lock
import FyersWebSocket as Fskt
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

websocket_running = False
lock = Lock()

def start_websocket():
    global websocket_running
    with lock:
        if not websocket_running:
            websocket_running = True
            Fskt.main()
            print("WebSocket has started.")
        else:
            print("WebSocket is already running.")

def stop_websocket():
    global websocket_running
    with lock:
        if websocket_running:
            Fskt.stop_websocket()  
            websocket_running = False
            print("WebSocket has been stopped.")
        else:
            print("WebSocket is not running.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    if not websocket_running:
        thread = Thread(target=start_websocket)
        thread.start()
        return jsonify({'message': 'WebSocket started'})
    else:
        return jsonify({'message': 'WebSocket is already running'})

@app.route('/stop', methods=['POST'])
def stop():
    stop_websocket()
    return jsonify({'message': 'WebSocket Stopped'})

@app.route('/get-messages', methods=['GET'])
def get_messages():
    # Make sure Fskt.get_messages() is implemented correctly to return the messages.
    return jsonify({'messages': Fskt.get_messages()})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
