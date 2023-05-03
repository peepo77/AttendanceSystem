import numpy as np
import dlib
from voicer2 import read_out_message
from scipy.spatial import distance
import face_recognition
from datetime import datetime
import cv2



def recognize_attendance():
    closed_eyes_time = 0
    opened_eyes_time = 0
    face_encodings_known = np.load('encode-data.npy', allow_pickle=True)
    known_faces_data = np.load('known-faces-data.npy', allow_pickle=True)

    def markAttendance(name):
        read_out_message(name + "your attendance has been marked")
        with open('Attendance_Records/IIT_BHU_ECE.csv', 'r+') as f:
            myDataList = f.readlines()
            face_names = []
            for line in myDataList:
                entry = line.split(',')
                face_names.append(entry[0])
            
            if name not in face_names:
                now = datetime.now()
                dtString = now.strftime('%H:%M')
                f.writelines(f'\n{name},{dtString},{datetime.today().strftime("%d-%m-%Y")}')
            



# Example usage:


#  This code reads frames from a video capture device, then performs facial landmark detection using the face_recognition library to detect the locations of the eyes in the face. It then calculates the eye aspect ratio (EAR) for each eye to determine if the eyes are open or closed. If both eyes are closed for a certain duration of time, the program considers the person to be drowsy and takes some action, such as sounding an alarm.
# The code also uses the dlib library to detect faces in the video frame, clear what this is used for as it is not directly related to detecting drowsiness. The dets, scores, and idx variables returned by the detector.run() function are not used in the provided code.

# Note that the code assumes the existence of the get_ear() function, which is not shown in the code snippet.

# Example usage:

    

    cap = cv2.VideoCapture(1)

    while True:
        ret, frame = cap.read()
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_landmarks_list = face_recognition.face_landmarks(rgb_small_frame)
        for face_landmark in face_landmarks_list:
            left_eye = face_landmark['left_eye']
            right_eye = face_landmark['right_eye']
            ear_left = get_ear(left_eye)
            ear_right = get_ear(right_eye)
            closed = ear_left < 0.2 and ear_right < 0.2
            if closed:
                closed_eyes_time += 1
            else:
                opened_eyes_time += 1
            if closed_eyes_time > 1 and opened_eyes_time > 1:
                current_face_locations = face_recognition.face_locations(rgb_small_frame)
                current_face_encodings = face_recognition.face_encodings(rgb_small_frame, current_face_locations)

                detector = dlib.get_frontal_face_detector()
                dets, scores, idx = detector.run(rgb_small_frame, 1, -1)
                count = 1
                for i in scores:
                    Detectionscore = i % 100 * 100
                    dontremovedetectionscore = Detectionscore
                count += 1
                for (top, right, bottom, left), face_encoding in zip(current_face_locations,
                                                                     current_face_encodings):
                    matches = face_recognition.compare_faces(face_encodings_known, face_encoding)
                    faceDis = face_recognition.face_distance(face_encodings_known, face_encoding)
                    matchIndex = np.argmin(faceDis)

                    if matches[matchIndex]:
                        known_faces, face_id = zip(*known_faces_data)
                        name = known_faces[matchIndex]
                        id = face_id[matchIndex]
                        markAttendance(name)
                        
                        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                        top *= 4
                        right *= 4
                        bottom *= 4
                        left *= 4
                    # Draw a Rectangle around the Face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_TRIPLEX
                    if count > 1 and dontremovedetectionscore > 70:
                        dontremovedetectionscore = round(dontremovedetectionscore,1)
                        cv2.putText(frame, name + " " + str(id) + str(dontremovedetectionscore), (left + 3, bottom - 6), font, 1.0, (255, 255, 255), 1)
                    else:
                        cv2.putText(frame, "detection not confident", (left + 3, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # display the frame
        cv2.imshow('Video', frame)
        # wait for 100 milliseconds
        if cv2.waitKey(100) & 0xFF == ord('q'):
            print('exited..\n')
            cap.release()
            cv2.destroyAllWindows()
            break

#function to get EAR of the student
# The get_ear() function calculates the Eye Aspect Ratio (EAR) based on the Euclidean distances between key points in the eye region. The choice of these key points can be optimized based on the specific use case and requirements.

# For example, in this code, the function uses the 6th and 2nd points from the left_eye and right_eye lists, respectively, to calculate the vertical component of the EAR. This might work well for some cases, but might not be optimal for others.

# To choose better parameters, you can experiment with different combinations of key points, and evaluate their performance on a test dataset. Additionally, you can also try using different algorithms for eye detection and landmark extraction, and see how they perform compared to the current method.

# Overall, choosing the best parameters depends on the specific use case and the performance requirements.
def get_ear(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear
