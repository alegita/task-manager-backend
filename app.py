from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from models import db, bcrypt
from routes.auth_routes import auth_bp
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
#CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})  # Allow React frontend

CORS(app, origins="http://localhost:5173", methods=["GET", "POST", "OPTIONS"], allow_headers=["Authorization", "Content-Type"], supports_credentials=True)

@app.before_request
def handle_preflight():
    """Handle CORS preflight requests (OPTIONS) manually."""
    if request.method == "OPTIONS":
        response = jsonify({"message": "CORS preflight successful"})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Authorization, Content-Type")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response, 200

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)


# Register Flask-Migrate
migrate = Migrate(app, db)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")


@app.route('/')
def home():
    return jsonify({"message": "Task Manager API is running!"}), 200


if __name__ == '__main__':
    app.run(debug=True)