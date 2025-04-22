import os
import cv2
import pandas as pd
from datetime import datetime
from deepface import DeepFace
import time

LOG_DIR = "logs"
KNOWN_FACES_DIR = "known_faces"
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)

def get_known_faces():
    known_faces = []
    for student in os.listdir(KNOWN_FACES_DIR):
        student_folder = os.path.join(KNOWN_FACES_DIR, student)
        if os.path.isdir(student_folder):
            for img in os.listdir(student_folder):
                img_path = os.path.join(student_folder, img)
                known_faces.append((student, img_path))
    return known_faces

def get_current_hour_slot():
    now = datetime.now()
    hour = now.hour
    if 9 <= hour <= 21:
        return f"{hour}AM" if hour < 12 else f"{hour-12 if hour > 12 else 12}PM"
    return None

def is_within_first_30_minutes():
    return datetime.now().minute < 30

def load_attendance_csv():
    date_str = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join(LOG_DIR, f"attendance_{date_str}.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
    else:
        hours = [f"{h}AM" if h < 12 else f"{h-12 if h > 12 else 12}PM" for h in range(9, 22)]
        df = pd.DataFrame(columns=["Name", "Date"] + hours)
    return df, path

def save_attendance(name):
    now = datetime.now()
    hour_col = get_current_hour_slot()
    if not hour_col:
        print("Outside class hours (9AM–9PM).")
        return

    if not is_within_first_30_minutes():
        print(f"{name} was late for the {hour_col} class. Attendance not logged.")
        return

    df, path = load_attendance_csv()
    today = now.strftime("%Y-%m-%d")

    if name not in df["Name"].values:
        new_row = {"Name": name, "Date": today, hour_col: "Present"}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        idx = df.index[df["Name"] == name][0]
        if pd.isna(df.at[idx, hour_col]):
            df.at[idx, hour_col] = "Present"

    df.to_csv(path, index=False)
    print(f"Attendance for {name} recorded at {now.strftime('%H:%M:%S')}.")

def save_new_face(face_image, student_name):
    student_folder = os.path.join(KNOWN_FACES_DIR, student_name)
    os.makedirs(student_folder, exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    new_image_path = os.path.join(student_folder, f"{student_name}_{timestamp}.jpg")
    cv2.imwrite(new_image_path, face_image)
    print(f"Saved new face image for {student_name} at {new_image_path}.")
    
def check_attendance():
    print("Press SPACE to take attendance photo. ESC to exit.")
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        cv2.imshow("Check Attendance", frame)
        key = cv2.waitKey(1)

        if key == 27:  # ESC
            break
        elif key == 32:  # SPACE
            try:
                captured_path = "temp.jpg"
                cv2.imwrite(captured_path, frame)

                known_faces = get_known_faces()
                found = False
                for name, path in known_faces:
                    result = DeepFace.verify(captured_path, path, enforce_detection=False)
                    if result["verified"]:
                        save_attendance(name)
                        found = True
                        break

                if not found:
                    print("Face not recognized.")
                    student_name = input("Enter your name: ")

                    # Save the new face
                    save_new_face(frame, student_name)

                    # Log the attendance after saving the new face
                    save_attendance(student_name)
                    
            except Exception as e:
                print("Error:", e)
            finally:
                if os.path.exists(captured_path):
                    os.remove(captured_path)

    cap.release()
    cv2.destroyAllWindows()

