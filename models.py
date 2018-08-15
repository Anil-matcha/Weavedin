from flask_login import UserMixin
from run import app, db
import datetime

class Item(db.Model):
    id = db.Column('item_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    brand = db.Column(db.String(100))  
    category = db.Column(db.String(100))
    product_code = db.Column(db.String(100))
    variants = db.relationship("Variant", backref="item", cascade="all,delete", lazy = "dynamic")
    	
    def __init__(self, name, brand, category, product_code):
       self.name = name
       self.brand = brand
       self.category = category
       self.product_code = product_code
	   
class Variant(db.Model):
    id = db.Column('variant_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    selling_price = db.Column(db.Integer)
    cost_price = db.Column(db.Integer)
    properties = db.Column(db.Text)
    quantity = db.Column(db.Integer)   
    item_id = db.Column("ItemID", db.Integer, db.ForeignKey('item.item_id'), index=True, nullable=True)

class User(UserMixin, db.Model):
    id = db.Column('user_id', db.Integer, primary_key = True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    name = db.Column(db.String(80))
    updates = db.relationship("Data_Update", backref="updater", cascade="all,delete", lazy = "dynamic")
    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name
    def __repr__(self):
        return '<User %r>' % self.email
    def get_id(self):
        return str(self.id)
       
class Data_Update(db.Model):
    id = db.Column('update_id', db.Integer, primary_key = True)    
    update_time = db.Column(db.DateTime(timezone=True), nullable=False)
    update = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
    def __init__(self, update):
        self.update_time = datetime.datetime.now()
        self.update = update