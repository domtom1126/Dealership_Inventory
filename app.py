from flask import Flask, render_template, request, url_for
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('user.db')



@app.route('/', methods=['POST', 'GET'])
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

if __name__ == '__main__':
    app.run(debug=True)
