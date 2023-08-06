import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime

path = 'Student_Images'
classNames = os.listdir(path)  # this lists all the files in a directory as an array
Student_names = []
images = []
temp = 0

# Define the time slots for attendance
attendance_slots = {'A1': {'start_time': '19:50:00', 'end_time': '19:52:00'},
                    'A2': {'start_time': '19:53:00', 'end_time': '19:54:00'},
                    'B1': {'start_time': '22:24:00', 'end_time': '22:25:00'},
                    'B2': {'start_time': '22:26:00', 'end_time': '22:27:00'},
                    'C1': {'start_time': '22:28:00', 'end_time': '22:29:00'},
                    'C2': {'start_time': '10:00:00', 'end_time': '11:00:00'}}

# Get the current time
now = datetime.now()
current_time = now.strftime('%H:%M:%S')
current_slot = None

# Check which time slot is currently active
for slot, times in attendance_slots.items():
    if current_time >= times['start_time'] and current_time <= times['end_time']:
        current_slot = slot
        break

if current_slot is None:
    print('No attendance slot is currently active')
    exit()
else:
    classNames = os.listdir(path + '/' + current_slot)
    for i in classNames:
        curImg = cv2.imread(f'{path}/{i}')
        images.append(curImg)
        Student_names.append(os.path.splitext(i)[0])
    print(Student_names)


# Get the images of students for the current attendance slot
slot_images_path = os.path.join(path, current_slot)
if not os.path.exists(slot_images_path):
    print(f'No images found for attendance slot {current_slot}')
    exit()

images = []
for image_file in os.listdir(slot_images_path):
    image_path = os.path.join(slot_images_path, image_file)
    curImg = cv2.imread(image_path)
    images.append(curImg)

# Get the face encodings for the images
def find_encodings(images_):
    encode_list = []
    for image in images_:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encoded_face = face_recognition.face_encodings(image)[0]
        encode_list.append(encoded_face)
    return encode_list

encoded_face_train = find_encodings(images)

# Mark attendance of students who appear on webcam
 # Mark attendance of students who appear on webcam
attendance_recorded = []
def mark_attendance(student_name, slot_name):
    global attendance_recorded
    with open(f'{slot_name}_Attendance.csv', 'a+') as f:
        my_data_list = f.readlines()
        name_list = []
        student_name = student_name.split('.')[0]
        reg_no = (student_name.split(', ')[1])
        student_name = student_name.split(', ')[0]
        for line in my_data_list:
            entry = line.split(',')
            if len(entry) >= 2:  # Check if the entry has at least two elements (name and registration number)
                name_list.append(entry[0])

        if student_name not in name_list and student_name not in attendance_recorded:
            now = datetime.now()
            time = now.strftime('%I:%M:%S %p')  # Correct the time format
            date = now.strftime('%d-%B-%Y')
            attendance_data = f"{student_name}, {reg_no}, {time}, {date}, {slot_name}\n"
            f.writelines(attendance_data)
            attendance_recorded.append(attendance_data.strip())  # Append to the list

# Function to display a message when attendance is marked successfully
def show_attendance_message(name):
    msg = f"Attendance marked for {name.split(',')[0]} ({name.split(',')[1]})"
    print(msg)
    cv2.putText(img, msg, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# take pictures from webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height
while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 1, 1)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    faces_in_frame = face_recognition.face_locations(imgS)
    encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)
    for encode_face, face_location in zip(encoded_faces, faces_in_frame):
        matches = face_recognition.compare_faces(encoded_face_train, encode_face)
        faceDist = face_recognition.face_distance(encoded_face_train, encode_face)
        matchIndex = np.argmin(faceDist)
        if matches[matchIndex]:
            name = classNames[matchIndex]
            y1, x2, y2, x1 = face_location  
            # since we scaled down by 4 times
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            mark_attendance(name, current_slot)
            show_attendance_message(name)

    cv2.putText(img, f"Attendance Slot: {current_slot}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('webcam', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()

# Export attendance data to a CSV file
def export_attendance_to_csv(slot_name):
    with open(f'{slot_name}_Attendance.csv', 'w') as f:
        now = datetime.now()
        date = now.strftime('%d-%B-%Y')
        f.writelines(f"Attendance Data for {slot_name} - {date}\n")
        f.writelines("Student Name, Registration Number, Time, Date, Slot\n")  # Write the header line
        for entry in attendance_recorded:
            student_name = entry.split(',')[0]
            reg_no = entry.split(', ')[1]
            time = entry.split(',')[2]
            f.writelines(f"{student_name}, {reg_no}, {time}, {date}, {slot_name}\n")

# Export attendance data to a CSV file at the end of the session
if len(attendance_recorded) > 0:
    export_attendance_to_csv(current_slot)
