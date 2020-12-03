import face_recognition
import os
import shutil
import smtplib
import ssl
import cv2
import numpy as np
import time

# from tkinter import Tk     # from tkinter import Tk for Python 3.x
#from tkinter.filedialog import askopenfilename

########### EMAIL SETTINGS ###########
port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "nishad10dev@gmail.com"
receiver_email = "nishad.aherrao10@gmail.com"
password = input("Type your password and press enter:")
message = """\
Subject: Face Recognition Security Alert

ALERT!! UNKNOWN FACE FOUND!"""

# Get video from webcam
video_capture = cv2.VideoCapture(0)

known_face_encodings = []
known_face_names = []
directory = './known_faces'

# Load all list of known faces
for filename in os.listdir(directory):
    oldfilename = filename
    filename = './known_faces/' + filename
    if filename.endswith(".jpg") or filename.endswith(".png"):
        user_image = face_recognition.load_image_file(filename)
        user_image_encoding = face_recognition.face_encodings(user_image)[0]
        known_face_encodings.append(user_image_encoding)
        known_face_names.append(oldfilename)
    else:
        continue

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
sendEmail = True
emailSentTime = time.time()

while True:

    # Send an email only if 1 minute has elapsed since last time you sent an email
    sendEmail = time.time() - emailSentTime > 60  # seconds

    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding)
            name = "Unknown"
            if True in matches:
                # This means theres a known face so its ok
                print(
                    'Ignoring alert as known face is in picture')
            if True not in matches:
                # This means theres all unknown faces in picture
                print('ALERT!! UNKNOWN FACE FOUND!')
                if sendEmail:
                    emailSentTime = time.time()  # Update last email sent time
                    # Send email alert
                    context = ssl.create_default_context()
                    with smtplib.SMTP(smtp_server, port) as server:
                        server.starttls(context=context)
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, message)

            # Get the face names based on distance to closest recognizable face
            face_distances = face_recognition.face_distance(
                known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            face_names.append(name)
    process_this_frame = not process_this_frame

    # Display the results
    try:
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Draw a box around the face
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        font, 1.0, (255, 255, 255), 1)
    finally:
        # Display the resulting image
        cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
