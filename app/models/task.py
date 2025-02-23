from app.models import db
from datetime import datetime
from app.models.user import User

class Task(db.Model):
    __tablename__ = "tasks"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.String(20), default="medium")  # "low", "medium", "high"
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Reference the 'users' table

    user = db.relationship("User", back_populates="tasks")  # ✅ Defines relationship

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "priority": self.priority,
            "user_id": self.user_id
        }