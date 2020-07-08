# QA home challenge

## Setup

1. Install latest python https://www.python.org/downloads/
2. Clone this repository
3. Initialize & Activate the environment

   `python -m venv env`

   On linux:
   `source env/bin/activate`

   On Windows:
   `env\Scripts\activate.bat`

4. Install the requirements

   `pip install -r requirements.txt`

## Running the application

To run the application execute the below command

`python run.py`

### Sample output

```text
127.0.0.1 - - [08/Jul/2020 16:54:47] "POST /messages HTTP/1.1" 202 -
127.0.0.1 - - [08/Jul/2020 16:56:14] "GET /messages HTTP/1.1" 200 -
This is a message
127.0.0.1 - - [08/Jul/2020 16:56:41] "GET /messages HTTP/1.1" 200 -
Closing MessageReader
MessageReader Stopped!
Shutting down API
```

## Running the tests

To run the tests execute the below command

`python -m unittest`

### Sample Output

```text
Running test:  test_invalid_date
Running test:  test_missing_values
Running test:  test_reader
Running test:  test_successful_create_message
Running test:  test_successful_get_messages

-------------------------
Ran 5 tests in 1.584s

OK
```

## REST API

### Create a message

> POST /messages

#### Request

```json
{
  "content": "This is a message",
  "time": "08/07/2020 15:08:00"
}
```

#### Response

```json
{
  "content": "This is a message",
  "time": "2020-08-07T15:08:00",
  "id": 1
}
```

### See all the messages

> GET /messages

#### Response

```json
[
  {
    "content": "POSTMAN Test message",
    "time": "2020-08-07T15:08:00",
    "id": 1
  },
  {
    "content": "This is a message",
    "time": "2020-08-07T15:08:00",
    "id": 2
  }
]
```

## Architecture

Python is used along with

- lightweight Flask freamework to orchestrate the REST API
- SQLAlchemy and Mashmallow used to define DB models and interact with database
- Two threads are created by the main application:
  - One starts the REST API
  - The other starts the application that listens to database for all the messages and displays messages if the time is past current time

SQLite database bundled with Python is used for simplicity

## File structure

- run.py : Contains code that starts the both the threads discussed above
- requirements.txt - Contains all the application dependencies
- application
  - \_\_init\_\_.py : Initializes database and the flask app
  - models.py : Defined the messages model and save, delete operations on it.
  - routes.py : Defines and implements all the REST endpoints
  - reader.py : A stoppable thread, that runs the MessageReader. This listens to database for any new messages. Messages whose time is past current time are displayed on console and removed from the database.
  - test.py - Python's unittest based tests for the application. Contains tests to test all REST endpoints and the MessageReader.
