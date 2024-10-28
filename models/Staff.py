from sqlalchemy import Column, String, ForeignKey, Integer, Date
from .Person import Person
from datetime import date
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