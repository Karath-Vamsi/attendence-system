from register_student import register_student
from attendance import check_attendance, auto_mark_absentees
from utils import view_attendance_for_student

def main():
    auto_mark_absentees()

    while True:
        print("\nSmart Attendance System")
        print("1. Register Student")
        print("2. Mark Attendance")
        print("3. View Attendance")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            register_student()
        elif choice == "2":
            check_attendance()
        elif choice == "3":
            name = input("Enter student's name to view attendance: ").strip()
            view_attendance_for_student(name)
        elif choice == "4":
            print("Exiting the system.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
