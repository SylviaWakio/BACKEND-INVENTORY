from flask import Flask, request, jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api, Resource
from models import db, Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

class Products(Resource):
    def get(self):
        products_dict_list = [d.to_dict() for d in Product.query.all()]
        response = make_response(
            jsonify(products_dict_list),
            200,
        )
        return response

    def post(self):
        products = []
        for data in request.json:
            name = data['product_name']
            quantity = data['product_quantity']
            price = data['product_price']

            new_product = Product(
                product_name=name,
                product_quantity=quantity,
                product_price=price,
            )

            db.session.add(new_product)
            products.append(new_product)

        db.session.commit()

        products_dicts = [products.to_dict() for product in products]

        response = make_response(
            jsonify(products_dicts),
            201
        )

        return response

api.add_resource(Products, '/products')

if __name__ == "__main__":
    app.run(debug=True)
