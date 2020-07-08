from datetime import datetime
from application.models import Message
import time
import threading


class MessageReader(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, name='MessageReader'):
        """ constructor, setting initial variables """
        self._stopevent = threading.Event()
        self._sleepperiod = 1.0
        threading.Thread.__init__(self, name=name)

    # Adding the stopping mechanism to join this thread
    def join(self, timeout=None):
        """ Stop the thread and wait for it to end. """
        self._stopevent.set()
        threading.Thread.join(self, timeout)

    # Infinitely listen for messages in DB and print
    def run(self):
        print("MessageReader Started!")
        while not self._stopevent.isSet():
            print_and_delete_messages()
            time.sleep(1)
        print("MessageReader Stopped!")


def print_and_delete_messages():
    # Get all messages from the database
    messages = Message.query.all()

    for message in messages:
        # Print the message on console if current datetime is more
        # than the time the message was supposed to be delivered
        if message.time < datetime.now():
            print(message.content)
            # Remove the message from database
            message.delete()
