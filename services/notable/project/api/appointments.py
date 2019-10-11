# services/notable/project/api/appointments.py

from datetime import datetime

from flask import Blueprint, request
from flask_restful import Resource, Api

from project.api.models import Appointment, Doctor
from project import db


appt_blueprint = Blueprint('appointments', __name__)
api = Api(appt_blueprint)

ACCEPTABLE_SLOTS_MINUTES = ['00', '15', '30', '45']


def validate_date(date_text):
    if not date_text:
        return False

    try:
        if date_text != datetime.strptime(date_text, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S'):
            raise ValueError
        return True
    except ValueError:
        return False


class AppointmentAdd(Resource):
    def post(self):
        """Add a new appointment"""
        post_data = request.get_json()

        if not post_data:
            return {
                'status': 'fail',
                'message': 'Invalid payload.'
            }, 400

        # Slot expected in format '09/22/2019, 15:52:32'
        slot = post_data.get('appointment')
        doctor_id = post_data.get('doctor_id')
        appt_type = post_data.get('type')

        # Validate the date format
        if not validate_date(slot):
            return {
                'status': 'fail',
                'message': 'Invalid date format, please enter appointment slot in format YYYY-MM-DD hh:mm:ss.'
            }, 400

        try:
            # Time check
            dt_obj = datetime.strptime(slot, "%Y-%m-%d %H:%M:%S")
            year = dt_obj.strftime("%Y")
            month = dt_obj.strftime("%m")
            day = dt_obj.strftime("%d")
            hh = dt_obj.strftime("%H")
            mm = dt_obj.strftime("%M")

            if mm not in ACCEPTABLE_SLOTS_MINUTES:
                return {
                    'status': 'fail',
                    'message': 'Invalid time slot, minutes can only be 00,15,30 or 45.'
                }, 400

            # Check if doctor has quota
            requested_slot = datetime(int(year), int(month), int(day), int(hh), int(mm))
            cur_appointments = Appointment.query.filter_by(
                doctor_id=int(doctor_id),
                appointment=requested_slot
            ).count()

            if cur_appointments == 3:
                return {
                    'status': 'fail',
                    'message': 'This slot is not available.'
                }, 400

            if cur_appointments < 3:
                db.session.add(Appointment(appointment=requested_slot, doctor_id=doctor_id, type=appt_type))
                db.session.commit()
                return {
                    'status': "success",
                    'message': f"Appointment at {requested_slot} was added successfully!"
                }, 201

            else:
                return {
                    'status': 'fail',
                    'message': 'This slot is not available.'
                }, 400

        except Exception as e:
            print(f'Post failed with error {e}')
            db.session.rollback()
            return {
                'status': 'fail',
                'message': 'Invalid payload.'
            }, 400


class AppointmentsGet(Resource):
    def get(self, doctor_id):
        """Get all appointments for a given doctor id"""
        response_object = {
            'status': 'fail',
            'message': f'Appointment(s) do not exist for doctor {doctor_id}'
        }
        try:
            appointments = Appointment.query.filter_by(doctor_id=int(doctor_id)).all()
            response_object = {
                'status': 'success',
                'data': {
                    'appointments': [appt.to_json() for appt in appointments]
                }
            }
            return response_object, 200

        except ValueError:
            return response_object, 404


class AppointmentDelete(Resource):
    def delete(self, id):
        """Given an appt id, if exists delete it"""
        try:
            appt = Appointment.query.filter_by(id=int(id)).first()
            if not appt:
                return {
                    'status': 'fail',
                    'message': 'No appt found'
                }, 404
            db.session.delete(appt)
            db.session.commit()
            return {
               'status': "success",
               'message': f"Appointment {id} was deleted successfully!"
            }, 200

        except Exception as e:
            print(f'Deleting appointment failed with error {e}')
            return {
                'status': 'fail',
                'message': 'Invalid payload.'
            }, 400


api.add_resource(AppointmentAdd, '/appointments')
api.add_resource(AppointmentsGet, '/appointments/<doctor_id>')
api.add_resource(AppointmentDelete, '/appointments/<id>')
