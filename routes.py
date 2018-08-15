from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import request, Response
import json
from models import *
import datetime
from utils import *
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/add_item', methods = ['POST'])
@login_required
def add_item():
    try:
        name = request.form['name']
        brand = request.form['brand']
        category = request.form['category']
        product_code = request.form['product_code']
        item = Item(name, brand, category, product_code)
        db.session.add(item)
        db.session.commit()	   
        return Response('{"message":"Added item"}', status=200, mimetype='application/json') 
        add_update(OPER.ADD, name, current_user, OBJ.ITEM)        
    except:    
        return Response('{"message":"Invalid input"}', status=400, mimetype='application/json')
        
@app.route('/update_item', methods = ['POST'])
@login_required
def update_item():
    try:
        item_id = request.form['id']
        item = Item.query.get_or_404(item_id)
        update_info = {}
        change = False
        if('name' in request.form and request.form['name'] != item.name):
            name = request.form['name']
            update_info["name"] = name
            item.name = name        
            change = True
        if('brand' in request.form and request.form['brand'] != item.brand):
            brand = request.form['brand']
            update_info["brand"] = brand
            item.brand = brand
            change = True
        if('category' in request.form and request.form['category'] != item.category):
            category = request.form['category']
            update_info["category"] = request.form['category']
            item.category = category
            change = True
        if('product_code' in request.form and request.form['product_code'] != item.product_code):
            product_code = request.form['product_code']
            update_info["product_code"] = request.form['product_code']
            item.product_code = product_code
            change = True
        if(not change):    
            return Response('{"message":"No changes"}', status=200, mimetype='application/json') 
        add_update(OPER.MODIFY, update_info, current_user, OBJ.ITEM)    
        db.session.commit()	   
        return Response('{"message":"Updated item"}', status=200, mimetype='application/json')    
    except:    
        return Response('{"message":"Invalid input"}', status=400, mimetype='application/json')        

@app.route('/delete_item', methods = ['POST'])
@login_required
def delete_item():
    try:    
        item_id = request.form['id']
        name = request.form['name']
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()	   
        add_update(OPER.DELETE, name, current_user, OBJ.ITEM)
        return Response('{"message":"Deleted item"}', status=200, mimetype='application/json')        
    except:    
        return Response('{"message":"Invalid input"}', status=400, mimetype='application/json')  

@app.route('/add_variant', methods = ['POST'])
@login_required
def add_variant():
    try:    
        name = request.form['name']
        selling_price = request.form['selling_price']
        cost_price = request.form['cost_price']
        properties = request.form['properties']
        quantity = request.form['quantity']
        item_id = request.form['id']
        var_item = Item.query.get_or_404(item_id)
        email = request.form['email']
        variant = Variant(name=name, selling_price=selling_price, cost_price=cost_price, properties=properties, quantity=quantity, item=var_item)
        db.session.add(variant)
        db.session.commit()	   
        add_update(OPER.ADD, name, current_user, OBJ.VARIANT)
        return Response('{"message":"Added variant"}', status=200, mimetype='application/json')        
    except:    
        return Response('{"message":"Invalid input"}', status=400, mimetype='application/json')        

@app.route('/update_variant', methods = ['POST'])
@login_required
def update_variant():
    try:
        var_id = request.form['id']
        variant = Variant.query.get_or_404(var_id)
        update_info = {}
        change = False
        if('cost_price' in request.form and int(request.form['cost_price']) != variant.cost_price):
            cost_price = request.form['cost_price']
            update_info["cost_price"] = cost_price
            variant.cost_price = cost_price     
            change = True
        if('selling_price' in request.form and int(request.form['selling_price']) != variant.selling_price):
            selling_price = request.form['selling_price']
            update_info["selling_price"] = selling_price
            variant.selling_price = selling_price
            change = True
        if('name' in request.form and request.form['name'] != variant.name):
            name = request.form['name']
            update_info["name"] = request.form['name']
            variant.name = name
            change = True
        if('quantity' in request.form and int(request.form['quantity']) != variant.quantity):
            quantity = request.form['quantity']
            update_info["quantity"] = request.form['quantity']
            variant.quantity = quantity
            change = True 
        if('properties' in request.form and request.form['properties'] != variant.properties):
            properties = json.loads(request.form['properties'])
            current_properties = json.loads(variant.properties)
            for key in properties:
                if(key not in current_properties or current_properties[key] != properties[key]):
                    update_info[key] = properties[key]
                    current_properties[key] = properties[key]
                    change = True
            variant.properties = json.dumps(current_properties)    
        if(not change):
            return Response('{"message":"No changes"}', status=200, mimetype='application/json')  
        add_update(OPER.MODIFY, update_info, current_user, OBJ.VARIANT)    
        db.session.commit()	   
        return Response('{"message":"Updated item"}', status=200, mimetype='application/json')    
    except:    
        return Response('{"message":"Invalid input"}', status=400, mimetype='application/json')    
        
