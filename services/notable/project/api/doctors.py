# services/notable/project/api/doctors.py


from flask import Blueprint, request
from flask_restful import Resource, Api

from project import db
from project.api.models import Doctor


doctors_blueprint = Blueprint('doctors', __name__)
api = Api(doctors_blueprint)


class DoctorsPing(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }


class DoctorsList(Resource):
    def post(self):
        post_data = request.get_json()

        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }

        if not post_data:
            return response_object, 400

        name = post_data.get('name')
        email = post_data.get('email')

        try:
            doctor = Doctor.query.filter_by(email=email).first()
            if not doctor:
                db.session.add(Doctor(name=name, email=email))
                db.session.commit()
                response_object['status'] = "success"
                response_object['message'] = f'Doctor {name}, {email} was successfully added!'

                return response_object, 201

            else:
                response_object['message'] = 'Sorry. That doctor already exists.'
                return response_object, 400

        except Exception as e:
            print(f"Error while saving doctor {name}, {email}: {repr(e)}.")
            db.session.rollback()
            return response_object, 400

    def get(self):
        """Get all doctors"""
        response_object = {
            'status': 'success',
            'data': {
                'doctors': [doctor.to_json() for doctor in Doctor.query.all()]
            }
        }
        return response_object, 200


class Doctors(Resource):
    def get(self, doctor_id):
        """Get single doctor details"""
        response_object = {
            'status': 'fail',
            'message': 'Doctor does not exist'
        }
        try:
            doctor = Doctor.query.filter_by(id=int(doctor_id)).first()
            if not doctor:
                return response_object, 404
            else:
                response_object = {
                    'status': 'success',
                    'data': {
                        'id': doctor.id,
                        'name': doctor.name,
                        'email': doctor.email,
                    }
                }
                return response_object, 200
        except ValueError:
            return response_object, 404


api.add_resource(DoctorsPing, '/doctors/ping')
api.add_resource(DoctorsList, '/doctors')
api.add_resource(Doctors, '/doctors/<doctor_id>')
