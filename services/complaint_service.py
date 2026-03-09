from models.complaint import Complaint
from models import db
def create_complaint(data):
    complaint = Complaint(**data)
    db.session.add(complaint)
    db.session.commit()
    return complaint