from datetime import datetime
from . import db
from models import db
import random
class Complaint(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    ticket_id = db.Column(db.String(30), unique=True)

    title = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text, nullable=False)

    department = db.Column(db.String(100), nullable=False)

    status = db.Column(db.String(50), default="Pending")

    priority = db.Column(db.String(20), default="Normal")

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
   

    created_at = db.Column(db.DateTime, default=datetime.utcnow)