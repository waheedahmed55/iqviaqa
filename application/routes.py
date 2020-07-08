from application.models import MessageSchema
from application.models import Message
from flask import current_app as app
from flask import request, Response
from flask_restful import Api, Resource
from datetime import datetime
import json

message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)

# Here we define our REST API endpoints and implementations


class MessageListResource(Resource):
    # GET /messages to list current messages in the DB
    def get(self):
        # Retrieve all messages from the database
        messages = Message.query.all()
        return messages_schema.dump(messages)

    # POST /messages to create a message in the DB
    def post(self):
        try:
            new_message = Message(
                # Reading the content from JSON request
                content=request.json['content'],
                # Reasing the datetime from the JSON request
                time=datetime.strptime(
                    request.json['time'], '%m/%d/%Y %H:%M:%S')
            )
            # Saving the message in DB
            new_message.save()
            return Response(json.dumps(message_schema.dump(new_message)), status=202, mimetype='application/json')
        except KeyError:
            # Handle exception when request is missing required keys
            return Response(json.dumps({"status": "INVALID_REQUEST"}), status=400, mimetype='application/json')
        except ValueError:
            # Handle exception when request has invaid date format
            return Response(json.dumps({"status": "INVALID_DATE"}), status=400, mimetype='application/json')


api = Api(app)
# Register the resource
api.add_resource(MessageListResource, '/messages')
