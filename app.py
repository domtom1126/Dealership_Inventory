from flask import Flask, render_template, request, url_for, flash, redirect, session
import sqlite3
from datetime import timedelta
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
conn = sqlite3.connect('user.db')

app.secret_key='secret'
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
        return render_template('login.html')

@app.route('/dashboard', methods=['POST','GET'])
def dashboard():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('user.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO user (username, password) VALUES (?,?)', (username, password))
        conn.commit()
        conn.close()
    return render_template('dashboard.html', username = username )

@app.route('/add_car', methods=['POST', 'GET'])
def add_car():
    if request.method == 'POST':
        make = request.form['make']
        model =request.form['model']
        year = request.form['year']
        color = request.form['color']
        price = request.form['price']
        conn = sqlite3.connect('inventory.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO inventory (make, model, year, color, price) VALUES (?,?,?,?,?)', (make, model, year, color, price))
        conn.commit()
        conn.close()
    return render_template('add_car.html')

@app.route('/car_added', methods=['POST', 'GET'])
def car_added():
    if request.method == 'POST':
        make = request.form['make']
        model =request.form['model']
        year = request.form['year']
        color = request.form['color']
        price = request.form['price']
        conn = sqlite3.connect('inventory.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO inventory (make, model, year, color, price) VALUES (?,?,?,?,?)', (make, model, year, color, price))
        conn.commit()
        conn.close()
    return render_template('car_added.html', make = make, model = model, year = year, color = color, price = price)

@app.route('/sell_car', methods=['POST', 'GET'])
def sell_car():
    return render_template('sell_car.html')

@app.route('/car_sold', methods=['POST', 'GET'])
def car_sold():
    if request.method == 'POST':
        id = request.form['id']
        # make = request.form['make']
        # model =request.form['model']
        # year = request.form['year']
        # color = request.form['color']
        # price = request.form['price']
        conn = sqlite3.connect('inventory.db')
        cur = conn.cursor()
        cur.execute('DELETE FROM inventory WHERE id = {}'.format(id))
        conn.commit()
        conn.close()
    return render_template('car_sold.html', id = id)

@app.route('/view_lot', methods=['POST', 'GET'])
def view_lot():
    conn = sqlite3.connect('inventory.db')
    cur = conn.cursor()
    select_all = cur.execute('SELECT * FROM inventory')
    display_all = select_all.fetchall()
    return render_template('view_lot.html', display_all=display_all)
if __name__ == '__main__':
    app.run(debug=True)