@app.route('/delete_variant', methods = ['POST'])
@login_required
def delete_variant():
    try:    
        var_id = request.form['id']
        name = request.form['name']
        variant = Variant.query.get_or_404(var_id)
        db.session.delete(variant)
        db.session.commit()	   
        add_update(OPER.DELETE, name, current_user, OBJ.VARIANT)
        return Response('{"message":"Deleted variant"}', status=200, mimetype='application/json')        
    except:    
        return Response('{"message":"Invalid input"}', status=400, mimetype='application/json')
        
@app.route('/remove_property', methods = ['POST'])
@login_required
def remove_property():
    try:    
        var_id = request.form['id']
        name = request.form['name']
        variant = Variant.query.get_or_404(var_id)
        curr_properties = json.loads(variant.properties)
        if(name not in curr_properties):
            return Response('{"message":"Invalid input"}', status=400, mimetype='application/json')  
        curr_properties.pop(name)
        variant.properties = json.dumps(curr_properties)
        db.session.commit()	   
        add_update(OPER.MODIFY, name, current_user, OBJ.VARIANT)        
        return Response('{"message":"Removed property"}', status=200, mimetype='application/json')        
    except:    
        return Response('{"message":"Invalid input"}', status=400, mimetype='application/json')        
	   
@app.route('/get_items', methods = ['GET'])
@login_required
def get_items():
    itList = []
    for it in Item.query.all():
        itDict = {
            'id': it.id,
            'name': it.name,
            'brand': it.brand,
            'category': it.category,
            'product_code': it.product_code}
        itList.append(itDict)
    return Response(json.dumps(itList), status=200, mimetype='application/json')

@app.route('/get_variants', methods = ['GET'])
@login_required
def get_variants():    
    varList = []
    for var in Variant.query.all():
        varDict = {
            'id': var.id,
            'name': var.name,
            'selling_price': var.selling_price,
            'cost_price': var.cost_price,
            'properties' : var.properties,			
            'quantity': var.quantity}
        varList.append(varDict)
    return Response(json.dumps(varList), status=200, mimetype='application/json')
    
@app.route('/get_updates', methods = ['GET'])
@login_required
def get_updates():    
    updateList = []
    user_id = request.args.get('user_id')
    if(user_id == None):
        data_update = Data_Update.query.all()
    else:
        data_update = Data_Update.query.filter_by(user_id=user_id)
    for update in data_update:
        updateDict = {
            'update': update.update,
            'user' : update.updater.name}
        updateList.append(updateDict)
    return Response(json.dumps(updateList), status=200, mimetype='application/json')    
	
@app.route('/register' , methods = ['POST'])
def register():
    try:
        user = User(request.form['email'] , request.form['password'], request.form['name'])
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return Response('{"message":"User successfully registered"}', status=200, mimetype='application/json') 
    except:
        return Response('{"message":"Invalid input"}', status=400, mimetype='application/json')        

@app.route('/login',methods=['POST'])
def login():
    try:    
        email = request.form['email']
        password = request.form['password']
        registered_user = User.query.filter_by(email=email,password=password).first()
        if registered_user is None:
            return Response('{"message":"Invalid user"}', status=401, mimetype='application/json') 
        login_user(registered_user)
        return Response('{"message":"Logged in successfully"}', status=200, mimetype='application/json') 
    except:
        return Response('{"message":"Invalid input"}', status=400, mimetype='application/json')         
        
@app.route('/logout')
@login_required
def logout():
    logout_user()    
    return Response('{"message":"Logged out successfully"}', status=200, mimetype='application/json')
    
@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()