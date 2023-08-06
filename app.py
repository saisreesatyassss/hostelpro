from flask import Flask, render_template, Response
import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
from flask import request, jsonify


app = Flask(__name__)

# Define the time slots for attendance
attendance_slots = {
    'A1': {'start_time': '19:50:00', 'end_time': '19:52:00'},
    'A2': {'start_time': '19:53:00', 'end_time': '19:54:00'},
    'B1': {'start_time': '22:24:00', 'end_time': '22:25:00'},
    'B2': {'start_time': '22:26:00', 'end_time': '22:27:00'},
    'C1': {'start_time': '22:28:00', 'end_time': '22:29:00'},
    'C2': {'start_time': '01:00:00', 'end_time': '05:00:00'}
}

# Global variables to store current slot and attendance data
current_slot = None
attendance_recorded = []

# Function to load images for the current attendance slot
def load_images_for_slot(slot):
    global attendance_recorded
    path = f'Student_Images/{slot}'
    if not os.path.exists(path):
        print(f'No images found for attendance slot {slot}')
        exit()

    images = []
    for image_file in os.listdir(path):
        image_path = os.path.join(path, image_file)
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

    global encoded_face_train
    encoded_face_train = find_encodings(images)

# Function to get the webcam stream
def generate_video():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route for the homepage
@app.route('/')
def index():
    global current_slot, attendance_recorded

    # Get the current time
    now = datetime.now()
    current_time = now.strftime('%H:%M:%S')

    # Check which time slot is currently active
    is_attendance_slot = False 
    for slot, times in attendance_slots.items():
        if current_time >= times['start_time'] and current_time <= times['end_time']:
            current_slot = slot
            load_images_for_slot(current_slot)
            is_attendance_slot = True 
            break

    if current_slot is None:
        current_slot_info = 'No attendance slot is currently active'
    else:
        current_slot_info = f"Attendance Slot: {current_slot}"

    return render_template('index.html', current_slot_info=current_slot_info, attendance_recorded=attendance_recorded, is_attendance_slot=is_attendance_slot)

# Route for video streaming
@app.route('/video_feed')
def video_feed():
    return Response(generate_video(), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/mark_attendance', methods=['POST'])

def mark_attendance_function(student_name, slot_name):
    # Replace this with your actual implementation to mark attendance
    # For example, you can store attendance in a database, log it to a file, etc.
    global attendance_recorded
    if student_name not in attendance_recorded:
        attendance_recorded.append(student_name)

# Route for marking attendance
@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    student_name = request.form.get('student_name')
    slot_name = request.form.get('slot_name')
    mark_attendance_function(student_name, slot_name)
    return jsonify({'status': 'success', 'message': f'Attendance marked for {student_name} in {slot_name}'})

        
if __name__ == '__main__':
    app.run(debug=True)
