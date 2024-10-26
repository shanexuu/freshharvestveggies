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
    custID = Column(Integer)
    maxOwing = Column(Float)
    cusType = Column(String(50))

    orders = relationship("Order", back_populates="customer")


    __mapper_args__ = {
        'polymorphic_on': cusType, 
        'polymorphic_identity': 'customer',
    }

    def __init__(self, firstName, lastName, password, username,custAddress, custBalance, custID, maxOwing):
        super().__init__(firstName=firstName, lastName=lastName, password=password, username=username)
        self.custAddress = custAddress
        self.custBalance = custBalance
        self.custID = custID
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
    customer_id = Column(Integer, ForeignKey('customer.id'))
    orderDate = Column(Date)
    orderStatus = Column(String(50))
    customer = relationship('Customer', back_populates='orders')
    listOfItems = relationship("OrderLine", back_populates="order")




    


      

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

    __mapper_args__ = {
        'polymorphic_on': 'vegType', 
        'polymorphic_identity': 'veggie',
    }

    def __init__(self, img_src, vegName, unit):
        super().__init__(img_src=img_src)
        self.vegName = vegName
        self.unit = unit
        self.type = 'veggie'

class PremadeBox(Item):
    __tablename__ = 'premadebox'
    id = Column(Integer, ForeignKey('item.id'), primary_key=True)
    boxSize = Column(String(255))
    numOfBoxes = Column(Integer)
    boxContent = Column(String(255))

    __mapper_args__ = {
        'polymorphic_identity': 'premadebox',
    }

    def __init__(self, img_src, boxSize, numOfBoxes, boxContent):
        super().__init__(img_src=img_src)
        self.boxSize = boxSize
        self.numOfBoxes = numOfBoxes
        self.boxContent = boxContent

        

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

    __mapper_args__ = {
        'polymorphic_identity': 'corporatecustomer', 
    }

    def __init__(self, firstName, lastName, password, username,custAddress, custBalance, custID, maxOwing, discountRate, maxCredit, minBalance):
        super().__init__(firstName=firstName, lastName=lastName, password=password, username=username,custAddress=custAddress, custBalance=custBalance, custID=custID, maxOwing=maxOwing)
        self.cusType = 'corporatecustomer'
        self.discountRate = discountRate
        self.maxCredit = maxCredit
        self.minBalance = minBalance

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
    weightUnit = Column(Float)
    pricePerWeight = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'weightedveggie', 
    }

    def __init__(self, img_src, vegName, unit, weightUnit, pricePerWeight):
        super().__init__(img_src=img_src, vegName=vegName, unit=unit)
        self.vegType = 'weightedveggie'
        self.weightUnit = weightUnit
        self.pricePerWeight = pricePerWeight

class PackVeggie(Veggie):
    __tablename__ = 'packveggie'
    id = Column(Integer, ForeignKey('veggie.id'), primary_key=True)  
    pack=Column(Integer)
    pricePerPack = Column(Float)
    __mapper_args__ = {
        'polymorphic_identity': 'packveggie',
    }

    def __init__(self, img_src, vegName, unit, pack, pricePerPack):
        super().__init__(img_src=img_src, vegName=vegName, unit=unit)
        self.vegType = 'packveggie'
        self.pack = pack
        self.pricePerPack = pricePerPack

class UnitPriceVeggie(Veggie):
    __tablename__ = 'unitpriceveggie'
    id = Column(Integer, ForeignKey('veggie.id'), primary_key=True)  
    vegUnit=Column(Integer)
    pricePerUnit = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'unitpriceveggie',
    }

    def __init__(self, img_src, vegName, unit, vegUnit, pricePerUnit):
        super().__init__(img_src=img_src, vegName=vegName, unit=unit)
        self.vegType = 'unitpriceveggie'
        self.vegUnit= vegUnit
        self.pricePerUnit = pricePerUnit


# Create all tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()



