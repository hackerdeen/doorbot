from flask import Flask, request, jsonify, Response, render_template, session
import json
import time
import serial

import gnupg
gpg = gnupg.GPG()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

def unlock():
    ard = serial.Serial('/dev/ttyUSB0', 9600)
    ard.write('u')
    ard.close()

@app.route('/open', methods=['POST'])
def open_door():
    v = gpg.verify(request.form['command'])
    if v.valid and v.username == "hackhub <hub@57north.co>":
        command = gpg.decrypt(request.form['command'])
    else:
        return jsonify({'result': "signature verification failed"})
    ts = json.loads(command.data)['time']
    delta = int(time.time()) - ts 
    if delta > 120:
        return jsonify({'result': "Command time too far in the past (%d seconds)"%delta})
    unlock()
    return jsonify({'result': "SUCCESS!"})
