#User
from flask import jsonify, request, Blueprint
from models import db, User
from werkzeug.security import generate_password_hash

user_bp = Blueprint("user_bp", __name__)

# Fetch all Users
@user_bp.route("/users")
def fetch_users ():
    users = User.query.all()
    user_list = []

    for user in users:
        user_list.append({
            'id':user.id,
            'username':user.username,
            'email':user.email,
            'is_admin':user.is_admin,
            "sports":[
                {
                    "id":sport.id,
                    "name":sport.name,
                    "type":sport.type,
                    "description":sport.description
                }
                for sport in user.sports
            ]

        })
    return jsonify(user_list)

# Fetch One User
@user_bp.route("/users/<int:user_id>", methods=["GET"])
def fetch_user(user_id):
   
    user = User.query.get(user_id) 
    if user:
        
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email
        }), 200
    else:
        
        return jsonify({"error": "User not found"}), 404


# Add users
@user_bp.route("/users", methods=["POST"])
def add_users():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password =  generate_password_hash(data['password'])


    check_username = User.query.filter_by(username=username).first()
    check_email= User.query.filter_by(email=email).first()

    print ("Username",check_username)
    print ("Email",check_email)
    if check_username or check_email:
        return jsonify({"error":"Username/email exists"}), 200

    else:
        new_user = User(username=username,email=email,password=password) 
        db.session.add(new_user)
        db.session.commit()   
        return jsonify({"success":["User added successfully"]}), 201

# Update Users
@user_bp.route("/users/<int:user_id>", methods=["PATCH"])
def update_users(user_id):
    user = User.query.get(user_id)

    if user:
        data = request.get_json()
        username = data.get('username', user.username)
        email = data.get('email', user.email)
        password = data.get('password', user.password)

        check_username = User.query.filter_by(username=username and id!= user.id ).first()
        check_email= User.query.filter_by(email=email and id!= user.id).first()

        if check_username or check_email:
            return jsonify({"error":"Username/email exists"}), 200

        else:
            user.username=username
            user.email=email
            user.password=password
            db.session.commit()   
            return jsonify({"success":["User updated successfully"]}), 201

    else:
        return jsonify({"error":["User doesn't exists"]}), 200

#Delete Users
@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_users(user_id):
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"success":["User deleted successfully"]}), 200

    else:
        return jsonify({"error":["The user you are trying to delete doesn't exists"]}), 406
