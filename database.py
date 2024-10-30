from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import date
from sqlalchemy.ext.hybrid import hybrid_property



# Create an engine to connect to MySQL database
engine = create_engine('mysql+pymysql://root:wsXY6205506@localhost:3306/fresh_harvest_veggies_db')
Base = declarative_base()

declarative_base()

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    firstName = Column(String(255))
    lastName = Column(String(255))
    password = Column(String(255))
    username = Column(String(255))
    type = Column(String(50)) 

    __mapper_args__ = {
        'polymorphic_on': type,  
        'polymorphic_identity': 'person'  
    }

    def __init__(self, firstName, lastName, password, username):
        self.firstName = firstName
        self.lastName = lastName
        self.password = password
        self.username= username

class Customer(Person):
    __tablename__ = 'customer'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    custAddress = Column(String(255))
    custBalance = Column(Float)
    maxOwing = Column(Float)
    cusType = Column(String(50))
    orders = relationship("Order", back_populates="customer")


    __mapper_args__ = {
        'polymorphic_on': cusType, 
        'polymorphic_identity': 'customer',
    }

    def __init__(self, firstName, lastName, password, username,custAddress, custBalance, maxOwing):
        super().__init__(firstName=firstName, lastName=lastName, password=password, username=username)
        self.custAddress = custAddress
        self.custBalance = custBalance
    
        self.maxOwing = maxOwing
        self.type = 'customer'
       
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

class OrderLine(Base):
    __tablename__ = 'orderline'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    item_id = Column(Integer, ForeignKey('item.id'))
  
    
    quantity = Column(Integer, nullable=False) 
    order = relationship("Order", back_populates="listOfItems")
    item = relationship("Item")
 

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    orderDate = Column(Date)
    orderStatus = Column(String(50))
    delivery = Column(String(255))
    customer = relationship('Customer', back_populates='orders')
    listOfItems = relationship("OrderLine", back_populates="order")

    def __init__(self, customer_id, orderDate, orderStatus, delivery):
        self.customer_id = customer_id
        self.orderDate = orderDate
        self.orderStatus = orderStatus
        self.delivery = delivery




class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    img_src = Column(String(255))
    type = Column(String(50)) 

    __mapper_args__ = {
        'polymorphic_on': type,  
        'polymorphic_identity': 'item'  
    }

    def __init__(self, img_src):
        self.img_src = img_src


class Veggie(Item):
    __tablename__ = 'veggie'
    id = Column(Integer, ForeignKey('item.id'), primary_key=True)  
    vegName = Column(String(50), nullable=False)
    vegType = Column(String(50))
    unit = Column(String(50))
    price = Column(Float)

    __mapper_args__ = {
        'polymorphic_on': vegType, 
        'polymorphic_identity': 'veggie',
    }

    

    def __init__(self, img_src, vegName, unit, price):
        super().__init__(img_src=img_src)
        self.vegName = vegName
        self.unit = unit
        self.price = price
        self.type = 'veggie'

class PremadeBox(Item):
    __tablename__ = 'premadebox'
    id = Column(Integer, ForeignKey('item.id'), primary_key=True)
    boxSize = Column(String(255))
    numOfBoxes = Column(Integer)
    boxContent = Column(String(255))
    price = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'premadebox',
    }

    def __init__(self, img_src,boxSize, numOfBoxes, boxContent,price):
        super().__init__(img_src=img_src)
        self.boxSize = boxSize
        self.numOfBoxes = numOfBoxes
        self.boxContent = boxContent
        self.price = price

        

class Payment(Base):
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True)
    paymentAmount = Column(Float)
    paymentDate = Column(Date)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_on': type,  
        'polymorphic_identity': 'payment' 
    }
    def __init__(self, paymentAmount, paymentDate,customer_id):
        self.paymentAmount = paymentAmount
        self.paymentDate = paymentDate
        self.customer_id = customer_id
     



class CorporateCustomer(Customer):
    __tablename__ = 'corporatecustomer'
    id = Column(Integer, ForeignKey('customer.id'), primary_key=True)
    discountRate = Column(Float)
    maxCredit = Column(Float)
    minBalance = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'corporatecustomer', 
    }

    def __init__(self, firstName, lastName, password, username,custAddress, custBalance,maxOwing, discountRate, maxCredit, minBalance):
        super().__init__(firstName=firstName, lastName=lastName, password=password, username=username,custAddress=custAddress, custBalance=custBalance,maxOwing=maxOwing)
        self.cusType = 'corporatecustomer'
        self.discountRate = discountRate
        self.maxCredit = maxCredit
        self.minBalance = minBalance


class AccountPayment(Payment):
    __tablename__ = 'accountpayment'
    id = Column(Integer, ForeignKey('payment.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'accountpayment',
    }

    def __init__(self, paymentAmount, paymentDate,customer_id):
        super().__init__(paymentAmount=paymentAmount, paymentDate=paymentDate, customer_id=customer_id)
        self.type = 'accountpayment'
        

class CreditCardPayment(Payment):
    __tablename__ = 'creditcardpayment'
    id = Column(Integer, ForeignKey('payment.id'), primary_key=True)
    nameOncard = Column(String(50))
    cardNumber = Column(String(255))
    expiration = Column(String(50))
    cvv = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'creditcardpayment',
    }

    def __init__(self, paymentAmount, paymentDate,customer_id, nameOncard, cardNumber, expiration, cvv):
        super().__init__(paymentAmount=paymentAmount, paymentDate=paymentDate, customer_id=customer_id)
        self.type = 'creditcardpayment'
        self.nameOncard = nameOncard
        self.cardNumber = cardNumber
        self.expiration = expiration
        self.cvv = cvv

