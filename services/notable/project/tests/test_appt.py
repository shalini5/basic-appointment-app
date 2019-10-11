# services/notable/project/tests/test_appt.py

from datetime import datetime
import json

from project.tests.base import BaseTestCase
from project import db
from project.api.models import Doctor, Appointment


def add_appointment(appointment, type, doctor_id):
    appt = Appointment(appointment=appointment, type=type, doctor_id=doctor_id)
    db.session.add(appt)
    db.session.commit()
    return appt


def add_doctor(name, email):
    doctor = Doctor(name=name, email=email)
    db.session.add(doctor)
    db.session.commit()
    return doctor


class TestApptService(BaseTestCase):
    """Tests for the Appt Service."""

    def test_add_appt(self):
        doctor = add_doctor('michael', 'michael@gmail.com')
        """Ensure a new appt can be added to the database."""
        with self.client:
            response = self.client.post(
                '/appointments',
                data=json.dumps(
                    {
                        "appointment": datetime(2019, 9, 22, 15, 0).strftime("%Y-%m-%d %H:%M:%S"),
                        "doctor_id": doctor.id,
                        "type": "follow up"
                    }
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])

    def test_add_appt_wrong_time(self):
        doctor = add_doctor('michael', 'michael@gmail.com')
        """Ensure a new appt can be added to the database."""
        with self.client:
            response = self.client.post(
                '/appointments',
                data=json.dumps(
                    {
                        "appointment": datetime(2019, 9, 22, 18, 0).strftime("%Y-%m-%d %H:%M:%S"),
                        "doctor_id": doctor.id,
                        "type": "follow up"
                    }
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])

    def test_add_appt_three_appt(self):
        """Ensure a new appt can be added to the database."""
        doctor = add_doctor('michael', 'michael@gmail.com')
        slot = datetime(2019, 9, 22, 15, 45)
        for i in range(3):
            appointment = add_appointment(slot, "new_patient", doctor.id)
        with self.client:
            response = self.client.post(
                '/appointments',
                data=json.dumps(
                    {
                        "appointment": datetime(2019, 9, 22, 15, 45).strftime("%Y-%m-%d %H:%M:%S"),
                        "doctor_id": doctor.id,
                        "type": "follow up"
                    }
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('This slot is not available.', data['message'])

    def test_delete(self):
        """"Ensure delete appt works"""
        slot = datetime(2019, 9, 22, 15, 45)
        doctor = add_doctor('michael', 'michael@gmail.com')
        appointment = add_appointment(slot, "follow up", doctor.id)
        with self.client:
            response = self.client.delete(f'/appointments/{appointment.id}')
            self.assertEqual(response.status_code, 200)

    def test_single_appointment(self):
        """Ensure get single appointment behaves correctly."""
        slot = datetime(2019, 9, 22, 15, 45)
        doctor = add_doctor('michael', 'michael@gmail.com')
        appointment = add_appointment(slot, "new_patient", doctor.id)
        with self.client:
            response = self.client.get(f'/appointments/{doctor.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)

    def test_add_appt_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/appointments',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_appt_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a required key.
        """
        with self.client:
            response = self.client.post(
                '/appointments',
                data=json.dumps({'type': 'follow up'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid date format, please enter appointment slot in format YYYY-MM-DD hh:mm:ss.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_appt_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/appointments/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Appointment(s) do not exist for doctor blah', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_appt_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/appointments/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual([], data['data']['appointments'])
            print(data)
            self.assertIn('success', data['status'])

