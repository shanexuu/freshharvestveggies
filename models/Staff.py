from sqlalchemy import Column, String, ForeignKey, Integer, Date
from .Person import Person
from sqlalchemy.orm import relationship
from .Order import Order  
from .OrderLine import OrderLine
from .Customer import Customer
from .CorporateCustomer import CorporateCustomer
from . import db
from sqlalchemy.orm.exc import NoResultFound
from .Item import Item
from .Veggie import Veggie
from .WeightedVeggie import WeightedVeggie
from .PackVeggie import PackVeggie
from .UnitPriceVeggie import UnitPriceVeggie
from .PremadeBox import PremadeBox
from datetime import datetime, timedelta
from sqlalchemy import extract, func




class Staff(Person):
    __tablename__ = 'staff'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    dateJoined = Column(Date)
    deptName = Column(String(50))
    staffID = Column(Integer)
   
    __mapper_args__ = {
        'polymorphic_identity': 'staff',
    }

    def __init__(self, firstName, lastName, password, username,dateJoined, deptName, staffID):
        super().__init__(firstName=firstName, lastName=lastName, password=password, username=username)
        self.dateJoined = dateJoined
        self.deptName = deptName
        self.staffID = staffID
        self.listOfCustomers = []
        self.listOfOrders = []
        self.premadeBoxes =[]
        self.veggies = []
        self.type = 'staff'

        
   
    def display_profile(self):
        """
        Returns the profile data for the staff to be rendered.
        """
        profile_data = {
            'name': f"{self.firstName} {self.lastName}",
            'dateJoined': self.dateJoined,
            'deptName': self.deptName,
            'staffID': self.staffID,
            
        }
        return profile_data
    
    def view_all_orders(self):
        """
        
        Retrieve all customer orders.
        
        Returns:
            list: A list of all orders in the system.
        """
        return db.session.query(Order).all() 
    
    def fulfill_order(self, order_id):
        """
        Mark an order as fulfilled by updating its status.
        
        Args:
            order_id (int): The ID of the order to fulfill.
        
        Returns:
            str: Confirmation message if fulfilled or error message if not found.
        """
        try:
            # Find the order by ID
            order = db.session.query(Order).filter_by(id=order_id).one()
            
            # Check if the order is already fulfilled
            if order.orderStatus == "Processing":
                # Update order status
               order.orderStatus = 'Fulfilled'
               db.session.commit()
               return f"Order {order_id} has been fulfilled."
            
            elif order.orderStatus == "Canceled":
                return f"Order {order_id} has been canceled by the customer."
                
            elif order.orderStatus == "Fulfilled":
                return f"Order {order_id} is already fulfilled."
            else:
                return None
            
        except NoResultFound:
            return f"Order {order_id} not found."
        except Exception as e:
            db.session.rollback()  
            return f"An error occurred while fulfill the order: {e}"
    
    def list_customers(self):
        """
        List all customers.
        
        Returns:
            list: A list of dictionaries with customer details.
        """
        try:
            customers = db.session.query(Customer).all()
            customer_list = []

            for customer in customers:
                customer_data = {
                    'id': customer.id,
                    'firstName': customer.firstName,
                    'lastName': customer.lastName,
                    'type': customer.cusType
                   
                }

                customer_list.append(customer_data)

            return customer_list

        except Exception as e:
            db.session.rollback()
            return f"An error occurred while listing customers: {e}"

    def display_customer_details(self, customer_id):
        """
        Display details of a customer by customer ID, including Corporate Customers.

        Args:
            customer_id (int): The ID of the customer to display.

        Returns:
            dict: A dictionary containing customer details if found, or an error message if not found.
        """
        try:
            # Try to retrieve the customer record by ID
            customer = db.session.query(Customer).filter_by(id=customer_id).one()
            
            # Determine if this customer is a corporate customer
            if isinstance(customer, CorporateCustomer):
                customer_data = {
                    'id': customer.id,
                    'firstName': customer.firstName,
                    'lastName': customer.lastName,
                    'address': customer.custAddress,
                    'balance': customer.custBalance,
                    'maxOwing': customer.maxOwing,
                    'customerType': "Corporate Customer",
                    'discountRate': customer.discountRate,
                    'maxCredit': customer.maxCredit,
                    'minBalance': customer.minBalance,
                    }
                   
            else:
           
                customer_data = {
                    'id': customer.id,
                    'firstName': customer.firstName,
                    'lastName': customer.lastName,
                    'address': customer.custAddress,
                    'balance': customer.custBalance,
                    'maxOwing': customer.maxOwing,
                    'customerType': 'Customer',
                }
            return customer_data

        except NoResultFound:
            return {"error": f"Customer with ID {customer_id} not found."}
        except Exception as e:
            db.session.rollback()
            return {"error": f"An error occurred while displaying customer details: {e}"}
        

    def list_products(self):
        """
        Display a list of all vegetables
        
        Returns:
            list: A list of dictionaries with veggie details, including image sources, categorized by type.
        """
        try:
            veggies = db.session.query(Veggie).all()  
            veggie_list = []

            for veggie in veggies:
               
                veggie_data = {
                    'id': veggie.id,
                    'name': veggie.vegName,
                    'category': veggie.vegType,
                    'img': veggie.img_src,
                    'unit' : veggie.unit,
                    'price': veggie.price
                }

                # Add subclass-specific data
                if isinstance(veggie, WeightedVeggie):
                    veggie_data.update({
                        'type': 'Weighted',
                        'weighted': veggie.weightUnit,
                       
                    })
                elif isinstance(veggie, PackVeggie):
                    veggie_data.update({
                        'type': 'Pack',
                        'pack': veggie.pack,
                    
                    })
                elif isinstance(veggie, UnitPriceVeggie):
                    veggie_data.update({
                        'type': 'Unit',
                        'unit': veggie.vegUnit,
                    
                    })
                
                veggie_list.append(veggie_data)

            return veggie_list
      

        except Exception as e:
            db.session.rollback()
            return f"An error occurred while displaying the veggie list: {e}"
        
    def list_premade_boxes(self):
        """
        Display a list of all premade boxes with their details and included items.
        
        Returns:
            list: A list of dictionaries containing details of each premade box and its items.
        """
        try:
            # Query all premade boxes
            premade_boxes = db.session.query(PremadeBox).all()
            premade_box_list = []

            for box in premade_boxes:
                # Basic box details
                box_data = {
                    'id': box.id,
                    'name': 'Premade box',
                    'price': box.price,
                    'size': box.boxSize,
                    'content': box.boxContent,
                    'img': box.img_src 
                }

               
                premade_box_list.append(box_data)

            return premade_box_list

        except Exception as e:
            db.session.rollback()
            return f"An error occurred while displaying the premade box list: {e}"
        

    def sales_report(self):
        """
        Generate a report for total sales of the week, month, and year.
        
        Returns:
            dict: A dictionary containing total sales for the week, month, and year.
        """
        try:
            # Get current date and define date ranges as date objects only
            today = datetime.today().date()
            start_of_week = today - timedelta(days=today.weekday())
            start_of_month = today.replace(day=1)
            start_of_year = today.replace(month=1, day=1)

            # Initialize totals
            weekly_sales = 0
            monthly_sales = 0
            yearly_sales = 0

            # Query orders placed this year
            orders_year = db.session.query(Order).filter(
                Order.orderDate >= start_of_year
            ).all()
            
            for order in orders_year:
                order_date = order.orderDate  
                
                for order_line in order.listOfItems:
                    item = order_line.item
                    quantity = order_line.quantity

                    # Retrieve item price
                    item_price = item.get_price
                    total_item_price = item_price * quantity

                    # Add to yearly sales
                    yearly_sales += total_item_price

                    # Add to monthly and weekly sales if within the date range
                    if order_date >= start_of_month:
                        monthly_sales += total_item_price
                    if order_date >= start_of_week:
                        weekly_sales += total_item_price

      
            # Return formatted results
            return {
                "weekly_sales": round(weekly_sales, 2),
                "monthly_sales": round(monthly_sales, 2),
                "yearly_sales": round(yearly_sales, 2),
            }
        
        except Exception as e:
            db.session.rollback()
            print(f"Error in sales_report: {e}")
            return {"error": f"An error occurred while generating the sales report: {e}"}
        
    
    def get_popularity_items(self):
        """
        Finds the most popular and least popular item(s) based on the total quantity ordered.

        Returns:
            dict: A dictionary containing two lists with item details for the most popular and least popular items.
        """
        try:
            # Dictionary to store item popularity
            item_popularity = {}

            # Retrieve all orders
            orders = db.session.query(Order).all()

            # Loop through each order and each item in the order
            for order in orders:
                for order_line in order.listOfItems:
                    item = order_line.item  # Retrieve item instance
                    quantity = order_line.quantity

                    # Update the item popularity count
                    if item in item_popularity:
                        item_popularity[item] += quantity
                    else:
                        item_popularity[item] = quantity

            # If no orders exist, return empty lists
            if not item_popularity:
                return {"most_popular": [], "least_popular": []}

            # Find the maximum and minimum order counts
            max_quantity = max(item_popularity.values())
            min_quantity = min(item_popularity.values())

            def item_details(item, quantity):

                if isinstance(item, Veggie):
                   return {
                    "item_id": item.id,
                    "img": item.img_src,  
                    "quantity": quantity,
                    "name": item.vegName,  
                  }
                if isinstance(item, PremadeBox):
                   return {
                    "item_id": item.id,
                    "img": item.img_src,  
                    "quantity": quantity,
                    "name": f"Premade Box - {item.boxContent}",  
                  }

            # Extract most popular items with details
            most_popular_items = [
                item_details(item, quantity)
                for item, quantity in item_popularity.items()
                if quantity == max_quantity
            ]

            # Extract least popular items with details
            least_popular_items = [
                item_details(item, quantity)
                for item, quantity in item_popularity.items()
                if quantity == min_quantity
            ]

            
            return {
                "most_popular": most_popular_items,
                "least_popular": least_popular_items,
            }

        except Exception as e:
            db.session.rollback()
            print(f"Error in get_popularity_items: {e}")
            return {"error": f"An error occurred while calculating popularity items: {e}"}