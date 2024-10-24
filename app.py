import os
from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from models import db 
from models.Item import Item 
from models.Veggie import Veggie 

from models.PackVeggie import PackVeggie 
from models.WeightedVeggie import WeightedVeggie
from models.UnitPriceVeggie import UnitPriceVeggie
from models.Person import Person
from sqlalchemy.orm import sessionmaker
from models.Staff import Staff
from models.Customer import Customer
from models.CorporateCustomer import CorporateCustomer


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.secret_key = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:wsXY6205506@localhost:3306/fresh_harvest_veggies_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)




@app.route("/")
def index():

    name = session.get('firstName')
    veggie = Veggie.query.all()
    if isinstance(veggie, WeightedVeggie):
        price = veggie.pricePerWeight  # price per kilo
    elif isinstance(veggie, PackVeggie):
        price = veggie.pricePerPack  # price per pack
      
    elif isinstance(veggie, UnitPriceVeggie):
        price = veggie.pricePerUnit  # price per pack  
    else:
        price = None
       
    return render_template('index.html', veggie=veggie, name=name, price=price)

@app.route("/shop")
def shop():
    name = session.get('firstName')

    veggie = Veggie.query.all()
   
    return render_template('shop.html', veggie=veggie,name=name)

@app.route("/premadebox")
def premadeBox():
    name = session.get('firstName')
   
    return render_template('premadebox.html', name=name)



@app.route("/login", methods=['GET', 'POST'])
def login():
    msg = ''

    if 'loggedin' in session:
        return redirect(url_for('dashboard'))

    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Query the Person table (polymorphic will resolve the subclass)
        person = Person.query.filter_by(username=username).first()

        if person and person.check_password(password):
            # Store user information in session
            session['loggedin'] = True
            session['firstName'] = person.firstName
            session['type'] = person.type 
            session['id'] = person.id

            if person.type == 'staff':
                return redirect(url_for('dashboard'))
            elif person.type == 'customer':
                if hasattr(person, 'cusType') and person.cusType == 'corporatecustomer':
                    session['type'] = person.cusType
                    print(f"User type: {person.cusType}")
                    return redirect(url_for('dashboard'))
                else:
                    print(f"User type: {person.cusType}")
                    return redirect(url_for('dashboard')) 
                    
            else:
                return redirect(url_for('index'))  

        else:
            msg = "Invalid username or password."
            
    return render_template('login.html',msg =msg)
          

@app.route('/shop/<int:id>/', methods=['GET', 'POST'])
def item(id):

    name = session.get('firstName')
    # Fetch the veggie by id
    veggie = Veggie.query.get_or_404(id)

    if veggie is None:
        return "Veggie not found", 404

    # Check the type of veggie and get the relevant price
    if isinstance(veggie, WeightedVeggie):
        price = veggie.pricePerWeight  # price per kilo
        unit = veggie.unit
        perUnit = veggie.weightUnit
    elif isinstance(veggie, PackVeggie):
        price = veggie.pricePerPack  # price per pack
        unit = veggie.unit
        perUnit = veggie.pack

    elif isinstance(veggie, UnitPriceVeggie):
        price = veggie.pricePerUnit  # price per pack
        unit = veggie.unit
        perUnit = veggie.vegUnit

    else:
        price = None
        unit = ""
        perUnit= None


    return render_template('item-details.html', veggie=veggie, price=price, unit=unit, perUnit=perUnit, name=name)

@app.route("/cart")
def cart():
    name = session.get('firstName')
    return render_template('cart.html', name=name)

@app.route("/dashboard")
def dashboard():

    name = session.get('firstName')

    if 'loggedin' in session:
      user_type = session.get('type') 
      if user_type == 'staff':
          return render_template('staff-dashboard.html', name=name)
      if user_type == 'customer':
          return render_template('customer-dashboard.html', name=name)
      if user_type == 'corporatecustomer':
          return render_template('corporate-dashboard.html', name=name)
      
    return redirect(url_for('index'))      





@app.route("/profile")
def profile():
  
  user_type = session.get('type')
  user_id = session.get('id')
  name = session.get('firstName')
  if user_type == 'customer':
    customer = Customer.query.get(user_id)
    profile = customer.display_profile()
    return render_template('customer-profile.html', profile=profile, name=name)
  elif user_type == 'corporatecustomer':
     corporate_customer = CorporateCustomer.query.get(user_id)
     profile_data = corporate_customer.display_profile()
     return render_template('corporate-profile.html', profile=profile_data, name=name)

  elif user_type == 'staff':
    staff = Staff.query.get(user_id)
    profile_data = staff.display_profile()
    return render_template('staff-profile.html', profile=profile_data, name=name)
        
  else:
    return redirect(url_for('index'))
 


@app.route("/logout")
def logout():
    session.pop('firstName', None)
    session.pop('loggedin', None)
    session.pop('type', None)
    session.pop('id', None)
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)