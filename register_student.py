import os
import cv2
import shutil
import tkinter as tk
from tkinter import filedialog

def capture_images_via_webcam(student_dir):
    cap = cv2.VideoCapture(0)
    print("Press SPACE to capture a photo. Press ESC to finish.")
    count = 0

    while True:
        ret, frame = cap.read()
        cv2.imshow("Register Face", frame)
        key = cv2.waitKey(1)

        if key == 27:  # ESC
            break
        elif key == 32:  # SPACE
            img_path = os.path.join(student_dir, f"{student_name}_{count}.jpg")
            cv2.imwrite(img_path, frame)
            print(f"Saved {img_path}")
            count += 1

    cap.release()
    cv2.destroyAllWindows()

def upload_existing_images(student_dir):
    print("Please select image files from the file picker dialog.")
    
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    file_paths = filedialog.askopenfilenames(
        title="Select face images",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    
    for idx, path in enumerate(file_paths):
        ext = os.path.splitext(path)[1]
        dest = os.path.join(student_dir, f"{student_name}_{idx}{ext}")
        shutil.copy2(path, dest)
        print(f"Copied {path} -> {dest}")

def register_student():
    global student_name
    student_name = input("Enter student's name: ").strip()
    student_dir = os.path.join("known_faces", student_name)
    os.makedirs(student_dir, exist_ok=True)

    print("Choose method to register face:")
    print("1. Capture from webcam")
    print("2. Upload existing images")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        capture_images_via_webcam(student_dir)
    elif choice == "2":
        upload_existing_images(student_dir)
    else:
        print("Invalid choice.")
