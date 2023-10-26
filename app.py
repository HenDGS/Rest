from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import base64
import threading
import time
from datetime import datetime
import pandas as pd

app = Flask(__name__)
api = Api(app)
logged_on_clients = {}

def check_csvs():
    try:
        pd.read_csv('csvs/clients.csv')
    except FileNotFoundError:
        df = pd.DataFrame({'name': [],
                           'public_key': [],
                           'remote_object_reference': []})
        df.to_csv('csvs/clients.csv', index=False)

    try:
        pd.read_csv('csvs/products.csv')
    except FileNotFoundError:
        df = pd.DataFrame({'code': [],
                           'name': [],
                           'description': [],
                           'quantity': [],
                           'price': [],
                           'stock': [],
                           'date': [],
                           'hour': []})
        df.to_csv('csvs/products.csv', index=False)

    try:
        pd.read_csv('csvs/stock.csv')
    except FileNotFoundError:
        df = pd.DataFrame({'code': [],
                           'quantity': [],
                           'date': [],
                           'hour': []})
        df.to_csv('csvs/stock.csv', index=False)


check_csvs()
stock = pd.read_csv('csvs/stock.csv')
clients = pd.read_csv('csvs/clients.csv')
products = pd.read_csv('csvs/products.csv')


TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}



def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


parser = reqparse.RequestParser()
parser.add_argument('task')


def Todo(Resource):
    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1

        remote_object_reference2 = remote_object_reference
        logged_on_clients[name] = remote_object_reference

        remote_object_reference = str(remote_object_reference)

        print(f'Client {name} registered successfully')

        df = pd.DataFrame({'name': [name],
                           'public_key': [public_key],
                           'remote_object_reference': [remote_object_reference]})

        df.to_csv('csvs/clients.csv', mode='a', header=False, index=False)
        print('Client registered successfully')

        clients = pd.read_csv('csvs/clients.csv')


class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201


api.add_resource(Todo, '/todos/<todo_id>')

if __name__ == '__main__':
    check_csvs()
    app.run(debug=False)
