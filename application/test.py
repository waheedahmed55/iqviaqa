from . import db
from . import api_server
from . import reader
import unittest
import json
import io
import sys
import time


class ApiTest(unittest.TestCase):

    def setUp(self):
        # Print the name of the test
        print("Running test: ", self._testMethodName)
        # Start the test API
        self.app = api_server().test_client()
        # Define a good payload
        self.payload = json.dumps({
            "content": "Test message 1",
            "time": "07/07/2020 22:35:00"
        })

    def tearDown(self):
        # Clear the database after each test
        db.drop_all()

    def test_successful_create_message(self):

        # When we send message with good payload
        response = self.app.post(
            '/messages', headers={"Content-Type": "application/json"}, data=self.payload)

        # Then we should recieve 202 success response with details of created message
        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(202, response.status_code)

    def test_successful_get_messages(self):
        # When we POST a message and GET the messages
        self.app.post(
            '/messages', headers={"Content-Type": "application/json"}, data=self.payload)
        response = self.app.get(
            '/messages', headers={"Content-Type": "application/json"})

        # Then we should see the POSTed message in the GET response
        self.assertEqual([{'time': '2020-07-07T22:35:00',
                           'content': 'Test message 1', 'id': 1}], response.json)
        self.assertEqual(200, response.status_code)

    def test_missing_values(self):
        # Given
        bad_payload = json.dumps({
            "time": "07/07/2020 22:35:00"
        })

        # When I POST a message that's missing "content"
        response = self.app.post(
            '/messages', headers={"Content-Type": "application/json"}, data=bad_payload)

        # Then I should receive an error
        self.assertEqual("INVALID_REQUEST", response.json['status'])
        self.assertEqual(400, response.status_code)

    def test_invalid_date(self):
        # Given
        bad_payload = json.dumps({
            "content": "Valid message",
            "time": "07/07/20200 22:35:00"
        })

        # When I POST a message with invalid date
        response = self.app.post(
            '/messages', headers={"Content-Type": "application/json"}, data=bad_payload)

        # Then I should receive an error
        self.assertEqual("INVALID_DATE", response.json['status'])
        self.assertEqual(400, response.status_code)

    def test_reader(self):

        # To test the reader, we wish to capture console output
        capturedOutput = io.StringIO()                  # Create StringIO object
        sys.stdout = capturedOutput                     # and redirect stdout.

        # When I Add a good message with date and time less than today
        self.app.post(
            '/messages', headers={"Content-Type": "application/json"}, data=self.payload)

        # And call function that reads and prints messages
        reader.print_and_delete_messages()
        sys.stdout = sys.__stdout__                     # Reset redirect.

        # Then I should see the message on console
        self.assertEqual("Test message 1\n", capturedOutput.getvalue())


if __name__ == '__main__':
    unittest.main()
