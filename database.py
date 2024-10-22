from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import date


# Create an engine to connect to MySQL database
engine = create_engine('mysql+pymysql://root:wsXY6205506@localhost:3306/fresh_harvest_veggies_db')
Base = declarative_base()

declarative_base()

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    firstName = Column(String(50))
    lastName = Column(String(50))
    password = Column(String(50))
    username = Column(String(50))

class Staff(Person):
    __tablename__ = 'staff'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    dateJoined = Column(Date)
    deptName = Column(String(50))
    listOfCustomers = Column(String(255))
    listOfOrders = Column(String(255))
    premadeBoxes = Column(String(255))
    staffID = Column(Integer)
    veggies = Column(String(255))

class Customer(Person):
    __tablename__ = 'customer'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    custAddress = Column(String(255))
    custBalance = Column(Float)
    custID = Column(Integer)
    maxOwing = Column(Float)

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    orderCustomer = Column(Integer, ForeignKey('customer.id'))
    orderDate = Column(Date)
    orderNumber = Column(Integer)
    orderStatus = Column(String(50))
    listOfItems = relationship("OrderLine", back_populates="order")

class OrderLine(Base):
    __tablename__ = 'orderline'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    itemNumber = Column(Integer)
    order = relationship("Order", back_populates="listOfItems")

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    img_src = Column(String(255))

class Veggie(Item):
    __tablename__ = 'veggie'
    id = Column(Integer, ForeignKey('item.id'), primary_key=True)
    vegName = Column(String(50))

class PremadeBox(Item):
    __tablename__ = 'premadebox'
    id = Column(Integer, ForeignKey('item.id'), primary_key=True)
    boxSize = Column(String(50))
    numOfBoxes = Column(Integer)
    boxContent = Column(String(255))

class Payment(Base):
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True)
    paymentAmount = Column(Float)
    paymentDate = Column(Date)
    paymentID = Column(Integer)
    customer_id = Column(Integer, ForeignKey('customer.id'))

class CorporateCustomer(Customer):
    __tablename__ = 'corporatecustomer'
    id = Column(Integer, ForeignKey('customer.id'), primary_key=True)
    discountRate = Column(Float)
    maxCredit = Column(Float)
    minBalance = Column(Float)

class CreditCardPayment(Payment):
    __tablename__ = 'creditcardpayment'
    id = Column(Integer, ForeignKey('payment.id'), primary_key=True)
    cardExpiryDate = Column(Date)
    cardNumber = Column(String(50))
    cardType = Column(String(50))

class DebitCardPayment(Payment):
    __tablename__ = 'debitcardpayment'
    id = Column(Integer, ForeignKey('payment.id'), primary_key=True)
    bankName = Column(String(50))
    debitCardNumber = Column(String(50))

class WeightedVeggie(Veggie):
    __tablename__ = 'weightedveggie'
    id = Column(Integer, ForeignKey('veggie.id'), primary_key=True)
    weight = Column(Float)
    weightPerKilo = Column(Float)

class PackVeggie(Veggie):
    __tablename__ = 'packveggie'
    id = Column(Integer, ForeignKey('veggie.id'), primary_key=True)
    numOfPack = Column(Integer)
    pricePerPack = Column(Float)

class UnitPriceVeggie(Veggie):
    __tablename__ = 'unitpriceveggie'
    id = Column(Integer, ForeignKey('veggie.id'), primary_key=True)
    pricePerUnit = Column(Float)
    quantity = Column(Integer)




# Create all tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Add test data for Person, Staff, and Customer
person1 = Person(firstName="John", lastName="Doe", password="password123", username="johndoe")
person2 = Person(firstName="Jane", lastName="Smith", password="password456", username="janesmith")

staff1 = Staff(firstName="Alice", lastName="Johnson", password="password789", username="alicej", 
               dateJoined=date(2022, 1, 15), deptName="Sales", listOfCustomers="Customer1, Customer2", 
               listOfOrders="Order1, Order2", premadeBoxes="Box1, Box2", staffID=1, veggies="Carrot, Potato")

customer1 = Customer(firstName="Bob", lastName="Brown", password="password654", username="bobb", 
                     custAddress="123 Main St", custBalance=100.0, custID=1, maxOwing=50.0)

corporate_customer1 = CorporateCustomer(firstName="Corp", lastName="Inc", password="corp_password", 
                                        username="corp_user", custAddress="456 Corporate Blvd", 
                                        custBalance=500.0, custID=2, maxOwing=200.0, discountRate=10.0, 
                                        maxCredit=1000.0, minBalance=50.0)

# Add test data for Orders and OrderLine
order1 = Order(orderCustomer=customer1.id, orderDate=date(2023, 5, 20), orderNumber=12345, orderStatus="Pending")
orderline1 = OrderLine(order=order1, itemNumber=1)

# Add test data for Items, Veggies, and PremadeBox
item1 = Item(img_src="images/Carrots.jpg")
veggie1 = Veggie(img_src="images/Carrots.jpg", vegName="Carrot")
premade_box1 = PremadeBox(img_src="images/Carrots.jpg", boxSize="Large", numOfBoxes=10, boxContent="Carrots, Potatoes")

weighted_veggie1 = WeightedVeggie(img_src="images/Carrots.jpg",vegName="Carrot", weight=2.5, weightPerKilo=4.0)
pack_veggie1 = PackVeggie(img_src="images/Carrots.jpg",vegName="Broccoli", numOfPack=5, pricePerPack=10.0)
unit_price_veggie1 = UnitPriceVeggie(img_src="images/Carrots.jpg",vegName="Tomato", pricePerUnit=0.5, quantity=20)

# Add test data for Payments and Payment types
payment1 = Payment(paymentAmount=100.0, paymentDate=date(2023, 5, 21), paymentID=1, customer_id=customer1.id)
credit_card_payment1 = CreditCardPayment(paymentAmount=100.0, paymentDate=date(2023, 5, 21), 
                                         paymentID=2, customer_id=customer1.id, cardExpiryDate=date(2025, 12, 31), 
                                         cardNumber="1234567890123456", cardType="Visa")

debit_card_payment1 = DebitCardPayment(paymentAmount=150.0, paymentDate=date(2023, 6, 15), 
                                       paymentID=3, customer_id=corporate_customer1.id, bankName="Bank XYZ", 
                                       debitCardNumber="9876543210987654")

# Add all the objects to the session
session.add_all([
    person1, person2, staff1, customer1, corporate_customer1,
    order1, orderline1, item1, veggie1, premade_box1, weighted_veggie1, 
    pack_veggie1, unit_price_veggie1, payment1, credit_card_payment1, debit_card_payment1
])

# Commit the session to save the objects to the database
session.commit()

# Close the session
session.close()

print("Test data successfully added.")



# Close the session
