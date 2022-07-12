from flask import Flask, request,redirect
import sqlite3
from settings import DB_PATH
from typing import Optional

app = Flask(__name__)


class Connection:
    def __init__(self):
        self._connection: Optional[sqlite3.Connection] = None

    def __enter__(self):
        self._connection = sqlite3.connect(DB_PATH)
        self._connection.row_factory = sqlite3.Row
        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()


@app.route('/')
def hello():
    return 'My homework'


@app.route('/phones/create/')
def create():
    with Connection() as connect:
        curs = connect.cursor()
        curs.execute("""CREATE TABLE IF NOT EXISTS users_phone (
                        phoneID INTEGER,
                        contactName VARCHAR,
                        phoneValue VARCHAR)""")

        name = request.form.get('contactName')
        phone = request.form.get('phoneValue')

        if name != None and phone != None:
            curs.execute("""INSERT INTO users_phone(contactName, phoneValue) VALUES (?,?)""", (name, phone))
            connect.commit()
    return 'ok'


@app.route('/phones/read/')
def read__phones():
    with Connection() as connect:
        user_phone = connect.execute('SELECT * FROM users_phone;').fetchall()
    return '<br>'.join([f'{phone["phoneID"]}: {phone["contactName"]} - {phone["phoneValue"]}' for phone in user_phone])


@app.route('/phones/update/',methods=['POST', 'GET'])
def update():
    with Connection() as connect:
        curs = connect.cursor()

        if request.method == 'POST':
            oldname = request.form.get('oldname')
            print(oldname)
            values = [oldname]
            query = """SELECT * FROM hw8 WHERE contactName = ?"""
            curs.execute(query, values)
            res = curs.fetchall()
            print(res)
            if res:
                return redirect(f"/phones/update/{oldname}")
            return 'Successfully upgraded'


@app.route('/phones/delete/<int:phoneID>')
def delete(phoneID):
    with Connection() as connect:
        with connect:
            connect.execute(
                'DELETE FROM users_phone WHERE (phoneID=:phoneID);',
                {'phoneID': phoneID}
            )
    return 'Delete phone'


if __name__ == '__main__':
    app.run(debug=True, port=2000)
