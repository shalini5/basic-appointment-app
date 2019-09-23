# services/notable/project/api/models.py

from datetime import datetime

from sqlalchemy.sql import func

from project import db


class Doctor(db.Model):

    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }


class Appointment(db.Model):

    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointment = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(128), nullable=False)
    doctor_id = db.Column(db.ForeignKey("doctors.id"), nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, appointment, type, doctor_id):
        self.appointment = appointment
        self.type = type
        self.doctor_id = doctor_id

    def to_json(self):
        return {
            'id': self.id,
            'appointment': self.appointment.strftime("%m/%d/%Y, %H:%M:%S"),
            'type': self.type,
            'doctor': self.doctor_id,
        }
