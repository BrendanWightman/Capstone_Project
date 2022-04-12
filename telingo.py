from Telingo import create_app, socketio
from Telingo import events

app = create_app()

if __name__ == '__main__':
    socketio.run(app)