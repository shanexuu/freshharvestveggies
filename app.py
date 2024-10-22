import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from models.Item import db, Item  # Importing db from Item
from models.Veggie import Veggie 



basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:wsXY6205506@localhost:3306/fresh_harvest_veggies_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)





@app.route("/")
def index():

    veggie = Veggie.query.all()
   
    return render_template('index.html', veggie=veggie)


@app.route('/<int:id>/')
def item(id):
    veggie = Veggie.query.get_or_404(id)
    return render_template('item-details.html', veggie=veggie)


if __name__ == '__main__':
    app.run(debug=True)