class DebitCardPayment(Payment):
    __tablename__ = 'debitcardpayment'
    id = Column(Integer, ForeignKey('payment.id'), primary_key=True)
    nameOncard = Column(String(50))
    cardNumber = Column(String(255))
    expiration = Column(String(50))
    cvv = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'debitcardpayment',
    }

    def __init__(self, paymentAmount, paymentDate,customer_id, nameOncard, cardNumber, expiration, cvv):
        super().__init__(paymentAmount=paymentAmount, paymentDate=paymentDate, customer_id=customer_id)
        self.type = 'debitcardpayment'
        self.nameOncard = nameOncard
        self.cardNumber = cardNumber
        self.expiration = expiration
        self.cvv = cvv

class WeightedVeggie(Veggie):
    __tablename__ = 'weightedveggie'
    id = Column(Integer, ForeignKey('veggie.id'), primary_key=True)  
    weightUnit = Column(Float)
    
    __mapper_args__ = {
        'polymorphic_identity': 'weightedveggie', 
    }


    def __init__(self, img_src, price, vegName, unit, weightUnit):
        super().__init__(img_src=img_src, vegName=vegName, unit=unit, price=price)
        self.vegType = 'weightedveggie'
        self.weightUnit = weightUnit
       

class PackVeggie(Veggie):
    __tablename__ = 'packveggie'
    id = Column(Integer, ForeignKey('veggie.id'), primary_key=True)  
    pack=Column(Integer)
   
    __mapper_args__ = {
        'polymorphic_identity': 'packveggie',
    }


    def __init__(self, img_src, vegName, unit, price, pack):
        super().__init__(img_src=img_src, vegName=vegName, unit=unit, price=price)
        self.vegType = 'packveggie'
        self.pack = pack
     

class UnitPriceVeggie(Veggie):
    __tablename__ = 'unitpriceveggie'
    id = Column(Integer, ForeignKey('veggie.id'), primary_key=True)  
    vegUnit=Column(Integer)


    __mapper_args__ = {
        'polymorphic_identity': 'unitpriceveggie',
    }


    def __init__(self, img_src, vegName, unit, price,vegUnit):
        super().__init__(img_src=img_src, vegName=vegName, unit=unit, price=price)
        self.vegType = 'unitpriceveggie'
        self.vegUnit= vegUnit
      


# Create all tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()



staff1 = Staff(firstName="Alice", lastName="Johnson", password="1234", username="alicej", dateJoined=date(2022, 1, 15), deptName="Sales",staffID=1)

customer1 = Customer(firstName="Bob", lastName="Brown", password="1234", username="bobb", custAddress="123 Main St 1010", custBalance=100.0, maxOwing=50.0)

corporate_customer1 = CorporateCustomer(firstName="Shane", lastName="Xu", password="1234", username="foliageandvine", custAddress="456 Corporate Blvd 1010", custBalance=500.0,maxOwing=200.0, discountRate=10.0, maxCredit=1000.0, minBalance=50.0)


premade_box1 = PremadeBox(img_src="images/PremadeBox.jpg", boxSize="Small", numOfBoxes=10, boxContent="Carrots, Potatoes", price = 19.99)

weighted_veggie1 = WeightedVeggie(img_src="images/Galic.jpg",vegName="Galic", unit='g', weightUnit=500, price=9.99)
weighted_veggie2 = WeightedVeggie(img_src="images/Tomatos.jpg",vegName="Tomatos", unit='kg',weightUnit=1, price=5.99)
pack_veggie1 = PackVeggie(img_src="images/Eggplant.jpg",vegName="Eggplant", unit='bag', pack=1, price=4.99)
unit_price_veggie1 = UnitPriceVeggie(img_src="images/Squash.jpg",vegName="Squash", unit='ea', price=4.99, vegUnit=1)
unit_price_veggie2 = UnitPriceVeggie(img_src="images/Broccoli.jpg",vegName="Broccoli", unit='ea', price=2.99, vegUnit=1)
unit_price_veggie3 = UnitPriceVeggie(img_src="images/Avocado.jpg",vegName="Avocado", unit='ea', price=1.19, vegUnit=1)



# Add all the objects to the session
session.add_all([staff1, customer1, corporate_customer1, premade_box1, weighted_veggie1, weighted_veggie2, pack_veggie1, unit_price_veggie1, unit_price_veggie2, unit_price_veggie3])

session.commit()

# Create OrderLines (with quantity and items)
orderline1 = OrderLine(quantity=5, item_id=premade_box1.id)
orderline2 = OrderLine(quantity=2, item_id=pack_veggie1.id)
orderline3 = OrderLine(quantity=10, item_id=unit_price_veggie1.id)

# Create Orders
order1 = Order(customer_id=customer1.id, orderDate=date(2024, 10, 21),  orderStatus="Processing", delivery = "Pickup")
order2 = Order(customer_id=corporate_customer1.id, orderDate=date(2024, 10, 28),  orderStatus="Fulfilled", delivery = "Delivery")


# Add order lines to orders
order1.listOfItems.append(orderline1)
order1.listOfItems.append(orderline2)
order2.listOfItems.append(orderline3)

# Add orders to customer
customer1.orders.append(order1)
corporate_customer1.orders.append(order2)



account_payment1 = AccountPayment(paymentAmount=100.0, paymentDate=date(2024, 10, 28), customer_id=customer1.id)
debit_card_payment1 = DebitCardPayment(paymentAmount=150.0, paymentDate=date(2024, 10, 29), customer_id=corporate_customer1.id, nameOncard="ShaneX", cardNumber="2323232323333", expiration="03/30", cvv=422)

session.add_all([order1, order2, orderline1, orderline2, orderline3, account_payment1, debit_card_payment1])

# Commit the session to save the objects to the database
session.commit()

# Close the session
session.close()

print("Test data successfully added.")


