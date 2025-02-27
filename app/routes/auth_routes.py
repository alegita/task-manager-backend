from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, verify_jwt_in_request, jwt_required, get_jwt_identity
from app.models.user import User
from app.models import db


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    if not data.get("username") or not data.get("password") or not data.get("email"):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400

    new_user = User(username=data["username"], email=data["email"])
    new_user.set_password(data["password"])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200


@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify({"message": f"Access granted to user {current_user_id}"}), 200


@auth_bp.route("/debug_token", methods=["GET"])
@jwt_required()
def debug_token():
    try:
        verify_jwt_in_request()
        identity = get_jwt_identity()
        return jsonify({"user_id": str(identity), "message": "Token is valid!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