staff1 = Staff(firstName="Alice", lastName="Johnson", password="1234", username="alicej", dateJoined=date(2022, 1, 15), deptName="Sales",staffID=1)

customer1 = Customer(firstName="Bob", lastName="Brown", password="1234", username="bobb", custAddress="123 Main St", custBalance=100.0, custID=1, maxOwing=50.0)

corporate_customer1 = CorporateCustomer(firstName="Shane", lastName="Xu", password="1234", username="foliageandvine", custAddress="456 Corporate Blvd", custBalance=500.0, custID=2, maxOwing=200.0, discountRate=10.0, maxCredit=1000.0, minBalance=50.0)


premade_box1 = PremadeBox(img_src="images/PremadeBox.jpg", boxSize="Large", numOfBoxes=10, boxContent="Carrots, Potatoes")

weighted_veggie1 = WeightedVeggie(img_src="images/Galic.jpg",vegName="Galic", unit='g', weightUnit=500, pricePerWeight=9.99)
weighted_veggie2 = WeightedVeggie(img_src="images/Tomatos.jpg",vegName="Tomatos", unit='kg',weightUnit=1,  pricePerWeight=5.99)
pack_veggie1 = PackVeggie(img_src="images/Eggplant.jpg",vegName="Eggplant", unit='bag', pack=1, pricePerPack=4.99)
unit_price_veggie1 = UnitPriceVeggie(img_src="images/Squash.jpg",vegName="Squash", unit='ea', pricePerUnit=0.5, vegUnit=1)
unit_price_veggie2 = UnitPriceVeggie(img_src="images/Broccoli.jpg",vegName="Broccoli", unit='ea', pricePerUnit=2.99, vegUnit=1)
unit_price_veggie3 = UnitPriceVeggie(img_src="images/Avocado.jpg",vegName="Avocado", unit='ea', pricePerUnit=1.19, vegUnit=1)




# Add test data for Payments and Payment types
payment1 = Payment(paymentAmount=100.0, paymentDate=date(2023, 5, 21), paymentID=1, customer_id=customer1.id)
credit_card_payment1 = CreditCardPayment(paymentAmount=100.0, paymentDate=date(2023, 5, 21), paymentID=2, customer_id=customer1.id, cardExpiryDate=date(2025, 12, 31), cardNumber="1234567890123456", cardType="Visa")

debit_card_payment1 = DebitCardPayment(paymentAmount=150.0, paymentDate=date(2023, 6, 15), paymentID=3,customer_id=corporate_customer1.id, bankName="Bank XYZ", debitCardNumber="9876543210987654")

# Add all the objects to the session
session.add_all([staff1, customer1, corporate_customer1, premade_box1, weighted_veggie1, weighted_veggie2, pack_veggie1, unit_price_veggie1, unit_price_veggie2, unit_price_veggie3, payment1, credit_card_payment1, debit_card_payment1
])

session.commit()

# Create OrderLines (with quantity and items)
orderline1 = OrderLine(quantity=5, item_id=premade_box1.id)
orderline2 = OrderLine(quantity=2, item_id=weighted_veggie1.id)
orderline3 = OrderLine(quantity=10, item_id=unit_price_veggie1.id)

# Create Orders
order1 = Order(customer_id=customer1.id, orderDate=date(2023, 5, 21),  orderStatus="Processing")
order2 = Order(customer_id=corporate_customer1.id, orderDate=date(2024, 10, 21),  orderStatus="Shipped")


# Add order lines to orders
order1.listOfItems.append(orderline1)
order1.listOfItems.append(orderline2)
order2.listOfItems.append(orderline3)

# Add orders to customer
customer1.orders.append(order1)
corporate_customer1.orders.append(order2)

session.add_all([order1, order2, orderline1, orderline2, orderline3 ])

# Commit the session to save the objects to the database
session.commit()

# Close the session
session.close()

print("Test data successfully added.")


