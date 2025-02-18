from flask import Flask, jsonify
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

# Debugging: Print config values to confirm it's set
print("Final DATABASE URI in Flask config:", app.config.get("SQLALCHEMY_DATABASE_URI"))

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})  # Allow React frontend

# Register Flask-Migrate
migrate = Migrate(app, db)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")


@app.route('/')
def home():
    return jsonify({"message": "Task Manager API is running!"}), 200


if __name__ == '__main__':
    app.run(debug=True)