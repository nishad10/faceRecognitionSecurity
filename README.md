# faceRecognitionSecurity
Using pre-built face recognition  models to identify presence of strangers using a camera

Built using face recognition model from here :-

https://github.com/ageitgey/face_recognition

## Installation

Here is a simple installation guide that worked for us (It might change for you depending on what programs/libraries you are missing)

Make sure you go through preparation before moving on to Library/Module installation

### Preparation
1. Make sure you have python v3.0+
2. Make sure you have cmake installed.
3. Make sure you have dlib installed

Depending on your operating system the instructions might vary

For python check out - https://www.python.org/downloads/

For cmake check out - https://cmake.org/install/
> There are precompiled binaries for windows as well as mac/linux that you can download and run to install cmake.

- For pip one thing to keep in mind is your path should be properly setup so that pip is recognized if you face issues try doing this -
`python3 -m pip install` or `python -m pip install` instead of doing `pip install`

For dlib installation do 
` pip install dlib `

Now that we have met all requirements we will download and install all libraries used in the program.

### Libraries/Modules Installation

Use pip3 instead of pip if thats what you have setup for v3.0+

Install face_recognition library
` pip install face_recognition`

Install cv2
`pip install opencv-python`

Install numpy
`pip install numpy`

We have a few other modules imported in the program, these are and should be a part of your standard library and should come installed by default.
If you face any errors after running the above errors please take a look at what library you are missing and refer to docs to intall it using `pip`
