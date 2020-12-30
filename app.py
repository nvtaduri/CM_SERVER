import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect,jsonify
from werkzeug.exceptions import abort
from search import SearchForm
import unicodedata
import json
import requests
import urllib.parse as urlparse
from urllib.parse import parse_qs


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True



def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    changes = conn.execute('SELECT * FROM posts').fetchall()
    row_list = []
    for row in changes:
        t = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]]
        col = ['id','person','created','status','assigned','priority','type','description']
        a = dict(zip(col,t))
        row_list.append(a)
    j = json.dumps(row_list)
    conn.close()
    return j


@app.route('/<int:id>')
def post(id):
    conn = get_db_connection()
    change = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (id,)).fetchone()
    data_list = []
    for row in change:
        data_list.append(row)
    col = ['id','person','created','status','assigned','priority','type','description']
    a = dict(zip(col,data_list))
    row_list = []
    row_list.append(a)
    j = json.dumps(row_list)
    conn.close()
    return j


@app.route('/create', methods=['GET','POST'])
def create():
    
        req_data = request.get_json(force = True)
        person = req_data.get('person')
        status = req_data.get('status')
        assigned = req_data.get('assigned')
        priority = req_data.get('priority')
        type = req_data.get('type')
        description = req_data.get('description')
        
        if not person:
            flash('Person is required!')
        else:
            conn = get_db_connection()
        
            conn.execute('INSERT INTO posts (person,status,assigned,priority,type,description) VALUES (?,?,?,?,?,?)',
                         (person,status,assigned,priority,type,description))
            conn.commit()
            conn.close()
            return{
                    "code": "success",
                    "message":"Change created"    
                    }

        return{
        "status": "change created"
        }
    

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=1000)