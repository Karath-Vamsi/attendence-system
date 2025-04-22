import os
import cv2
from datetime import datetime

def register_student():
    student_name = input("Enter student name: ").strip()
    student_folder = os.path.join("known_faces", student_name)
    os.makedirs(student_folder, exist_ok=True)

    cap = cv2.VideoCapture(0)
    count = 0

    print("Press SPACE to take a photo. Press ESC to quit.")
    while True:
        ret, frame = cap.read()
        cv2.imshow("Register Student", frame)
        key = cv2.waitKey(1)

        if key == 27:  # ESC
            break
        elif key == 32:  # SPACEBAR
            img_path = os.path.join(student_folder, f"{student_name}_{count}.jpg")
            cv2.imwrite(img_path, frame)
            print(f"Saved {img_path}")
            count += 1

    cap.release()
    cv2.destroyAllWindows()
