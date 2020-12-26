import flask
from datetime import datetime
from flask import Flask, render_template, request, Response, send_file
from flask_socketio import SocketIO, emit 
import shutil
import os
from pathlib import Path
import subprocess
import re
import sys
import io
from contextlib import redirect_stdout
from time import sleep
app = flask.Flask(__name__)
from sentimentApp.sentiment import chainSentimentList

'''
socketio = SocketIO(app)                                                        
thread = None                                                                   


def background_thread():                                                        
    while True:                                                                 
        socketio.emit('message', f"Message:{'ping'}")                        
        sleep(5)       

@socketio.on('connect')                                                         
def connect():                                                                  
    global thread                                                               
    if thread is None:                                                          
        thread = socketio.start_background_task(target=background_thread)   
'''

@app.route("/")
def home():
    print(Path.cwd())
    return render_template("home.html")

zipFile_data = None
graph_data = None

@app.route("/analyse/",methods=['GET', 'POST'])
def analyse():
    print(request.form)
    fromDate = request.form['fromMonthInput']
    fromMonth = int(fromDate.split('-')[1])
    fromYear = int(fromDate.split('-')[0])
    toDate = request.form['toMonthInput']
    toMonth = int(toDate.split('-')[1])
    toYear = int(toDate.split('-')[0])
    topics = request.form['hiddenTopicsInput']
    topicsList = re.findall("(?<=\<).+?(?=\>)", topics)
    print(f"{fromMonth},{fromYear},{toMonth},{toYear},{topicsList}")
    '''
    with io.StringIO() as buf, redirect_stdout(buf):
        print('redirected')
        chainSentimentList(topicsList,fromMonth,fromYear,toMonth,toYear)
        output = buf.getvalue()
    print(f"The output:{output}")
    '''
    chainSentimentList(topicsList,fromMonth,fromYear,toMonth,toYear)
    
    # subprocess.run("python sentimentApp/sentiment.py",fromMonth,fromYear,toMonth,toYear)
    topicString = '+'.join(topicsList)
    data = f"{fromMonth}_{fromYear}-{toMonth}_{toYear}_{topicString}"
    print(f"sending {data} to client")

    # Handle Graph
    graph_file_path = f"{Path.cwd()}\outputs\{data}\outputGraph.jpg"
    global graph_data
    graph_data = io.BytesIO()
    with open(graph_file_path, 'rb') as fo:
        graph_data.write(fo.read())
    # (after writing, cursor will be at last byte, so move it to start)
    graph_data.seek(0)
    shutil.rmtree(f"{Path.cwd()}\outputs\{data}")
    print(f"removed {graph_file_path}")

    # Handle Zip File
    zip_file_path = f"{Path.cwd()}\zips\{data}.zip"
    global zipFile_data
    zipFile_data = io.BytesIO()
    with open(zip_file_path, 'rb') as fo:
        zipFile_data.write(fo.read())
    # (after writing, cursor will be at last byte, so move it to start)
    zipFile_data.seek(0)
    os.remove(zip_file_path)
    print(f"removed {zip_file_path}")

    return f'{data}'



@app.route("/output")
def output():
    data = request.args.get('data')
    print("received: ", request.args.get('data'))
    """
    # Handle Graph
    graph_file_path = f"{Path.cwd()}\outputs\{data}\outputGraph.jpg"
    global graph_data
    graph_data = io.BytesIO()
    with open(graph_file_path, 'rb') as fo:
        graph_data.write(fo.read())
    # (after writing, cursor will be at last byte, so move it to start)
    graph_data.seek(0)
    shutil.rmtree(f"{Path.cwd()}\outputs\{data}")
    print(f"removed {graph_file_path}")

    # Handle Zip File
    zip_file_path = f"{Path.cwd()}\zips\{data}.zip"
    global zipFile_data
    zipFile_data = io.BytesIO()
    with open(zip_file_path, 'rb') as fo:
        zipFile_data.write(fo.read())
    # (after writing, cursor will be at last byte, so move it to start)
    zipFile_data.seek(0)
    os.remove(zip_file_path)
    print(f"removed {zip_file_path}")
    """
    return send_file(graph_data,mimetype="image/jpeg")

@app.route("/download")
def download():
    print(zipFile_data)
    data = request.args.get('data')
    file_path = f"{Path.cwd()}\zips\{data}.zip"
    '''
    data = request.args.get('data')
    return_data = io.BytesIO()
    with open(file_path, 'rb') as fo:
        return_data.write(fo.read())
    # (after writing, cursor will be at last byte, so move it to start)
    return_data.seek(0)
    os.remove(file_path)
    print(f"removed {file_path}")
    '''
    return send_file(zipFile_data,mimetype="application/zip",as_attachment=True,attachment_filename=f"{data}.zip")


@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

