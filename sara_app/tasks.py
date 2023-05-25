import cv2
from celery import *
import os

from sara_chatbot.celery import app

# app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
#                 CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])
celery = Celery('tasks', broker='amqp://guest@localhost/http://127.0.0.1:8000/')

@shared_task
def capture_frames():
    # Open the camera
    cap = cv2.VideoCapture(0)

    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()

        if ret:
            # Process the frame here
            # ...

            # Display the frame (optional)
            cv2.imshow('frame', frame)
            cv2.waitKey(1)

    # Release the camera
    cap.release()
    cv2.destroyAllWindows()
