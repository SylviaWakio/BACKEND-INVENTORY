from random import choice

from faker import Faker

from app import app,db
from models import Transaction


from models import Product


fake = Faker()

with app.app_context():


    Transaction.query.delete()
  
    Product.query.delete()

    db.session.add
    db.session.commit()

