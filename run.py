from app import create_app, db

app = create_app()

if __name__ == "__main__":
    with app.app_context():  # Ensures Flask app context is active
        db.create_all()
    app.run(debug=True)

