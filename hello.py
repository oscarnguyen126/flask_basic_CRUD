from flask import Flask, request
from flask_mysqldb import MySQL
import json


app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456a@'
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)


class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = mysql.connect

    def query_all(self, sql_string):
        cursor = self.connection.cursor()
        cursor.execute(sql_string)
        return cursor.fetchall()


    def interact(self, sql_string, data):
        cursor = self.connection.cursor()
        cursor.execute(sql_string, data)
        mysql.connection.commit()


db = Database()
with app.app_context():
    db.connect()


@app.route('/list', methods=['GET'])
def list_items():
    results = db.query_all('''select * from items''')
    results_json = json.dumps(results)
    return results_json


@app.route('/create', methods=['POST'])
def create_items():
    data = request.json
    db.interact('''insert into items (name, price) values (%s, %s)''', (data['name'], data['price']))
    return {'msg':'data created succesfully'}


@app.route('/update', methods=['PUT'])
def update_items():
    data = request.json
    db.interact('''update items set name = %s, price = %s where id = %s''', (data['name'], data['price'], data['id']))
    return {'msg':'data updated'}


@app.route('/delete', methods=['DELETE'])
def delete_items():
    data = request.json
    db.interact('''delete from items where id = %s''', (data['id'],))
    return {'msg': 'item deleted'}
