from flask import *
from flask_socketio import *
import threading
import uuid
import os
import subprocess
import time
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

tasks ={}

@socketio.on('onconnect')
def onconnect(data):
    print(f'{data}')

@socketio.on('recieved')
def onrecieved(data):
    data = data.get('data')
    os.system('clear')
    print("--------------------------------------------------------")
    print(f'{data}')
    names = data.get('names')
    links = data.get('links')

    for i in range(len(names)):
        print(f'{names[i]} : {links[i]}')
        command = f'python pwdl.py --url {links[i]} --name {names[i]}'

        # Create a separate thread to run the command and capture stdout
        def run_command():
            process = subprocess.Popen(command, shell=True, stdout=sys.stdout, stderr=sys.stderr)
            while process.poll() is None:
                output = sys.stdout.readline()
                socketio.emit('stdout', {'output': output})
                socketio.emit('progress', {'progress':"Hello World"})
                time.sleep(0.01)

        thread = threading.Thread(target=run_command)
        thread.start()
    

@app.route("/",methods=["GET","POST"])
def hello_world():
    global tasks
    
    if request.method == "POST":
        
        session_uuid = request.form.get("session_uuid")
        names = request.form.getlist("name[]")
        links = request.form.getlist("link[]")
        
        tasks[session_uuid] = {'names':names,'links':links}

        socketio.emit('recieve', {'name': names, 'link': links})
        return render_template("progress.html",task=tasks[session_uuid])
        
    return render_template("index.html",session_uuid=str(uuid.uuid4()))

socketio.run(app,debug=True)
