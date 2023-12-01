import subprocess
from datetime import datetime
import pandas as pd
from flask import Flask
from flask_restful import reqparse, Api, Resource

app = Flask(__name__)
api = Api(app)


def check_csvs():
    try:
        pd.read_csv('csvs/clients.csv')
    except FileNotFoundError:
        df = pd.DataFrame({'name': [], })
        df.to_csv('csvs/clients.csv', index=False)

    try:
        pd.read_csv('csvs/products.csv')
    except FileNotFoundError:
        df = pd.DataFrame({'code': [],
                           'name': [],
                           'description': [],
                           'quantity': [],
                           'price': [],
                           'min_stock': [],
                           'date': [],
                           'hour': []})
        df.to_csv('csvs/products.csv', index=False)

    try:
        pd.read_csv('csvs/stock_control.csv')
    except FileNotFoundError:
        df = pd.DataFrame({'code': [],
                           'quantity': [],
                           'date': [],
                           'hour': []})
        df.to_csv('csvs/stock_control.csv', index=False)


check_csvs()

subprocess.Popen(['python', 'sse.py'], shell=True)


class Rest:
    logged_on_clients = {}

    name = 'henrique'
    clients = pd.read_csv('csvs/clients.csv')
    products = pd.read_csv('csvs/products.csv')
    stock_control = pd.read_csv('csvs/stock_control.csv')

    class TodoList(Resource):
        def get(self):
            print(Rest.name)
            Rest.name = 'caio'
            print(Rest.name)
            return "Hello World!"

    class RegisterClient(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='Your name', required=True)
            args = parser.parse_args()

            df = pd.DataFrame({'name': [args['name']]})
            df.to_csv('csvs/clients.csv', mode='a', header=False, index=False)
            print('Client registered successfully')

            Rest.clients = pd.read_csv('csvs/clients.csv')

            return 'Client registered successfully'

    class RegisterProduct(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('code', type=int, help='Product code', required=True)
            parser.add_argument('name', type=str, help='Product name', required=True)
            parser.add_argument('description', type=str, help='Product description', required=True)
            parser.add_argument('quantity', type=int, help='Product quantity', required=True)
            parser.add_argument('price', type=int, help='Product price', required=True)
            parser.add_argument('min_stock', type=int, help='Product min stock', required=True)
            args = parser.parse_args()

            if args['code'] in Rest.products['code'].values:
                print('Product already registered')
                return

            df = pd.DataFrame({'code': [args['code']],
                               'name': [args['name']],
                               'description': [args['description']],
                               'quantity': [args['quantity']],
                               'price': [args['price']],
                               'min_stock': [args['min_stock']],
                               'date': [datetime.now().strftime("%d/%m/%Y")],
                               'hour': [datetime.now().strftime("%H:%M:%S")]})

            df.to_csv('csvs/products.csv', mode='a', header=False, index=False)
            print('Product registered successfully')

            Rest.products = pd.read_csv('csvs/products.csv')

            Rest.UpdateStockLog(args['code'], args['quantity'], datetime.now().strftime("%d/%m/%Y"),
                                datetime.now().strftime("%H:%M:%S"))

            return 'Product registered successfully'

    class RemoveProduct(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('code', type=int, help='Product code', required=True)
            parser.add_argument('quantity', type=int, help='Product quantity', required=True)
            args = parser.parse_args()

            if args['code'] in Rest.products['code'].values:
                # check if quantity is valid
                if args['quantity'] <= Rest.products.loc[Rest.products['code'] == args['code'], 'quantity'].values[0]:
                    Rest.products.loc[Rest.products['code'] == args['code'], 'quantity'] -= args['quantity']
                    Rest.products.to_csv('csvs/products.csv', index=False)
                    print('Product removed successfully')

                    # update stock.csv with movement (add or remove) and quantity of products
                    Rest.UpdateStockLog(args['code'], args['quantity'] * -1, datetime.now().strftime("%d/%m/%Y"),
                                        datetime.now().strftime("%H:%M:%S"))
                else:
                    print('Invalid quantity')
            else:
                print('Product not found')

    def UpdateStockLog(code, quantity, date, hour):
        df = pd.DataFrame({'code': [code],
                           'quantity': [quantity],
                           'date': [date],
                           'hour': [hour]})
        df.to_csv('csvs/stock_control.csv', mode='a', header=False, index=False)

        Rest.stock_control = pd.read_csv('csvs/stock_control.csv')

        print('Stock log updated successfully')

    class GetProduct(Resource):
        def get(self):
            return Rest.products.loc[Rest.products['quantity'] > 0].to_json()

    class GetStockLog(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('initial_date', type=str, help='Initial date', required=True)
            parser.add_argument('final_date', type=str, help='Final date', required=True)
            args = parser.parse_args()

            Rest.stock_control['date'] = pd.to_datetime(Rest.stock_control['date'], format="%d/%m/%Y")

            initial_date = datetime.strptime(args['initial_date'], '%d/%m/%Y')
            final_date = datetime.strptime(args['final_date'], '%d/%m/%Y')

            return Rest.stock_control.loc[(Rest.stock_control['date'] >= initial_date) &
                                          (Rest.stock_control['date'] <= final_date)].to_string(index=False)

    class GetProductsWithoutMovement(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('initial_date', type=str, help='Initial date', required=True)
            parser.add_argument('final_date', type=str, help='Final date', required=True)
            args = parser.parse_args()

            Rest.stock_control['date'] = pd.to_datetime(Rest.stock_control['date'], format="%d/%m/%Y")

            initial_date = datetime.strptime(args['initial_date'], '%d/%m/%Y')
            final_date = datetime.strptime(args['final_date'], '%d/%m/%Y')

            # products_without_movement = self.products.loc[~self.products['code'].isin( self.stock.loc[(self.stock[
            # 'date'] >= initial_date) & (self.stock['date'] <= final_date)]['code'])]
            products_without_movement = Rest.products.loc[~Rest.products['code'].isin(
                Rest.stock_control.loc[(Rest.stock_control['date'] >= initial_date) &
                                       (Rest.stock_control['date'] <= final_date)]['code'])]

            return products_without_movement.to_string(index=False)


attributes = Rest.__dict__

for attribute in attributes:
    if isinstance(attributes[attribute], type):
        api.add_resource(attributes[attribute], f'/{attribute}')

if __name__ == '__main__':
    check_csvs()
    app.run(debug=False)
