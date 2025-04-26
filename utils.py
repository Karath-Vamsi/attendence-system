import pandas as pd
from datetime import datetime
import os

LOG_DIR = "logs"

def view_attendance_for_student(name):
    date_str = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join(LOG_DIR, f"attendance_{date_str}.csv")

    if not os.path.exists(path):
        print(f"No attendance data found for {date_str}.")
        return

    df = pd.read_csv(path)

    student_row = df[df["Name"].str.lower() == name.lower()]
    if student_row.empty:
        print(f"No attendance found for '{name}' on {date_str}.")
        return

    print(f"\n Attendance for {name} on {date_str}:")
    for col in df.columns[2:]:
        status = student_row.iloc[0][col]
        print(f"  {col}: {status if pd.notna(status) else 'Absent'}")

def auto_mark_absentees():
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    flag_file = os.path.join("logs", f".absentees_marked_{today_str}.flag")

    if now.hour >= 18:
        if not os.path.exists(flag_file):
            print("Marking absentees now...")
            mark_absentees()
            with open(flag_file, "w") as f:
                f.write("done")
            print("Absentees marked successfully!")
        else:
            print("Absentees already marked for today.")
