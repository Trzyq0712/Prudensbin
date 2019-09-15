# from app import app
from flask import Flask, redirect, url_for, request, render_template, current_app, g, escape
from flask.cli import with_appcontext
import sqlite3

app = Flask(__name__)
db = sqlite3.connect('base.db', check_same_thread=False)

def db_fetch(bin_id):
    cursor = db.cursor()    
    cursor.execute('SELECT * FROM bins WHERE id = ?;', (bin_id,))
    res = cursor.fetchall()
    assert(len(res) > 0)
    return res[0]

#@app.route('/style.css')
#def static_style():
#    return app.send_static_file('style.css')

#@app.route('/script.js')
#def static_script():
#    return app.send_static_file('script.js')

@app.route('/', methods = ['POST', 'GET'])
@app.route('/index', methods = ['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/create', methods = ['POST', 'GET'])
def create():
    args = request.args if request.method == 'GET' else request.form
    try:
        lat, lng = float(args.get('lat')), float(args.get('lng'))
        assert(-180 <= lng <= 180)
        assert(-90 <= lat <= 90)
        cursor = db.cursor()    
        cursor.execute('INSERT INTO bins(lat, lng, bintype, rating_sum, rating_count) VALUES(?,?,?,?,?)', (lat, lng, '', 0, 0))
        db.commit()
    except:
        return {'ok' : False}
    print('#', cursor.lastrowid)
    return {'ok' : True, 'id' : cursor.lastrowid}

@app.route('/update', methods = ['POST', 'GET'])
def update():
    args = request.args if request.method == 'GET' else request.form
    try:
        bin_id = int(args.get('bin_id'))
        row = list(db_fetch(bin_id))
        if args.get('rating'):
            rating = float(args.get('rating'))
            assert(0 <= rating <= 5)
            row[4] += rating
            row[5] += 1
        if args.get('bintype'):
            bintype = ''.join(list({i for i in args.get('bintype') if i in 'BELMPST'}))
            if bintype != '':
                row[3] = bintype
        cursor = db.cursor()    
        cursor.execute('UPDATE bins SET bintype = ?, rating_count = ?, rating_sum = ? WHERE id = ?', (row[3], row[5], row[4], bin_id))
        db.commit()
    except:
        return {'ok' : False}
    return {'ok' : True, 'id' : cursor.lastrowid}

@app.route('/fetch', methods = ['POST', 'GET'])
def fetch():
    args = request.args if request.method == 'GET' else request.form
    try:
        return {'ok' : True, 'row' : db_fetch(int(args.get('bin_id')))}
    except:
        return {'ok' : False}
    return {'ok' : False} # This state should be unreachable

@app.route('/nearby', methods = ['POST', 'GET'])
def nearby():
    args = request.args if request.method == 'GET' else request.form
    try:
        lat, lng = float(args.get('lat')), float(args.get('lng'))
        assert(-180 <= lng <= 180)
        assert(-90 <= lat <= 90)
        cursor = db.cursor()    
        cursor.execute('SELECT * FROM bins WHERE lat < ? AND lat > ? AND lng < ? AND lng > ?',
            (lat + .1, lat - .1, lng + .1, lng - .1))
        res = cursor.fetchall()
        db.commit()
        return {'ok' : True, 'rows' : res}
    except:
        return {'ok' : False}
    return {'ok' : False} # This state should be unreachable

@app.route('/reviews', methods = ['POST', 'GET'])
def reviews():
    args = request.args if request.method == 'GET' else request.form
    try:
        bin_id = int(args.get('bin_id'))
        cursor = db.cursor()
        cursor.execute('SELECT * FROM reviews WHERE bin = ?;', (bin_id,))
        res = cursor.fetchall()
        db.commit()
        return {'ok' : True, 'rows' : res}
    except:
        return {'ok' : False}
    return {'ok' : False} # This state should be unreachable

@app.route('/add_review', methods = ['POST', 'GET'])
def add_review():
    args = request.args if request.method == 'GET' else request.form
    try:
        print('$', args)
        bin_id = int(args.get('bin_id'))
        print(bin_id)
        content = args.get('content')
        print(bin_id, content)
        cursor = db.cursor()    
        cursor.execute('INSERT INTO reviews(bin, content) VALUES(?,?)', (bin_id, escape(content)))
        db.commit()
    except:
        return {'ok' : False}
    return {'ok' : True}

@app.route('/add_pic', methods = ['POST', 'GET'])
def add_pic():#TODO
    args = request.args if request.method == 'GET' else request.form
    try:
        bin_id = int(args.get('bin_id'))
        content = args.get('content')
        cursor = db.cursor()    
        cursor.execute('INSERT INTO reviews(bin, content) VALUES(?,?)', (bin_id, escape(content)))
        db.commit()
    except:
        return {'ok' : False}
    return {'ok' : True}