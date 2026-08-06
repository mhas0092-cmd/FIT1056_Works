Name: Muhammad Hassan
Student ID: 37433972
Github Link: https://github.com/mhas0092-cmd/FIT1056_Works.git

Music School Management System (MSMS) – PST1

Overview

This project marks the first stage of the Music School Management System (MSMS) Project. It contains a simple, in-memory Console application with which we will implement basic functions such as register new student(s), enrol student(s) in instrument, search students/teachers, list all students/teachers etc.

All data used in this app is held in memory (in Python lists) and are therefore lost once you close this program. We will expand on our MSMS Project in future PSTs by implementing additional functionality including saving data files, using OOP designs, developing GUI’s and more importantly doing tests!

Features
Data Models

Student: ID, Name, List of enrolled instruments
Teacher: ID, Name, Speciality

Core Functions

add_teacher()
list_students()
list_teachers()
find_students() - search student with given name case-insensitively.
find_teachers() - search teacher with given name/speciality case-insensitively.

Front Desk Functions

front_desk_register(): Register a new student, and enroll them immediately.

front_desk_enrol():Enroll an existing student on an instrument.

front_desk_lookup():Search for both Students and Teachers.

Main Menu Options

Select one of these options from the main menu:
Register New Student
Enrol Existing Student
Lookup Student or Teacher
List all Students
List all Teachers
q. Quit
 
The two samples teachers listed below are automatically loaded when you start this program.
• Dr. Keys - Piano
• Ms. Fret - Guitar

Design Decisions & Assumptions

Starts with student/teacher ID of 1 and increments automatically.

Supports enrollment on multiple instruments per student.

Searches are case-insensitive with partial matches allowed.

Only stores data during runtime (intentionally designed for PST1).

Includes basic error-handling around invalid student IDs.

All code fits inside a single file called MSMS.py