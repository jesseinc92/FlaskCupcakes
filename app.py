"""Flask app for Cupcakes"""

from flask import Flask
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yessiree'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()


