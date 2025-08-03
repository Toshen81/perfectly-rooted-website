from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class FormSubmission(db.Model):
    __tablename__ = 'form_submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    form_type = db.Column(db.String(50), nullable=False)  # 'consultation', 'package', etc.
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(100), nullable=True)
    interest = db.Column(db.String(100), nullable=True)  # area of interest or package type
    message = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    submission_data = db.Column(db.Text, nullable=True)  # JSON string of all form data
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<FormSubmission {self.id}: {self.name} - {self.form_type}>'
