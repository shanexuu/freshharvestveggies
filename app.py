import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from models.Item import db, Item  # Importing db from Item
from models.Veggie import Veggie 
from models.PackVeggie import PackVeggie 
from models.WeightedVeggie import WeightedVeggie
from models.UnitPriceVeggie import UnitPriceVeggie

from sqlalchemy.orm import sessionmaker


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:wsXY6205506@localhost:3306/fresh_harvest_veggies_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)




@app.route("/")
def index():

    veggie = Veggie.query.all()
   
    return render_template('index.html', veggie=veggie)


@app.route('/shop/<int:id>/')
def item(id):

    
    # Fetch the veggie by id
    veggie = Veggie.query.get_or_404(id)

    if veggie is None:
        return "Veggie not found", 404

    # Check the type of veggie and get the relevant price
    if isinstance(veggie, WeightedVeggie):
        price = veggie.pricePerWeight  # price per kilo
        unit = "per kilo"
    elif isinstance(veggie, PackVeggie):
        price = veggie.pricePerPack  # price per pack
        unit = "per pack"
    elif isinstance(veggie, UnitPriceVeggie):
        price = veggie.pricePerUnit  # price per pack
        unit = "per pack"

    else:
        price = None
        unit = ""


    return render_template('item-details.html',  veggie=veggie, price=price, unit=unit)


if __name__ == '__main__':
    app.run(debug=True)