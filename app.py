import os
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            site TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('SELECT site, username, password FROM passwords')
    passwords = c.fetchall()
    conn.close()
    return render_template('index.html', passwords=passwords)

@app.route('/add', methods=['POST'])
def add():
    site = request.form['site']
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('INSERT INTO passwords (site, username, password) VALUES (?, ?, ?)',
              (site, username, password))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit', methods=['POST'])
def edit_password():
    original_site = request.form['original_site']
    new_site = request.form['site']
    new_username = request.form['username']
    new_password = request.form['password']
    
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''
        UPDATE passwords 
        SET site = ?, username = ?, password = ? 
        WHERE site = ?
    ''', (new_site, new_username, new_password, original_site))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
