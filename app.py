from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import User, Sport, db, TokenBlocklist
from flask_jwt_extended import JWTManager
from datetime import timedelta
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sports.db'
migrate = Migrate(app, db)
db.init_app(app)

# jwt
app.config["JWT_SECRET_KEY"] = "asdfghjkl"  
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours = 60)
jwt = JWTManager(app)
jwt.init_app(app)

# Importing all functions in views
from views import *

app.register_blueprint(user_bp)
app.register_blueprint(sport_bp)
app.register_blueprint(auth_bp)

# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None
