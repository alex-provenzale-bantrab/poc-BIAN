from prp import create_app
import threading
from prp.EDA.listener_thread import start_listener

app = create_app()

def start_listener_thread():
    listener_thread = threading.Thread(target=start_listener, args=("bian-coreless4-poc", app), daemon=True)
    listener_thread.start()

if __name__ == '__main__':
    # Initiate a listener thread decoupled
    start_listener_thread()
    # Execute flask application
    app.run(host='0.0.0.0', port=5000, debug=True)