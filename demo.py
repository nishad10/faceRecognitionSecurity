from PIL import Image
import face_recognition

# Load the jpg file into a numpy array
user_image = face_recognition.load_image_file("./known_faces/obama.jpg")
unknown_image = face_recognition.load_image_file("./unknown_faces/obama.jpg")

user_encoding = face_recognition.face_encodings(user_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

known_faces_encoding = [user_encoding]

results = face_recognition.compare_faces(
    known_faces_encoding, unknown_encoding)

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
