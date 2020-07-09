from flask import Flask, render_template, request, redirect
import datetime
from flask_apscheduler import APScheduler

import sqlite3

app = Flask(__name__)



conn = sqlite3.connect('database.db')

conn.execute('''CREATE TABLE IF NOT EXISTS tableee
         (id INTEGER NOT NULL PRIMARY KEY,
         title TEXT,
         datetime timestamp);''')
conn.commit()



@app.route('/')
def index():
    return 'hello world'


@app.route('/posts/<title>', methods= ['GET','POST'])
def posts(title):
    conn = sqlite3.connect('database.db')
    conn.execute("INSERT INTO tableee(title,datetime) values(?,?)" ,(title,datetime.datetime.now()))
    conn.commit()
    scheduler = APScheduler()
    scheduler.add_job(func=delete,args=[title],run_date=datetime.datetime.now()+datetime.timedelta(0,5),id='title')
    scheduler.start()
    return 'inserted '+title


def delete(title):
    conn = sqlite3.connect('database.db')
    data=conn.execute("DELETE from tableee where title = '"+title+"'")
    conn.commit()
    return 'deleted '+title

if __name__== "__main__":
    app.run(debug=True)
