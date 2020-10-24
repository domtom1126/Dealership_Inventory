from flask import Flask, render_template, request, url_for, flash, redirect, session
import sqlite3
from datetime import timedelta, datetime
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


db = SQLAlchemy(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(128))
    date_created = db.Column(db.DateTime, default=datetime.now)

class Inventory(db.Model):
    vin = db.Column(db.String(17), primary_key = True)
    make = db.Column(db.String(25))
    model = db.Column(db.String(25))
    year = db.Column(db.Integer)
    color = db.Column(db.String(25))
    price = db.Column(db.Integer)
    mileage = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default = datetime.now)

app.secret_key='secret'
app.permanent_session_lifetime = timedelta(minutes=5)



@app.route('/', methods=['POST', 'GET'])
def login():
    return render_template('login.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    return render_template('logout.html')

@app.route('/dashboard', methods=['POST','GET'])
def dashboard():
    username_form = request.form.get('username')
    password_form = request.form.get('password')
    if request.method == 'POST':
        if username_form != None:
            user_login = User(username = username_form, password = password_form)
            db.session.add(user_login)
            db.session.commit()
    elif username_form == None:
        print('returned none')
        return render_template('dashboard.html')
    return render_template('dashboard.html' , username_form = username_form)

@app.route('/add_car', methods=['POST', 'GET'])
def add_car():
    return render_template('add_car.html')

@app.route('/car_added', methods=['POST', 'GET'])
def car_added():
    if request.method == 'POST':
        make = request.form['make']
        model =request.form['model']
        year = request.form['year']
        color = request.form['color']
        price = request.form['price']
        mileage = request.form['mileage']
        vin = request.form['vin']
        add_car_db = Inventory(make = make, model = model, year = year, color = color, price = price, mileage = mileage, vin = vin)
        db.session.add(add_car_db)
        db.session.commit()
    return render_template('car_added.html', make = make, model = model, year = year, color = color, price = price, vin = vin)

@app.route('/sell_car', methods=['POST', 'GET'])
def sell_car():
    return render_template('sell_car.html')

@app.route('/car_sold', methods=['POST', 'GET'])
def car_sold():
    if request.method == 'POST':
        vin = request.form['vin']
        conn = sqlite3.connect('user.sqlite3')
        cur = conn.cursor()
        cur.execute('DELETE FROM inventory WHERE vin = {}'.format(vin))
        conn.commit()
        conn.close()
    return render_template('car_sold.html', vin = vin)

# Still need to make sqlalchemy format
@app.route('/view_lot', methods=['POST', 'GET'])
def view_lot():
    conn = sqlite3.connect('inventory.db')
    cur = conn.cursor()
    select_all = cur.execute('SELECT * FROM inventory')
    display_all = select_all.fetchall()
    return render_template('view_lot.html', display_all=display_all)

if __name__ == '__main__':
    app.run(debug=True)
