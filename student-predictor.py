"""Student Performance Predictor (short beginner version)."""
import csv   # CSV file handling
import re    # regular expressions

# Module I: variables and data types
CSV_FILE = "students.csv"
PASS_MARKS = 40
FIELDS = ("name", "prn", "study_hours", "attendance", "previous_marks", "assignments")  # tuple

# Module II: lambda function (one-line function) to convert marks to grade
get_grade = lambda m: "A" if m >= 75 else "B" if m >= 60 else "C" if m >= PASS_MARKS else "F"


def predict_marks(study_hours, attendance, previous_marks, assignments):
    """Weighted formula; returns predicted marks (function with return value)."""
    marks = 0.45 * previous_marks + 0.20 * attendance + 0.20 * assignments + 1.9 * study_hours
    return round(min(marks, 100), 1)


# Module IV: classes and objects
class Student:
    def __init__(self, name, prn, study_hours, attendance, previous_marks, assignments):
        # Constructor: runs when an object is created
        self.name, self.prn = name, prn
        self.study_hours, self.attendance, self.assignments = study_hours, attendance, assignments
        # Encapsulation: __ makes the attribute private (use the getter to read it)
        self.__marks = predict_marks(study_hours, attendance, previous_marks, assignments)

    def __del__(self):
        pass  # Destructor: runs when the object is deleted ('pass' = do nothing)

    def get_marks(self):
        return self.__marks

    def get_status(self):
        return "Pass" if self.__marks >= PASS_MARKS else "Fail"

    def advice(self):
        return "Keep up the regular study routine."


class TopStudent(Student):  # Inheritance: gets everything from Student
    def advice(self):       # Polymorphism: same method name, different behaviour
        return "Excellent! Try advanced topics."


class AtRiskStudent(Student):
    def advice(self):
        tips = []
        if self.attendance < 75:
            tips.append("improve attendance")
        if self.study_hours < 2:
            tips.append("study 2+ hours daily")
        if self.assignments < 60:
            tips.append("submit assignments")
        return "Needs help: " + ", ".join(tips) if tips else "Revise basics regularly."


def create_student(data):
    """Picks the class based on predicted marks. *data unpacks the list."""
    marks = predict_marks(*data[2:])
    if marks >= 75:
        return TopStudent(*data)
    elif marks < PASS_MARKS + 15:
        return AtRiskStudent(*data)
    return Student(*data)


# Module IV: file handling and exception handling
def load_students():
    students = []
    try:
        with open(CSV_FILE, "r") as f:
            for row in csv.DictReader(f):
                try:
                    # Type conversion: CSV gives strings, we need numbers
                    nums = [float(row[k]) for k in FIELDS[2:]]
                    students.append(create_student([row["name"], row["prn"]] + nums))
                except (ValueError, KeyError):
                    print("Skipping a bad row.")
                    continue
    except FileNotFoundError:
        print("No CSV file found, starting empty.")
    return students


def save_report(students):
    with open("report.txt", "w") as f:  # text file
        f.write("STUDENT REPORT\n" + "=" * 30 + "\n")
        for s in students:
            f.write(f"{s.name} ({s.prn}): {s.get_marks()} - {s.get_status()}\n")
    print("Report saved to report.txt")


# Input helpers
def get_number(prompt, low, high):
    while True:  # keep asking until valid
        try:
            value = float(input(prompt))  # type conversion
            if low <= value <= high:
                break
            print(f"Enter a value between {low} and {high}.")
        except ValueError:  # exception handling
            print("Please enter a number.")
    return value


def get_text(prompt, pattern):
    while True:
        text = input(prompt).strip()  # string method
        if re.fullmatch(pattern, text):  # regex check
            return text.title()
        print("Invalid input, try again.")


# Menu options
def add_student(students):
    name = get_text("Name (letters only): ", r"[A-Za-z ]+")
    prn = get_text("PRN (6-12 digits): ", r"\d{6,12}")
    nums = [get_number("Study hours/day (0-12): ", 0, 12),
            get_number("Attendance % (0-100): ", 0, 100),
            get_number("Previous marks (0-100): ", 0, 100),
            get_number("Assignments % (0-100): ", 0, 100)]
    student = create_student([name, prn] + nums)
    students.append(student)
    with open(CSV_FILE, "a", newline="") as f:  # append to CSV
        csv.writer(f).writerow([name, prn] + nums)
    m = student.get_marks()
    print(f"Predicted: {m} | Grade: {get_grade(m)} | {student.get_status()}")
    print("Advice:", student.advice())


def view_students(students):
    for s in students:
        m = s.get_marks()
        print(f"{s.name:<16}{s.prn:<10}{m:<7}{get_grade(m):<4}{s.get_status():<6}{s.advice()}")


def show_summary(students):
    if not students:
        print("No data.")
        return
    marks = [s.get_marks() for s in students]  # list comprehension
    failing = [s.name for s in students if s.get_status() == "Fail"]
    grades = {}  # dictionary: grade -> count
    for m in marks:
        grades[get_grade(m)] = grades.get(get_grade(m), 0) + 1
    print(f"Students: {len(students)} | Average: {sum(marks) / len(marks):.1f}")
    print(f"Highest: {max(marks)} | Lowest: {min(marks)}")
    print(f"Likely to fail: {failing}")
    print(f"Grade count: {grades}")
    print(f"Unique results: {set(s.get_status() for s in students)}")  # set


def main():
    students = load_students()
    while True:
        print("\n1.Add student  2.View all  3.Summary  4.Save report  5.Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            show_summary(students)
        elif choice == "4":
            save_report(students)
        elif choice == "5":
            print("Goodbye!")
            break  # exit the loop
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
