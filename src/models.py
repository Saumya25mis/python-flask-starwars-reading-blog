
# IMPORTANT: run 'URL/populate' to populate database for testing purposes

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# For each 'model` I have to declare a class with the model properties 
# and a method `serialize` that returns a dictionary representation of the class

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False, default=True)

    favorites = db.relationship('Favorite', backref='user', lazy=True) # One to Many

    # What does db.relationship() do? 
    # That function returns a new property that can do multiple things. 
    # In this case, it points to the Favorite class and loads multiple of those. 
    # How does it know that this will return more than one favorite? (One-to-Many)
    # Because SQLAlchemy guesses a useful default from the declaration. 
    # For a One-to-One relationship we can pass 'uselist=False' to relationship().

    # What do backref and lazy mean? 
    # backref is a simple way to declare a new property on the Character or Planet class. 
    # lazy defines when SQLAlchemy will load the data from the database. 
    # By default, SQLAlchemy will load the data as necessary in one go using a standard select statement.


    # __repr__():  tell python how to print the class object in the console
    def __repr__(self):
        return '<User: %r>' % self.username

    # serialize(): tell python how convert the class object into a dictionary ready to jsonify
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    

class Favorite(db.Model):
    __tablename__ = "favorite"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, unique=False, nullable=False) # store character_id or planet_id
    item_type = db.Column(db.String(80), unique=False, nullable=False) # type can be Character or Planet
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "item_id": self.item_id, 
            "item_type": self.item_type
        }


class Character(db.Model):
    __tablename__ = "character"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    birth_year = db.Column(db.String(50), unique=False, nullable=False)
    gender = db.Column(db.String(50), unique=False, nullable=False)
    height = db.Column(db.Float, unique=False, nullable=False)
    eye_color = db.Column(db.String(50), unique=False, nullable=False)
    hair_color = db.Column(db.String(50), unique=False, nullable=False)
    skin_color = db.Column(db.String(50), unique=False, nullable=False)
    item_type = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return '<Character: %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "item_type": self.item_type
        }


class Planet(db.Model):
    __tablename__ = "planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=False)
    terrain = db.Column(db.String(50), unique=False, nullable=False)
    diameter = db.Column(db.Float, unique=False, nullable=False)
    climate = db.Column(db.String(50), unique=False, nullable=False)
    rotation_period = db.Column(db.Float, unique=False, nullable=False)
    item_type = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return '<Planet: %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
            "diameter": self.diameter,
            "climate": self.climate,
            "rotation_period": self.rotation_period,
            "item_type": self.item_type
        }
    

    