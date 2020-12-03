from PIL import Image
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import face_recognition
import os
import shutil

# Load the jpg file into a numpy array
user_image = face_recognition.load_image_file("./known_faces/nishad.jpg")
unknown_image = face_recognition.load_image_file(
    "./unknown_faces/nishad_stranger.jpg")

# Known user face encoding
user_encoding = face_recognition.face_encodings(user_image)[0]
known_faces_encoding = [user_encoding]

# Unknown faces in picture
face_locations = face_recognition.face_locations(unknown_image)
face_encodings = face_recognition.face_encodings(
    unknown_image, face_locations)

# Check image
results = []
for face_encoding in face_encodings:
    # See if the face is a match for the known face(s)
    result = face_recognition.compare_faces(
        known_faces_encoding, face_encoding)
    results.append(result)

results = [item for sublist in results for item in sublist]
print(results)
###############################
# Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
# show an "Open" dialog box and return the path to the selected file
#filename = askopenfilename()
#user_name = 'nishad'
#shutil.move(filename, './known_faces/' + user_name + '.jpg')
#############################
if False in results:
    # This means there is unknown face in our picture
    if True in results:
        # This means theres a known face as well as a unknown face so its ok
        print('Ignoring alert as unknown face is accompanied by known face.')
    if True not in results:
        # This means theres all unknown faces in picture
        print('ALERT!! UNKNOWN FACE FOUND!')
else:
    # This means all known faces in picture
    print('Hello! This will not be alerted')
