from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('user.db')


@app.route('/', methods=['post', 'get'])
def login():
    username = request.form.get('username', False)
    password = request.form.get('password', False)
    if request.method == 'POST':
        conn = sqlite3.connect('user.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO user (username, password) VALUES (?,?)', (username, password))
        conn.commit()
        conn.close()
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)