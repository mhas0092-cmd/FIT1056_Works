Name: Muhammad Hassan

Student ID: 37433972

Github Link: https://github.com/mhas0092-cmd/FIT1056_Works.git

Music School Management System (MSMS) – PST2

Overview:

This project is the second stage of the Music School Management System (MSMS) Project. It upgrades the simple in-memory console application from PST1 into a persistent application. All data is now saved to and loaded from a single structured JSON file (msms.json), so information is no longer lost when the program is closed.

In this stage we also added full Create, Read, Update and Delete (CRUD) operations and new receptionist features such as student check-in and printing student ID cards.

Features

Data Structure:

All data is stored in a global dictionary called app_data with the following keys:
students (list of dictionaries)
teachers (list of dictionaries)
attendance (list of check-in records)
next_student_id
next_teacher_id

Core Persistence Functions:

load_data() – Loads data from msms.json (or creates a default empty structure if the file does not exist)
save_data() – Saves the current state of app_data to msms.json in a readable format

CRUD Functions:

add_teacher() – Adds a new teacher
update_teacher() – Updates a teacher’s details by ID
remove_teacher() – Removes a teacher by ID
update_student() – Updates a student’s details by ID
remove_student() – Removes a student by ID

Receptionist Features:

check_in() – Records a student’s attendance for a course with a timestamp
print_student_card() – Creates a text file badge for a student

Main Menu Options:

1. Check-in Student
2. Print Student Card
3. Update Teacher Info
4. Remove Student
q. Quit and Save

Design Decisions & Assumptions:

Data is stored as plain dictionaries instead of class objects (OOP will be introduced in PST3)
Student and teacher IDs start at 1 and auto-increment
Attendance records store student_id, course_id and an ISO timestamp
Student cards are saved as simple text files named {id}_card.txt
The program automatically saves data after every change and also on exit
Basic input validation is included for student and teacher IDs
All code for this stage is contained in a single file called pst2_main.py