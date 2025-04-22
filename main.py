from register_student import register_student
from attendance import check_attendance

def main():
    while True:
        print("\nSmart Attendance System")
        print("1. Register Student")
        print("2. Check Attendance")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            register_student()
        elif choice == "2":
            check_attendance()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
