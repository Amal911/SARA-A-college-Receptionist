import cv2, time
import pickle
import face_recognition
from datetime import datetime
from face_recognition.face_recognition_cli import image_files_in_folder
import cv2



def predict(img_path, knn_clf=None, model_path=None, threshold=0.6):  # 6 needs 40+ accuracy, 4 needs 60+ accuracy
    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")
    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open("sara_app/model/trained_knn_model.xml", 'rb') as f:
            knn_clf = pickle.load(f)
    # Load image file and find face locations
    img = img_path
    face_box = face_recognition.face_locations(img)
    # If no faces are found in the image, return an empty result.
    if len(face_box) == 0:
        return []
    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(img, known_face_locations=face_box)
    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=2)
    matches = [closest_distances[0][i][0] <= threshold for i in range(len(face_box))]
    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in
            zip(knn_clf.predict(faces_encodings), face_box, matches
                )]

def recognise():
    webcam = cv2.VideoCapture(0)
    while True:
        # Loop until the camera is working
        rval = False
        while (not rval):
            # Put the image from the webcam into 'frame'
            (rval, frame) = webcam.read()
            if (not rval):
                print("Failed to open webcam. Trying again...")

        frame = cv2.flip(frame, 1)  # 0 = horizontal ,1 = vertical , -1 = both
        frame_copy = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        frame_copy = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB)
        predictions = predict(frame_copy, model_path="")

        for name, (top, right, bottom, left) in predictions:
            # webcam.release()
            # cv2.destroyAllWindows()
            return name

# speech_recognition

import speech_recognition
import pyttsx3 as tts
recognizer = speech_recognition.Recognizer()

speaker= tts.init()
speaker.setProperty('rate',150)
def audio():
    global recognizer
    while True:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                recognizer.dynamic_energy_threshold = None
                print("listening...")
                audio = recognizer.listen(mic,timeout=2, phrase_time_limit=6)
                message = recognizer.recognize_google(audio)
                # message = recognizer.recognize_google(audio,language='en-IN',show_all=True)
                message = message.lower()
                # speaker.say(message)
                # speaker.runAndWait()
                print(message)
                return message

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
        except speech_recognition.WaitTimeoutError as k:
            print("time out")



import math
from sklearn import neighbors
import os
import os.path
import pickle

from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import numpy as np

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def train(train_dir, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False):
    # The training data would be all the face encodings from all the known images and the labels are their names
    encodings = []
    names = []

    # Training directory

    train_dir = os.listdir('Faculty_Images/')
    print(train_dir)

    # Loop through each person in the training directory
    for person in train_dir:
        pix = os.listdir("Faculty_Images/" + person)

        # Loop through each training image for the current person
        for person_img in pix:
            # Get the face encodings for the face in each image file
            print("Faculty_Images/" + person + "/" + person_img)
            face = face_recognition.load_image_file("Faculty_Images/" + person + "/" + person_img)
            print(face.shape)
            # Assume the whole image is the location of the face
            # height, width, _ = face.shape
            # location is in css order - top, right, bottom, left
            height, width, _ = face.shape
            face_location = (0, width, height, 0)
            print(width, height)

            face_enc = face_recognition.face_encodings(face)

            face_enc = np.array(face_enc)
            face_enc = face_enc.flatten()

            # Add face encoding for current image with corresponding label (name) to the training data
            encodings.append(face_enc)
            names.append(person)

    print(np.array(encodings).shape)
    print(np.array(names).shape)
    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(encodings, names)

    # Save the trained KNN classifier
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    return knn_clf


def face_train():
    # STEP 1: Train the KNN classifier and save it to disk
    # Once the model is trained and saved, you can skip this step next time.
    print("Training KNN classifier...")
    classifier = train("dataset", model_save_path="sara_app/model/trained_knn_model.xml", n_neighbors=2)
    print("Training complete!")




