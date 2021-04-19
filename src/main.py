
# IMPORTANT: run 'URL/populate' to populate database for testing purposes ('/populate' endpoint created below)

"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os # library in phyton that allows me to interact with the operating system (os)
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger # not used in this exercise
from flask_cors import CORS # to avoid CORS (Cross-Origin Resource Sharing) domain errors 
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
from service import Service

# import Flask-JWT-Extended extension library
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = Flask(__name__)    # create new Flask app
app.url_map.strict_slashes = False    # to allow URL with or without final slash "/"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')  # connect to database specified in file: .env
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   # if "true", everytime I modify models.py it creates a migration
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.environ.get('TOKEN_KEY')  # for security purposes, located in .env file, which is also located in .gitignore
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/token", methods=["POST"])
def create_token():
    email = request.json.get("email", None) # "None" parameter, see below
    password = request.json.get("password", None)

    # None parameter is used to create a conditional in case no values are passed. 
    # Example: 
    # if username is None:
    #     return jsonify({msg: "value not found"})  

    user = User.query.filter_by(email=email, password=password).first()
    # Filter() method filters the records before we fire the select with all() or first()

    if user is None:
         return jsonify({"msg": "Bad username or password"}), 401
    
    print("Authorized user: ", user)

    access_token = create_access_token(identity=user.id) # this line indicates that function get_jwt_identity() returns "user.id"
    return jsonify(access_token=access_token)

### User endpoints [GET, POST, PUT, UPDATE]: 
@app.route('/user', methods=['GET'])
def get_all_user():
    all_users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), all_users)) 
    print("GET all_users: ", all_users)
    return jsonify(all_users), 200

@app.route('/user/<int:id>', methods=['GET'])
def get_single_user(id):
    user = User.query.get(id)

    if user is None:
        raise APIException('User not found', status_code=404)

    print("GET single user: ", user)
    return jsonify(user.serialize()), 200

@app.route('/user', methods=['POST'])
def create_user():
    request_body = request.get_json()
    user = User(username=request_body["username"], email=request_body["email"], password=request_body["password"])
    db.session.add(user)
    db.session.commit()
    print("User created: ", request_body)
    return jsonify(request_body), 200

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    request_body = request.get_json()
    user = User.query.get(user_id)

    if user is None:
        raise APIException('User not found', status_code=404)
    if "username" in request_body:
        user.username = request_body["username"]
    if "email" in request_body:
        user.email = request_body["email"]
    if "password" in request_body:
        user.password = request_body["password"]
    
    db.session.commit()

    print("User property updated: ", request_body)
    return jsonify(request_body), 200

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    if user is None:
        raise APIException('User not found', status_code=404)

    db.session.delete(user)
    db.session.commit()
    response_body = {
         "msg": "User delete successful",
    }
    return jsonify(response_body), 200


### Character endpoints [GET, POST, PUT, UPDATE]: 
@app.route('/character', methods=['GET'])
def get_all_character():
    all_characters = Character.query.all()
    all_characters = list(map(lambda x: x.serialize(), all_characters)) 
    return jsonify(all_characters), 200

@app.route('/character/<int:id>', methods=['GET'])
def get_single_character(id):
    character = Character.query.get(id)

    if character is None:
        raise APIException('Character not found', status_code=404)

    return jsonify(character.serialize()), 200

@app.route('/character', methods=['POST'])
def create_character():
    request_body = request.get_json()
    character = Character(name=request_body["name"], birth_year=request_body["birth_year"], eye_color=request_body["eye_color"], gender=request_body["gender"], hair_color=request_body["hair_color"], height=request_body["height"], skin_color=request_body["skin_color"], item_type=request_body["item_type"])
    db.session.add(character)
    db.session.commit()
    print("Character created: ", request_body)
    return jsonify(request_body), 200

@app.route('/character/<int:id>', methods=['PUT'])
def update_character(id):
    request_body = request.get_json()
    character = Character.query.get(id)

    if character is None:
        raise APIException('Character not found', status_code=404)
    if "name" in request_body:
        character.name = request_body["name"]
    if "birth_year" in request_body:
        character.birth_year = request_body["birth_year"]
    if "eye_color" in request_body:
        character.eye_color = request_body["eye_color"]
    if "gender" in request_body:
        character.gender = request_body["gender"]
    if "hair_color" in request_body:
        character.hair_color = request_body["hair_color"]
    if "height" in request_body:
        character.height = request_body["height"]
    if "skin_color" in request_body:
        character.skin_color = request_body["skin_color"]
    
    db.session.commit()

    print("Character property updated: ", request_body)
    return jsonify(request_body), 200

@app.route('/character/<int:id>', methods=['DELETE'])
def delete_character(id):
    character = Character.query.get(id)

    if character is None:
        raise APIException('Character not found', status_code=404)

    db.session.delete(character)
    db.session.commit()
    response_body = {
         "msg": "Character delete successful",
    }
    return jsonify(response_body), 200


### Planet endpoints [GET, POST, PUT, UPDATE]: 
@app.route('/planet', methods=['GET'])
def get_all_planet():
    all_planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets)) 
    return jsonify(all_planets), 200

@app.route('/planet/<int:id>', methods=['GET'])
def get_single_planet(id):
    planet = Planet.query.get(id)

    if planet is None:
        raise APIException('Planet not found', status_code=404)

    return jsonify(planet.serialize()), 200

