# Sports

from flask import jsonify, request, Blueprint
from models import db, User, Sport
from flask_jwt_extended import jwt_required,get_jwt_identity

sport_bp = Blueprint("sport_bp", __name__)

# Fetch all Sports
@sport_bp.route("/sports")
@jwt_required()
def fetch_sports():

    current_user_id = get_jwt_identity()  
    sports = Sport.query.filter_by(user_id= current_user_id)  
    sports_list = []  

    for sport in sports:
        sports_list.append({
            'id': sport.id,
            'name': sport.name,
            'type': sport.type,
            'description': sport.description,
            'user_id': sport.user_id  ,
            "user":{"id":sport.user.id, "username": sport.user.username, "email":sport.user.email}
        })

    return jsonify(sports_list)  

# Fetch One Sport
# @sport_bp.route("/sports/<int:sport_id>", methods=["GET"])
# def fetch_sport(sport_id):
  
#     sport = Sport.query.get(sport_id)  
#     if sport:
      
#         return jsonify({
#             'id': sport.id,
#             'name': sport.name,
#             'type': sport.type,
#             'description': sport.description,
#             'user_id': sport.user_id
#         }), 200
#     else:
       
#         return jsonify({"error": "Sport not found"}), 404


# Add Sport
@sport_bp.route("/sports/add", methods=["POST"])
@jwt_required()
def add_sport():
    data = request.get_json()
    
    current_user_id = get_jwt_identity()  

    name = data['name']
    type = data['type']
    description = data['description']

    new_sport = Sport(name=name, type=type, description=description, user_id=current_user_id)

    db.session.add(new_sport)
    db.session.commit()   

    return jsonify({"success": "Sport added successfully"}), 201


# Update a Sport
@sport_bp.route("/sports/<int:sport_id>", methods=["PATCH"])
@jwt_required() 
def update_sport(sport_id):
    current_user_id = get_jwt_identity()  

    sport = Sport.query.get(sport_id)

    if not sport:
        return jsonify({"error": "Sport with the given ID does not exist"}), 404

    if sport.user_id != current_user_id:
        return jsonify({"error": "You are not authorized to update this sport"}), 403
    
    data = request.get_json()
    
    name = data.get('name', sport.name)  
    type = data.get('type', sport.type) 
    description = data.get('description', sport.description) 

 
    sport.name = name
    sport.type = type
    sport.description = description

    db.session.commit()

    return jsonify({"success": "Sport updated successfully"}), 200

# Delete Sport
@sport_bp.route("/sports/<int:sport_id>", methods=["DELETE"])
@jwt_required()  
def delete_sport(sport_id):

    current_user_id = get_jwt_identity()  

    sport = Sport.query.filter_by(id=sport_id, user_id=current_user_id).first()

    if not sport:
        return jsonify({"error": "Sport not found/You are not authorised to delete this sport"}), 404

    
    db.session.delete(sport)
    db.session.commit()

    return jsonify({"success": "Sport deleted successfully"}), 200
