
from flask import jsonify, request, Blueprint
from models import db, User, TokenBlocklist
from werkzeug.security import check_password_hash
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

auth_bp = Blueprint("auth_bp", __name__)

# Login
@auth_bp.route("/login", methods = ["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email = email).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity = user.id)
        return jsonify({"access_token":access_token}),200

    else:
        return jsonify({"error":"Either email or password does not exist or is incorrect"}),404 

#How to get the details of the currently logged in user
@auth_bp.route("/current_user", methods = ["GET"])
@jwt_required()
def current_user():
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)

    user_data = {
            'id':user.id,
            'email':user.email,
            'username':user.username
        }

    return jsonify(user_data)


# Logout
@auth_bp.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify({"Success":"Logged out successfully"})