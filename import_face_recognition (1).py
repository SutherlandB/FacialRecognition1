import face_recognition
import picamera
import numpy as np
import os

camera = picamera.PiCamera()
camera.resolution = (320,240)
current = np.empty((240,320,3), dtype=nuint8)

os.chdir("home/pi/face_recognition/examples")
finished = ""
all_names = []
library_faces = []
while True:
    initial_name = input("What is your name? ").strip()
    all_names.append(initial_name)
    ready = input("Press y when youre ready to have your picture taken ")
    
    while len(ready) == 0:
        print("Error! No response given. Try again.")
        ready = input("Press y when you're ready to have your picture taken ")

    while len(ready) > 0:
        if ready == 'y':
            print("Capturing an initial face for comparisons")
            camera.capture("data.jpg")

            print("Loading known face image(s)")
            image = face_recognition.load_image_file("data.jpg", mode="RGB")
            initial_face_encoding = face_recognition.face_encodings(image)[0]
            library_faces.append(initial_face_encoding)
            break
        
        else:
            print("Error! Unknown response given. Try again.")
            ready = input("Are you ready to have your picture taken? ")
    
    while True:
        finished = input("Do you want to add more faces? y or n ")
        if finished == "y":
            break
        elif finished == "n":
            break
        else:
            print("Not a valid response")
    if finished == "n":
        break

face_locations = []
face_encodings = []

flag = False
count = 0
while not flag:
    print("Capturing image.")
    camera.capture(current, format="rgb")

    face_locations = face_recognition.face_locations(current) #a list of new faces
    print("Found {} faces in this current image.".format(len(face_locations)))
    new_face_encodings = face_recognition.face_encodings(current, face_locations) #a list of encodings for the new faces

    for i in new_face_encodings:
        """
        Here we finally match the new face(s) captured against the face(s) we already know, by
        looping over each face object found in the frame
        """
        match = face_recognition.compare_faces(library_faces, i) 
        name = "<Unknown Person>"
        for y in range(0,len(match)):
            if match[y]:
                name = all_names[y]  #update name if face is successfully recognized
                break
        print("I see someone named {}!".format(name))
    count+=1

    if count > 10:
        flag = True
        break