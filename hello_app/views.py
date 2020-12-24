from datetime import datetime
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit  
import sys
from time import sleep
from . import app
from sentimentApp.sentiment import chainSentimentList

socketio = SocketIO(app)                                                        
thread = None                                                                   


def background_thread():                                                        
    while True:                                                                 
        socketio.emit('message', f"Message:{sys.stdout}")                        
        sleep(5)       

@socketio.on('connect')                                                         
def connect():                                                                  
    global thread                                                               
    if thread is None:                                                          
        thread = socketio.start_background_task(target=background_thread)   

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/analyse/",methods=['GET', 'POST'])
def analyse():
    fromDate = request.form['fromMonthInput']
    fromMonth = int(fromDate.split('-')[1])
    fromYear = int(fromDate.split('-')[0])
    toDate = request.form['toMonthInput']
    toMonth = int(toDate.split('-')[1])
    toYear = int(toDate.split('-')[0])
    topics = request.form['hiddenTopicsInput']
    topicsList = topics.split()
    print(f"{fromMonth},{fromYear},{toMonth},{toYear},{topicsList}")
    chainSentimentList(topicsList,fromMonth,fromYear,toMonth,toYear)
    return 'OK'

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