@app.route('/planet', methods=['POST'])
def create_planet():
    request_body = request.get_json()
    planet = Planet(name=request_body["name"], climate=request_body["climate"], diameter=request_body["diameter"], population=request_body["population"], rotation_period=request_body["rotation_period"], terrain=request_body["terrain"], item_type=request_body["item_type"])
    db.session.add(planet)
    db.session.commit()
    print("Planet created: ", request_body)
    return jsonify(request_body), 200

@app.route('/planet/<int:id>', methods=['PUT'])
def update_planet(id):
    request_body = request.get_json()
    planet = Planet.query.get(id)

    if planet is None:
        raise APIException('Planet not found', status_code=404)
    if "name" in request_body:
        planet.name = request_body["name"]
    if "climate" in request_body:
        planet.climate = request_body["climate"]
    if "diameter" in request_body:
        planet.diameter = request_body["diameter"]
    if "population" in request_body:
        planet.population = request_body["population"]
    if "rotation_period" in request_body:
        planet.rotation_period = request_body["rotation_period"]
    if "terrain" in request_body:
        planet.terrain = request_body["terrain"]
    
    db.session.commit()

    print("Planet property updated: ", request_body)
    return jsonify(request_body), 200

@app.route('/planet/<int:id>', methods=['DELETE'])
def delete_planet(id):
    planet = Planet.query.get(id)

    if planet is None:
        raise APIException('Planet not found', status_code=404)

    db.session.delete(planet)
    db.session.commit()
    response_body = {
         "msg": "Planet delete successful",
    }
    return jsonify(response_body), 200


### Favorite endpoints:
@app.route('/favorite', methods=['GET'])
@jwt_required()
def get_all_favorite():
    
    # Access the identity of the current user with get_jwt_identity()
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)
    if user is None:
        raise APIException('User not found', status_code=404)

    all_favorites = Service.get_favorites(current_user_id)
    return jsonify(all_favorites), 200

@app.route('/favorite', methods=['POST'])
@jwt_required()
def add_favorite():
    request_body = request.get_json()
    favorite = Favorite(item_id=request_body["item_id"], item_type=request_body["item_type"], user_id=request_body["user_id"])
    db.session.add(favorite)
    db.session.commit()
    print("Favorite added: ", request_body)
    return jsonify(request_body), 200

@app.route('/favorite/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_favorite(id):
    favorite = Favorite.query.get(id)

    if favorite is None:
        raise APIException('Favorite not found', status_code=404)

    db.session.delete(favorite)
    db.session.commit()
    response_body = {
         "msg": "Favorite delete successful",
    }
    return jsonify(response_body), 200


# Populate DB
@app.route('/populate', methods=['GET'])
def populate():
    u1 = User(username='user01', email='user01@example.com', password="01")
    u2 = User(username='user02', email='user02@example.com', password="02")
    u3 = User(username='user03', email='user03@example.com', password="03")

    c1 = Character(name='Luke Skywalker', birth_year='19BBY', gender='male', height='172.0', eye_color='blue', hair_color='blond', skin_color='fair', item_type='character')
    c2 = Character(name='C-3PO', birth_year='112BBY', gender='', height='167.0', eye_color='yellow', hair_color='n/a', skin_color='gold', item_type='character')
    c3 = Character(name='R2-D2', birth_year='33BBY', gender='n/a', height='96.0', eye_color='red', hair_color='n/a', skin_color='white, blue', item_type='character')
    c4 = Character(name='Darth Vader', birth_year='41.9BBY', gender='male', height='202.0', eye_color='yellow', hair_color='none', skin_color='white', item_type='character')
    c5 = Character(name='Leia Organa', birth_year='19BBY', gender='female', height='150.0', eye_color='brown', hair_color='brown', skin_color='light', item_type='character')
    c6 = Character(name='Owen Lars', birth_year='52BBY', gender='male', height='178.0', eye_color='blue', hair_color='brown, grey', skin_color='light', item_type='character')

    p1 = Planet(name='Tatooine', population='200000', terrain='desert', diameter='10465.0', climate='arid', rotation_period='23.0', item_type='planet')
    p2 = Planet(name='Alderaan', population='2000000000', terrain='grasslands, mountains', diameter='12500.0', climate='temperate', rotation_period='24.0', item_type='planet')
    p3 = Planet(name='Yavin IV', population='1000', terrain='jungle, rainforests', diameter='10200.0', climate='temperate, tropical', rotation_period='24.0', item_type='planet')
    p4 = Planet(name='Hoth', population='5000', terrain='tundra, ice caves, mountain ranges', diameter='7200.0', climate='frozen', rotation_period='23.0', item_type='planet')
    p5 = Planet(name='Dagobah', population='6500', terrain='swamp, jungles', diameter='8900.0', climate='murky', rotation_period='23.0', item_type='planet')
    p6 = Planet(name='Bespin', population='6000000', terrain='gas giant', diameter='118000.0', climate='temperate', rotation_period='12.0', item_type='planet')

    db.session.add_all([u1, u2, u3, c1, c2, c3, c4, c5, c6, p1, p2, p3, p4, p5, p6])
    db.session.commit()

    return('Data populated')


# These two lines should always be at the end of the main.py file.
# Meaning: only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


