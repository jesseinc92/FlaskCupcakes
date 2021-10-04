"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request, render_template
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
    

@app.route('/')
def cupcake_homepage():
    '''Displays a list of cupcakes, as well as a form to add form.'''
    return render_template('cupcake.html')


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


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    '''Update a single cupcake in the database.'''
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    
    db.session.commit()
    
    serialized = serialize_item(cupcake)
    
    return jsonify(cupcake=serialized)
    
    
@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    '''Delete a cupcake from the database.'''
    
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    
    return jsonify(message='deleted')