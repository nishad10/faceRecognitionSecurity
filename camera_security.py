import face_recognition
import os
import shutil
import smtplib
import ssl
import cv2
import numpy as np
import time
from PIL import Image, ImageTk
import tkinter.ttk
import tkinter as tk    # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import tkinter.simpledialog


def runProgram():
    window.destroy()
    runSecurity = True


def uploadimage():
    filename = askopenfilename()
    answer = tkinter.simpledialog.askstring("Input", "What is the name of this person?",
                                            parent=window)
    if answer is not None:
        shutil.move(filename, './known_faces/' + answer + '.jpg')
    else:
        print("ERROR MOVING FILE")


def runProgram():
    window.destroy()


def exit():
    window.destroy()
    quit()


########### EMAIL SETTINGS ###########
port = 587  # For starttls
smtp_server = "smtp.gmail.com"
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
        if len(face_recognition.face_encodings(user_image)) > 0:
            user_image_encoding = face_recognition.face_encodings(user_image)[
                0]
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

## Open Window ##
window = tk.Tk()  # Makes main window
window.title("Camera Security")
window.geometry("650x500")
label = tk.Label(text='Most Recent list of known faces',
                 font='Helvetica 12 bold')
label.grid(column=2, row=3, pady=10)
rowCount = 4
columnCount = 1
filenames = os.listdir(directory)
for filename in filenames:
    if filename.endswith(".jpg") or filename.endswith(".png"):
        label = tk.Label(text=filename)
        if columnCount < 5:
            label.grid(column=columnCount, row=rowCount, pady=5)
            columnCount += 1
        else:
            columnCount = 1
            rowCount += 1
            label.grid(column=columnCount, row=rowCount, pady=5)
    else:
        continue
email1 = tk.StringVar()  # Sender Email variable
email2 = tk.StringVar()  # Receiver Email variable
password = tk.StringVar()  # Password variable
shouldEmail = tk.IntVar()  # Should send email notification?

rowCount += 1
label1 = tk.Label(text='Program Settings', font='Helvetica 12 bold')
label1.grid(column=2, row=rowCount, pady=10)
rowCount += 1
tk.Checkbutton(window, text="Send Email Notification",
               variable=shouldEmail).grid(column=1, row=rowCount)
rowCount += 1
label_email = tk.Label(text='Notification Generator Email')
label_email.grid(column=1, row=rowCount, padx=10, pady=5)
label_email1 = tk.Label(text='Notification Receiver Email')
label_email1.grid(column=2, row=rowCount, padx=10, pady=5)
rowCount += 1
widget_email = tk.Entry(window, textvariable=email1, width=25)
widget_email.grid(column=1, row=rowCount, padx=10, pady=5)
widget_email1 = tk.Entry(window, textvariable=email2, width=25)
widget_email1.grid(column=2, row=rowCount, padx=10, pady=5)
rowCount += 1
label_password = tk.Label(text='Password')
label_password.grid(column=1, row=rowCount, padx=10, pady=5)
rowCount += 1
widget2 = tk.Entry(window, show="*", textvariable=password, width=25)
widget2.grid(column=1, row=rowCount, padx=10, pady=5)
rowCount += 1
label3 = tk.Label(text='Main Functions',
                  font='Helvetica 12 bold')
label3.grid(column=2, row=rowCount, pady=10)
rowCount += 1
button1 = tk.Button(window, text="Upload Image", command=uploadimage)
button1.grid(column=1, row=rowCount, padx=5, pady=10)
button2 = tk.Button(window, text="Run Program", command=runProgram)
button2.grid(column=2, row=rowCount, padx=5, pady=10)
button3 = tk.Button(window, text="Exit", command=exit)
button3.grid(column=3, row=rowCount, padx=5, pady=10)
window.mainloop()

if email1 is None:
    email1 = ''
else:
    email1 = email1.get()
if email2 is None:
    email2 = ''
else:
    email2 = email2.get()
if password is None:
    password = ''
else:
    password = password.get()
if shouldEmail is None:
    shouldEmail = False
else:
    shouldEmail = True if shouldEmail.get() == 1 else False

while True:

    # Send an email only if 1 minute has elapsed since last time you sent an email
    sendEmail = time.time() - emailSentTime > 30  # seconds

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
                if sendEmail is True and shouldEmail is True:
                    emailSentTime = time.time()  # Update last email sent time
                    # Send email alert
                    context = ssl.create_default_context()
                    with smtplib.SMTP(smtp_server, port) as server:
                        server.starttls(context=context)
                        server.login(email1, password)
                        server.sendmail(email1, email2, message)

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
