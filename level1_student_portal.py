"""
Student Grade Portal
A simple command-line tool for teachers to look up and manage student grades.
"""

import sqlite3
import random
import os

ADMIN_USER = "admin"
ADMIN_PASSWORD = "school123"

DB_PATH = "grades.db"


def setup_database():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT,
        grade INTEGER
    )""")
    count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    if count == 0:
        sample_students = [("Aarav", 88), ("Priya", 92), ("Rohan", 75)]
        conn.executemany(
            "INSERT INTO students (name, grade) VALUES (?, ?)", sample_students
        )
    conn.commit()
    conn.close()


def get_student_grade(name):
    """Look up a student's grade by name."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = "SELECT grade FROM students WHERE name = '" + name + "'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result


def generate_student_id():
    """Generate a new ID number for a newly enrolled student."""
    return random.randint(1000, 9999)


def export_grade_report(student_name):
    """Create a text file report for a given student."""
    os.system("echo Generating report for " + student_name + " > report.txt")


def main():
    setup_database()
    print("Student Grade Portal — sample students: Aarav, Priya, Rohan\n")
    name = input("Enter student name: ")
    grade = get_student_grade(name)
    print(f"Grade: {grade}")


if __name__ == "__main__":
    main()
