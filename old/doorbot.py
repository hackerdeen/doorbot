from flask import Flask, request, jsonify, Response, render_template, session
import json
import time
from subprocess import Popen

import gnupg
gpg = gnupg.GPG()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

def unlock():
    Popen("/home/pi/unlock.py")
    
@app.route('/open', methods=['POST'])
def open_door():
    msg = open("msg.txt", "w")
    msg.write(request.form['command'])
    msg.close()
    v = gpg.verify(request.form['command'])
    if v.valid and v.username == "hackhub <hub@57north.co>":
        command = gpg.decrypt(request.form['command'])
    else:
        return jsonify({'result': "signature verification failed" + str(v.valid) + str(v.username)})
    ts = json.loads(command.data)['time']
    delta = int(time.time()) - ts 
    if delta > 120:
        return jsonify({'result': "Command time too far in the past (%d seconds)"%delta})
    unlock()
    return jsonify({'result': "SUCCESS!"})
