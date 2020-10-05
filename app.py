from flask import Flask, render_template, request, url_for
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('user.db')


@app.route('/', methods=['POST', 'GET'])
def login():
    # username = request.form.get('username')
    # password = request.form.get('password', False)
    # if request.method == 'POST':
    #     conn = sqlite3.connect('user.db')
    #     cur = conn.cursor()
    #     cur.execute('INSERT INTO user (username, password) VALUES (?,?)', (username, password))
    #     conn.commit()
    #     conn.close()
    return render_template('login.html')

@app.route('/dashboard', methods=['POST','GET'])
def dashboard():
    if request.method == 'POST':
        username = request.form['username']
    return render_template('dashboard.html', username = username )


if __name__ == '__main__':
    app.run(debug=True)