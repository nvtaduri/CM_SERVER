import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)



@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        person = request.form['person']
        status = request.form['status']
        assigned = request.form['assigned']
        priority = request.form['priority']
        type = request.form['type']
        description = request.form['description']
        #person,status,assigned,priority,type,description
        if not person:
            flash('Person is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (person,status,assigned,priority,type,description) VALUES (?, ?,?,?,?,?)',
                         (person,status,assigned,priority,type,description))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=1000)