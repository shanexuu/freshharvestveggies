import os
from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from models import db 
from models.Item import Item 
from models.Veggie import Veggie 
from models.PremadeBox import PremadeBox
from models.PackVeggie import PackVeggie 
from models.WeightedVeggie import WeightedVeggie
from models.UnitPriceVeggie import UnitPriceVeggie
from models.Person import Person
from sqlalchemy.orm import sessionmaker
from models.Staff import Staff
from models.Customer import Customer
from models.CorporateCustomer import CorporateCustomer
from models.Order import Order
from models.OrderLine import OrderLine
import json



basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.secret_key = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password/fresh_harvest_veggies_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route("/")
def index():

    name = session.get('firstName')
    veggie = Veggie.query.all()
    if isinstance(veggie, WeightedVeggie):
        price = veggie.price  # price per kilo
    elif isinstance(veggie, PackVeggie):
        price = veggie.price   # price per pack
      
    elif isinstance(veggie, UnitPriceVeggie):
        price = veggie.price  # price per pack  
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

    premadeboxes = PremadeBox.query.all()
   
    return render_template('premadebox.html', name=name, premadeboxes=premadeboxes)


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
                return redirect(url_for('login'))  

        else:
            msg = "Invalid username or password."
            
    return render_template('login.html',msg =msg)
          

@app.route('/shop/<int:id>/', methods=['GET', 'POST'])
def item(id):

    name = session.get('firstName')
    # Fetch the veggie by id
    veggie = Veggie.query.get_or_404(id)
    print(veggie)

    if veggie is None:
        return "Veggie not found", 404

    # Check the type of veggie and get the relevant price
    if isinstance(veggie, WeightedVeggie):
        price = veggie.price  # price per kilo
        unit = veggie.unit
        perUnit = veggie.weightUnit
    elif isinstance(veggie, PackVeggie):
        price = veggie.price  # price per pack
        unit = veggie.unit
        perUnit = veggie.pack

    elif isinstance(veggie, UnitPriceVeggie):
        price = veggie.price  # price per pack
        unit = veggie.unit
        perUnit = veggie.vegUnit

    else:
        price = None
        unit = ""
        perUnit= None


    return render_template('item-details.html', veggie=veggie, price=price, unit=unit, perUnit=perUnit, name=name)

@app.route('/premadebox/<int:id>/', methods=['GET', 'POST'])
def premabox_details(id):

    name = session.get('firstName')
    # Fetch the veggie by id
    premadebox = PremadeBox.query.get_or_404(id)

    return render_template('premadebox-details.html', premadebox=premadebox, name=name)


@app.route("/cart")
def cart():
    name = session.get('firstName')
    cart = session.get('cart', {})
    
    # Calculate subtotal
    subtotal = sum(item['price'] * item['quantity'] for item in cart.values())

    return render_template('cart.html', name=name, cart=cart, subtotal=subtotal)



@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():

    user_id = session.get('id')
    item_id = str(request.form.get('item_id'))
    item_quantity = int(request.form.get('quantity', 1))


    if 'loggedin' in session:
        current_user = Person.query.get(user_id)
        item = Item.query.get(item_id)
        if not current_user:
           flash("User not found.", "error")
            
        if not item:
          flash("Item not found.", "error")
          return redirect(url_for('cart'))
        try:
           current_user.add_to_cart(item, item_quantity)
            
        except Exception as e:
            flash(f"Error adding item to cart: {e}", "error")


        print(f"Item ID: {item_id}, Item Quantity: {item_quantity}, User ID: {user_id}")
        print(f"Current User: {current_user}")
        print(f"Item: {item}")
        return redirect(url_for('cart'))
        

       
    else:
        return redirect(url_for('login'))


