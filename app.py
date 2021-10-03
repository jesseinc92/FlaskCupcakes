"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request
from sqlalchemy.sql.elements import Null
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yessiree'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()


def serialize_item(cupcake):
    '''Create object that can be turned into JSON.'''

    return {
        'id': cupcake.id,
        'flavor': cupcake.flavor,
        'size': cupcake.size,
        'rating': cupcake.rating,
        'image': cupcake.image
    }


@app.route('/api/cupcakes')
def get_all_cupcakes():
    '''Get data about all cupcakes.'''

    cupcakes = Cupcake.query.all()
    serialized = [serialize_item(cupcake) for cupcake in cupcakes]

    return jsonify(cupcakes=serialized)


@app.route('/api/cupcakes/<int:cupcake_id>')
def get_single_cupcake(cupcake_id):
    '''Get data about a single cupcake.'''
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    return jsonify(cupcake={
        'id': cupcake.id,
        'flavor': cupcake.flavor,
        'size': cupcake.size,
        'rating': cupcake.rating,
        'image': cupcake.image
    })


@app.route('/api/cupcakes', methods=['POST'])
def create_new_cupcake():
    '''Creates a new cupcake with the appropriate parameters.'''
    
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json.get('image', Null)
    
    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    
    db.session.add(new_cupcake)
    db.session.commit()
    
    serialized = serialize_item(new_cupcake)
    
    return (jsonify(cupcake=serialized), 201)