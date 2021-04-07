from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
    def get_all_users():
        all_users = User.query.all()
        all_users = list(map(lambda x: x.serialize(), all_users)) 
        return all_users
    
    def get_user(id):
        user = User.query.get(id).serialize()
        return user
    
    def delete_user(id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
    

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

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color
        }

    def get_all_characters():
        all_characters = Character.query.all()
        all_characters = list(map(lambda x: x.serialize(), all_characters)) 
        return all_characters

    def get_character(id):
        character = Character.query.get(id).serialize()
        return character

    def delete_character(id):
        character = Character.query.get(id)
        db.session.delete(character)
        db.session.commit()

class Planet(db.Model):
    __tablename__ = "planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=False)
    terrain = db.Column(db.String(50), unique=False, nullable=False)
    diameter = db.Column(db.Float, unique=False, nullable=False)
    climate = db.Column(db.String(50), unique=False, nullable=False)
    rotation_period = db.Column(db.Float, unique=False, nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
            "diameter": self.diameter,
            "climate": self.climate,
            "rotation_period": self.rotation_period
        }
    
    def get_all_planets():
        all_planets = Planet.query.all()
        all_planets = list(map(lambda x: x.serialize(), all_planets)) 
        return all_planets
    
    def get_planet(id):
        planet = Planet.query.get(id).serialize()
        return planet

    def delete_planet(id):
        planet = Planet.query.get(id)
        db.session.delete(planet)
        db.session.commit()
    