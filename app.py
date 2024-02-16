from flask import *
from flask_socketio import *
import threading
import uuid
import os
import subprocess
import time
import sys
from io import *
import io


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
std_org= sys.stdout
output = io.StringIO()

tasks ={}

def run(name,url):
    from pwdl import m3u8_module
    m3u8_module(name,url)
     

def send_to_client():
    while sys.stdout == output:
        time.sleep(0.1)
        socketio.emit('stdout', {'output': output.getvalue()})

@socketio.on('onconnect')
def onconnect(data):
    std_org.write(f'{data}')

@socketio.on('recieved')
def onrecieved(data):
    data = data.get('data')
    os.system('clear')
    print("--------------------------------------------------------")
    print(f'{data}')
    names = data.get('names')
    links = data.get('links')
    for i in range(len(names)):
        name = names[i]
        url = links[i]

        
        sys.stdout = output
     
        t1 = threading.Thread(target=run,args=(name,url))
        t2 = threading.Thread(target=send_to_client)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        sys.stdout = std_org
        
    

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
