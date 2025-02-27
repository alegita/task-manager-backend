from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from config.config import Config
from app.models import db, bcrypt  # Updated import path
from app.routes.auth_routes import auth_bp  # Updated import path
import os
from dotenv import load_dotenv
from app.routes.task_routes import task_routes

# Load environment variables
load_dotenv()

# Initialize extensions
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions with app
    db.init_app(app)  
    bcrypt.init_app(app)
    jwt.init_app(app)  # Now properly initialized
    migrate.init_app(app, db)  # Now properly initialized
    
    # Set up CORS
    CORS(app, origins="http://localhost:5173", 
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], 
     allow_headers=["Authorization", "Content-Type"], 
     supports_credentials=True)
    
    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(task_routes, url_prefix="/api")

    @app.route('/')
    def home():
        return jsonify({"message": "Task Manager API is running!"}), 200
    
    return app