@app.route('/order/<int:id>/', methods=['GET', 'POST'])
def order_details(id):

    name = session.get('firstName')

    if 'loggedin' in session:
      order_details = Order.get_order_details(id)

      user_type = session.get('type') 
      if user_type == 'staff':
          return render_template('staff-order_details.html', name=name, order_details=order_details)
      if user_type == 'customer':
          return render_template('customer-order_details.html', name=name, order_details=order_details)
      if user_type == 'corporatecustomer':
          return render_template('corporate-order_details.html', name=name, order_details=order_details)
      
    return redirect(url_for('index')) 

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'loggedin' not in session:
        return redirect(url_for('index'))  # Redirect if not logged in

    name = session.get('firstName')
    user_type = session.get('type')
    is_staff = user_type == 'staff'  # Boolean to indicate if the user is staff

    cart = session.get('cart', {})
    subtotal = sum(item['price'] * item['quantity'] for item in cart.values())

    # Retrieve customer list if the user is a staff member
    customers = Customer.query.all() if is_staff else None

    # Handle POST request for processing the checkout
    if request.method == 'POST':
        # For staff, fetch selected customer and delivery method
        if is_staff:
            customer_id = request.form.get('customer_id')
            delivery_method = request.form.get('deliveryMethod')
            customer = Customer.query.get(customer_id)
            if not customer:
                flash("Please select a valid customer.")
                return redirect(url_for('checkout'))
            
            # Create the order (assuming `create_order` handles staff orders without payment)
            staff_id = session.get('id')
            staff_member = Staff.query.get(staff_id)
            order_id = staff_member.create_order(customer_id, cart, delivery_method)
            session.pop('cart', None)
            return redirect(url_for('confirmation', order_id=order_id))
        
        # For regular customers, handle as usual
        customer_id = session.get('id')
        customer = Customer.query.get(customer_id)
        if customer is None:
            flash("Customer not found. Please log in again.")
            return redirect(url_for('index'))

        delivery_method = request.form.get('deliveryMethod')
        payment_method = request.form.get('paymentMethod')
        payment_details = {
            'nameOnCard': request.form.get('nameOnCard'),
            'cardNumber': request.form.get('cardNumber'),
            'expiration': request.form.get('expiration'),
            'cvv': request.form.get('cvv')
        }

        try:
            order_summary = customer.checkout(cart, delivery_method, payment_method, payment_details)
            session.pop('cart', None)
            return redirect(url_for('confirmation', order_id=order_summary['id']))
        except ValueError as e:
            flash(str(e))
            return render_template('checkout.html', name=name, cart=cart, subtotal=subtotal, customers=customers, is_staff=is_staff)

    # If GET request, render the checkout page
    return render_template('checkout.html', name=name, cart=cart, subtotal=subtotal, customers=customers, is_staff=is_staff)




@app.route('/confirmation/<int:order_id>')
def confirmation(order_id):
    
    # Fetch the order details using the order_id
    order = Order.query.get(order_id)

    if not order:
        flash("Order not found.")
        return redirect(url_for('index'))

    return render_template('order_confirmation.html', order=order)

@app.route("/dashboard")
def dashboard():

    name = session.get('firstName')
    user_id = session.get('id')

    user = db.session.query(Customer).get(user_id)
    staff = db.session.query(Staff).get(user_id)

    if 'loggedin' in session:
      user_type = session.get('type') 
      if user_type == 'staff':
          all_orders = staff.view_all_orders()
          return render_template('staff-dashboard.html', name=name, all_orders = all_orders)
      if user_type == 'customer':
          order_history = Order.display_orders(user)
          return render_template('customer-dashboard.html', name=name, order_history = order_history)
      if user_type == 'corporatecustomer':
          order_history = Order.display_orders(user)
          return render_template('corporate-dashboard.html', name=name, order_history = order_history)
      
    return redirect(url_for('index'))      


@app.route("/make_payment/<int:order_id>", methods=["GET", "POST"])
def make_payment(order_id):
    

    customer_id = session.get('id')
    customer = Customer.query.get(customer_id)
    corporate = CorporateCustomer.query.get(customer_id)
    user_type = session.get('type') 

    # Handle POST request to process the payment
    if request.method == "POST":
        payment_method = request.form.get('paymentMethod')

        # Calculate the payment amount based on the order's order lines
        order_lines = OrderLine.query.filter_by(order_id=order_id).all()
        payment_amount = sum(line.item.get_price * line.quantity for line in order_lines)  # Use get_price to access price

        # Collect additional payment details if necessary
        payment_details = {}
        if payment_method in ["credit", "debit"]:
            payment_details['nameOnCard'] = request.form.get('nameOnCard')
            payment_details['cardNumber'] = request.form.get('cardNumber')
            payment_details['expiration'] = request.form.get('expiration')
            payment_details['cvv'] = request.form.get('cvv')

        try:

            if user_type == 'customer':
                payment_successful = customer.payment(order_id, payment_method, payment_details)
                if payment_successful:
                    flash("Payment successful! Thank you.")
                else:
                    flash("Payment failed. Please try again.")
            elif user_type == 'corporatecustomer':
                payment_successful = corporate.payment(order_id, payment_method, payment_details)
                if payment_successful:
                    flash("Payment successful! Thank you.")
                else:
                    flash("Payment failed. Please try again.")
        except ValueError as e:
            flash(str(e))

        return redirect(url_for('dashboard'))

    # Handle GET request to render the payment page
    return render_template('payment.html', order_id=order_id)





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
 
