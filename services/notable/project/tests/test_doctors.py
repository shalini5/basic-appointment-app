# services/notable/project/tests/test_doctors.py

import json

from project.tests.base import BaseTestCase
from project import db
from project.api.models import Doctor


def add_doctor(name, email):
    doctor = Doctor(name=name, email=email)
    db.session.add(doctor)
    db.session.commit()
    return doctor


class TestDoctorService(BaseTestCase):
    """Tests for the doctors Service."""

    def test_doctors(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/doctors/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_doctor(self):
        """Ensure a new doctor can be added to the database."""
        with self.client:
            response = self.client.post(
                '/doctors',
                data=json.dumps(
                    {
                        "name": "michael",
                        "email": "michael@gmail.com"
                    }
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('Doctor michael, michael@gmail.com was successfully added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_doctor_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/doctors',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_doctor_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a name key.
        """
        with self.client:
            response = self.client.post(
                '/doctors',
                data=json.dumps({'email': 'michael@gmail.com'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_doctor_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        with self.client:
            self.client.post(
                '/doctors',
                data=json.dumps({
                    'name': 'michael',
                    'email': 'michael@gmail.com'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/doctors',
                data=json.dumps({
                    'name': 'michael',
                    'email': 'michael@gmail.com'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That doctor already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_doctor(self):
        """Ensure get single doctor behaves correctly."""
        doctor = add_doctor('michael', 'michael@gmail.com')
        with self.client:
            response = self.client.get(f'/doctors/{doctor.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('michael', data['data']['name'])
            self.assertIn('michael@gmail.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_doctor_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/doctors/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Doctor does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_doctor_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/doctors/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Doctor does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_doctors(self):
        """Ensure get all doctors behaves correctly."""
        add_doctor('abc', 'abc@gmail.com')
        add_doctor('xyz', 'xyz@gmail.com')
        with self.client:
            response = self.client.get('/doctors')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['doctors']), 2)
            self.assertIn('abc', data['data']['doctors'][0]['name'])
            self.assertIn(
                'abc@gmail.com', data['data']['doctors'][0]['email'])
            self.assertIn('xyz', data['data']['doctors'][1]['name'])
            self.assertIn(
                'xyz@gmail.com', data['data']['doctors'][1]['email'])
            self.assertIn('success', data['status'])
