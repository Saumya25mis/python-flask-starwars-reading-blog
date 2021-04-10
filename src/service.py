from flask import jsonify
from models import db, User, Character, Planet, Favorite

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Service:

    def get_favorite_per_type(fav):

        print(bcolors.WARNING + str(fav) + bcolors.ENDC)

        if fav.item_type == "planet":
            planet = Planet.query.get(fav.item_id)
            return planet.serialize()
        if fav.item_type == "character":
            character = Character.query.get(fav.item_id)
            return character.serialize()
        return None

    def get_favorites(user_id):
        
        #Verify that user exits
        user = User.query.get(user_id)
        if user is None:
            raise APIException('User not found', status_code=404)

        #search favorites from the user
        all_favorites = Favorite.query.all()

        #turn ids into planet_id or character_id
        all_favorites = list(map(lambda x: Service.get_favorite_per_type(x), all_favorites)) 

        #return entire list (planets and characters)
        return all_favorites
    