@app.route("/cancel-order/<int:order_id>", methods=["POST"])
def cancel_order(order_id):

    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    user_id = session.get('id')
    customer = Customer.query.get(user_id)

    if not customer:
        flash("Customer not found.", "error")
        return redirect(url_for('login'))
    try:
        message = customer.cancel_order(order_id)
        flash(message, "success" if "successfully" in message else "error")
        return redirect(url_for('dashboard')) 
     
    except Exception as e:
        return (f"An error occurred: {e}")
    

@app.route("/staff/orders")
def staff_orders():

    if 'loggedin' in session:

      user_type = session.get('type')
      name = session.get('firstName')
      if user_type == 'staff':
          
        return render_template('staff-orders.html',name=name)
        
      else:
        return redirect(url_for('login'))
      
    else:
        return redirect(url_for('login'))

@app.route('/fulfill-order/<int:order_id>', methods=["POST"])
def fulfill_order(order_id):
    if 'loggedin' in session and session.get('type') == 'staff':
        user_id = session.get('id')
        staff = Staff.query.get(user_id)

        if not staff:
            flash("Staff member not found!", "error")
            return redirect(url_for('login'))
    
        try:

          # Fulfill the order
          message = staff.fulfill_order(order_id)
          flash(message, "success" if "fulfilled" in message else "error")

        except Exception as e:
          return (f"An error occurred: {e}")

        # Redirect back to the orders page
        return redirect(url_for('dashboard'))
    
    else: 
      return redirect(url_for('login'))
    
    
@app.route("/staff/products")
def staff_products():
    user_type = session.get('type')
    name = session.get('firstName')
    user_id = session.get('id')

    if 'loggedin' in session and user_type == 'staff':

      staff = db.session.query(Staff).get(user_id)
      veggies = staff.list_products()
          
      return render_template('staff-products.html',name=name, veggies= veggies)
    else:
        return redirect(url_for('login'))

@app.route("/staff/premade-box")
def staff_premadebox():

    user_type = session.get('type')
    name = session.get('firstName')
    user_id = session.get('id')

    if 'loggedin' in session and user_type == 'staff':

        staff = db.session.query(Staff).get(user_id)
        premadeboxes = staff.list_premade_boxes()
          
        return render_template('staff-premadebox.html',name=name, premadeboxes=premadeboxes)
        
    else:
        return redirect(url_for('login'))
      
    
@app.route("/staff/customers")
def staff_customers():

    if 'loggedin' in session:

      user_type = session.get('type')
      name = session.get('firstName')
      user_id = session.get('id')
      if user_type == 'staff':

        staff = Staff.query.get(user_id)
        customers = staff.list_customers()
          
        return render_template('staff-customers.html',name=name, customers=customers)
        
      else:
        return redirect(url_for('login'))
      
    else:
        return redirect(url_for('login'))
    
@app.route('/staff/customers/<int:customer_id>')
def staff_view_customer(customer_id):

    user_type = session.get('type')
    name = session.get('firstName')
    # Ensure the user is logged in and is a staff member
    if 'loggedin' in session and user_type == 'staff':
        # Get the staff member from session user ID
        staff_id = session.get('id')
        staff = Staff.query.get(staff_id)

        customer= staff.display_customer_details(customer_id)
        
        return render_template('staff-customer_details.html', customer=customer, name=name)
    
    else:
       return redirect(url_for('login'))  
   
   
    
@app.route("/staff/reports")
def staff_reports():

    user_type = session.get('type')
    name = session.get('firstName')
    # Ensure the user is logged in and is a staff member
    if 'loggedin' in session and user_type == 'staff':

        # Get the staff member from session user ID
        staff_id = session.get('id')
        staff = Staff.query.get(staff_id)

        reports= staff.sales_report()
        popularity_items = staff.get_popularity_items()
          
        return render_template('staff-reports.html',name=name, reports=reports,popularity_items=popularity_items)
        
    else:
        return redirect(url_for('login'))
      

    


@app.route("/logout")
def logout():
    session.pop('firstName', None)
    session.pop('loggedin', None)
    session.pop('type', None)
    session.pop('id', None)
    session.pop('cart', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
