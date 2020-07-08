from threading import Thread
from application import api_server
from application.reader import MessageReader
import time

if __name__ == '__main__':

    # Initialize the API Thread
    api_process = Thread(target=api_server().run, daemon="True")

    # Initialize the message reader thread
    reader_process = MessageReader()

    # Start the MessageReader that will read and display messages from the database
    reader_process.start()

    # Start our API
    api_process.start()

    # Listed for keyboard interrupt to gracefully end both the threads, Reader and API
    try:
        while 1:
            time.sleep(.1)
    except KeyboardInterrupt:
        print("Closing MessageReader")
        reader_process.join()
        print("Shutting down API")
        exit(0)
