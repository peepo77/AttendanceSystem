import os
from voicer2 import read_out_message
import BlinkDetect
import Capture
import Trainer


    

####ATTENDANCE STATUS ALSO BEING SHOWN IN THIS FUNCTION WHICH PARSES THE IIT_BHU_ECE.csv FILE AND CHECKS STATUS

def options():
    # os.system('clear')
    os.system('cls')
    # title of the program
    print("\t**********************************************************")
    print("\t $$$$$$ Face Recognition Attendance System- IIT-BHU $$$$$$")
    print("\t**********************************************************")
    print("[1] New User")
    print("[2] Train Image")
    print("[3] Record Attendance")
    print("[4] Check Attendance Status")
    print("[5] Get whole attendance")
    print("[6] Quit")


    while True:
        key = int(input("Enter key: "))
        if key == 5:
            get_attendance()
            break

        elif key == 1:
            CaptureImage()
            break
        elif key == 2:
            TrainImage()
            break
        elif key == 3:
            record_attendance()
            break
        elif key == 4:
            check_attendance()
            break
        elif key == 6:
            print("Pls Don't Forget to Give Feedback to OUR IIT_BHU ATTENDANCE SYSTEM")
            break
        else:
            print("Invalid key. Enter 1-6")
            options()
        # try:
    #     except ValueError:
    #         print("Invalid key. Enter 1-5\n Try Again")
    # exit

def get_attendance():
    password = input("enter your passwprd: ")
    with open('security.txt', 'r+') as f:
        myDataList = f.readlines()
        dt = []
        for line in myDataList:
            entry = line.split(',')
            for passs in entry:

                dt.append(passs)
            
        
        if password not in dt:
            print("Access Forbidden!")
            read_out_message("Try Again!")
        else:
            read_out_message("Here is the list! "+str(len(dt)) +"students attended class!")
            with open('Attendance_Records/IIT_BHU_ECE.csv', 'r+') as f:
                myDataList = f.readlines()
                face_names = []
            for line in myDataList:
                entry = line.split(',')
                face_names.append(entry[0])
                print(entry[0]+"/n")


def record_attendance():
    BlinkDetect.recognize_attendance()
    key = input("Enter any key to return main menu")
    options()


def CaptureImage():
    Capture.capture_image()
    key = input("Enter any key to return main menu")
    options()


def check_attendance():
    name=input("enter your name: ")
    with open('Attendance_Records/IIT_BHU_ECE.csv', 'r+') as f:
        myDataList = f.readlines()
        face_names = []
        for line in myDataList:
            entry = line.split(',')
            face_names.append(entry[0])
        
        if name not in face_names:
            print("Attendance Not Marked!")
            read_out_message(name + "Your Attendance is Not Marked!")
        else:
            print("Attendance Marked!")
            read_out_message(name + "Your Attendance already Marked!")  



def TrainImage():
    Trainer.train_image()
    key = input("Enter any key to return main menu")
    options()

# main driver
options()
