from flask import Flask, request, abort
from datetime import datetime
import time
import sqlite3

app = Flask('__name__')

# db = [
#     {
#         'text': 'hello',
#         'name': 'J',
#         'time': 0.1
#     },
#     {
#         'text': 'hello, J',
#         'name': 'N',
#         'time': 0.2
#     },
# ]
# connect db and create table
with sqlite3.connect('server.db') as db:
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
            text text,
            name text,
            time BLOB
            )""")
    db_tuple = cur.execute("SELECT * FROM users").fetchall()
    db_dict = [dict(zip([c[0] for c in cur.description], i)) for i in db_tuple]
    db.commit()


@app.route('/')
def hello():
    return "Hello people <a href='/status'>Status </a>  <a href='/messages'>Messages </a>"

@app.route('/status')
def status():
    return {
        'status': True,
        'name': 'Messanger',
        'time0': time.time(),
        'time1': time.asctime(),
        'time2': datetime.now(),
        'time3': datetime.now().strftime('%H:%M:%S'),
        'messages': len(db_dict)
    }

@app.route('/send', methods = ['POST'])
def send_message():
    data = request.json

    # check data is dict with text & name
    if not isinstance(data, dict):
        return abort(400)

    if 'text' not in data or 'name' not in data:
        return abort(400)

    text = data['text'].strip()
    name = data['name'].strip()



    # check text & name are valid string
    if not isinstance(text, str) or not isinstance(name, str):
        return abort(400)
    if len(text) == 0 or len(name) == 0:
        return abort(400)
    if len(text) > 1000 or len(name) > 100:
        return abort(400)

    message = {
        'text': text,
        'name': name,
        'time': time.time()
    }

    # connect db and add message
    with sqlite3.connect('server.db') as db:
        cur = db.cursor()
        cur.execute("INSERT INTO users VALUES (:text, :name, :time)", message)
        db.commit()

    # db.append(message)

    if text == '/weather':
        pogoda = ({
            'text': 'Погода хорошая',
            'name': 'bot',
            'time': time.time()})
        cur.execute("INSERT INTO users VALUES (:text, :name, :time)", pogoda)
        db.commit()

    return {'ok': True}

@app.route("/messages")
def get_messages():
    try:
        after = float(request.args['after'])
    except:
        return abort(400)

    # connect
    with sqlite3.connect('server.db') as db:
        cur = db.cursor()
        db_tuple = cur.execute("SELECT * FROM users").fetchall()
        db_dict = [dict(zip([c[0] for c in cur.description], i)) for i in db_tuple]
        db.commit()

    result = []
    for message in db_dict:
        if message['time'] > after:
            result.append(message)

    return {"messages": result[:100]}

app.run()