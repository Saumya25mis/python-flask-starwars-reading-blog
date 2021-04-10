# from models import db, User, Character, Planet, Favorite

# def get_favorite_per_type(fav):
#     if fav.item_type == "planet":
#         planet = Planet.query.get(fav.item_id)
#         return planet.serialize()
#     if fav.item_type == "character":
#         character = Character.query.get(fav.item_id)
#         return character.serialize()
        
#     return None

# class Service():

#     f = get_favorite_per_type

#     def get_favorites(user_id):
        
#         #Verify that user exits
#         user = User.query.get(user_id)
#         if user is None:
#             raise APIException('User not found', status_code=404)

#         #search favorites from the user
#         all_favorites = Favorite.query.all()

#         #turn ids into planet_id or character_id
#         all_favorites = list(map(lambda x: x.f, all_favorites)) 

#         #return entire list (planets and characters)
#         return all_favorites
    
