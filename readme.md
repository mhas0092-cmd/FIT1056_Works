MSMS — Music School Management System

A simple, object-oriented command-line application for managing a music school's students, teachers, courses, and daily attendance.

Features

Daily Roster: View a formatted table of every lesson scheduled on a given day, including course, instrument, time, and teacher.

Student Check-in: Record a student's attendance for a course, with validation of both student and course IDs.

Switch Student Course: Move a student from one enrolled course to another in a single, validated operation.

Persistent Storage: All data (students, teachers, courses, and attendance) is loaded from and saved to a JSON file, so state survives between runs.

Usage

On launch, you'll see a menu:

```
===== MSMS v3 (Object-Oriented) =====
1. Daily Roster
2. Student Check-in
3. Switch Student Course
q. Quit
Enter choice:
```

1. Daily Roster
Enter a day of the week (e.g., `Monday`). The app displays every lesson scheduled
that day in a table with course name, instrument, time, and teacher ID.

2. Student Check-in
Enter a **Student ID** and **Course ID** (both positive integers). The app validates
that both exist, then logs a timestamped attendance record. If the student isn't
currently enrolled in that course, a warning is shown but check-in still proceeds.

3. Switch Student Course
Enter a Student ID, the From Course ID, and the To Course ID. The app
validates that:
The student exists.
Both courses exist.
The student is currently enrolled in the "from" course.
The "from" and "to" courses aren't the same.

If all checks pass, the student is unenrolled from the old course and enrolled in
the new one.

Quit
Enter `q` at any time from the main menu to exit.

Input Validation

The CLI includes helper prompts (`get_positive_int`, `get_valid_day`) that:
Reject empty input and re-prompt (with a cancel-on-double-empty escape hatch).
Reject non-numeric or non-positive values for IDs.
Restrict day input to valid weekday names, case-insensitive.