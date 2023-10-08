
from flask import Flask, request, jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api, Resource
from models import db, Transaction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transactions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

class Transactions(Resource):
    def get(self):
        transactions_dict_list = [d.to_dict() for d in Transaction.query.all()]
        response = make_response(
            jsonify(transactions_dict_list),
            200,
        )
        return response

    def post(self):
        transactions = []
        for data in request.json:
            product_name = data['product_name']
            product_quantity = data['product_quantity']
            product_price = data['product_price']

            new_transaction = Transaction(
                product_name=product_name,
                product_quantity=product_quantity,
                product_price=product_price,
            )

            db.session.add(new_transaction)
            transactions.append(new_transaction)

        db.session.commit()

        transaction_dicts = [transaction.to_dict() for transaction in transactions]

        response = make_response(
            jsonify(transaction_dicts),
            201
        )

        return response

api.add_resource(Transactions, '/transactions')

@app.route('/api/post', methods=['POST'])
def receive_post_request():
    # Check if the request contains JSON data
    if request.is_json:
        data = request.get_json()
        # You can access the JSON data as a Python dictionary
        # For example, if the JSON contains a "message" field:
        message = data.get('message', 'No message provided')
        return jsonify({'received_message': message})
    else:
        return jsonify({'error': 'Invalidi JSON data'}), 400

if __name__ == '__main__':
    app.run(debug=True)

