# Music School Management System (MSMS)

A Streamlit app for managing students, teachers, courses, lessons and attendance at a music school. Data is stored in a local JSON file.

## Features

- **Dashboard**: totals for students, teachers and courses, today's check-ins, and today's lessons
- **Student Management**: search, register (instrument chosen from a dropdown), rename, enroll in or remove from courses, delete
- **Courses & Teachers**: add teachers and courses, schedule lessons with room and teacher clash detection
- **Daily Roster**: view lessons by weekday and check students in (duplicate check-ins for the same day are blocked)
- **Attendance History**: filter by student, course and date range, and download as CSV
- **Payments**: placeholder page (planned for PST5)

## Project structure

```
msms/
├── main.py                 # Entry point (run with Streamlit)
├── requirements.txt
├── app/                    # Business logic
│   ├── user.py             # Base User class
│   ├── student.py          # StudentUser
│   ├── teacher.py          # TeacherUser and Course
│   └── schedule.py         # ScheduleManager: loading, saving, all rules
├── gui/                    # Streamlit pages
│   ├── main_dashboard.py   # Navigation and dashboard
│   ├── student_pages.py
│   ├── course_pages.py
│   ├── roster_pages.py
│   ├── history_pages.py
│   └── common.py           # Shared success/error message helper
└── data/
    └── msms.json           # Saved data (updated automatically)
```

`app/` and `gui/` each need an `__init__.py` file (empty is fine).

## Requirements

- Python 3.8 or newer (a regular Windows/macOS/Linux install from python.org)
- `streamlit` and `pandas` (see `requirements.txt`)

> **MSYS2 users:** the MSYS2 Python blocks `pip install` (PEP 668) and often cannot build Streamlit's dependencies. Use a python.org install instead.

## Setup and run

Open a terminal in the folder that contains `main.py`.

**Windows (PowerShell)**

```powershell
py -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe -m streamlit run main.py
```


The app opens at <http://localhost:8501>. Stop it with `Ctrl+C`.

If PowerShell refuses to activate the environment, either call `venv\Scripts\python.exe` directly as above, or run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once.

## Data

All changes (students, courses, lessons, check-ins) are saved to `data/msms.json` straight away. Back this file up, or delete it to start fresh. The app handles a missing file by starting empty.

Format:

```json
{
  "students":   [{"id": 1, "name": "...", "enrolled_course_ids": [101]}],
  "teachers":   [{"id": 1, "name": "...", "speciality": "Piano"}],
  "courses":    [{"id": 101, "name": "...", "instrument": "Piano", "teacher_id": 1,
                  "enrolled_student_ids": [1],
                  "lessons": [{"lesson_id": 1, "day": "Monday", "start_time": "16:00", "room": "Room A"}]}],
  "attendance": [{"student_id": 1, "course_id": 101, "timestamp": "2025-07-14T15:58:30"}]
}
```

## How the rules work

- **Registration** needs a teacher whose speciality matches the chosen instrument. The student is enrolled in that teacher's first matching course (one is created if none exists).
- **Check-in** requires enrollment and allows one check-in per student per course per day.
- **Lesson clashes**: lessons are assumed to last 60 minutes (`LESSON_MINUTES` in `app/schedule.py`). A new lesson is rejected if its room is in use, or the course's teacher is already teaching, within that window on the same day.
- **Deleting a student** removes them from all courses but keeps their attendance records.

## Troubleshooting

| Problem | Fix |
|---|---|
| `No module named 'app'` | Run from the folder containing `main.py`; make sure `app/__init__.py` exists |
| `No module named streamlit` | Install into the same Python you run with, using `python -m pip install ...` |
| Pylance "import could not be resolved" | VS Code: *Python: Select Interpreter* and pick `venv` |
| Old pages still showing | Restart Streamlit; check files were replaced and there is no doubled `gui/gui/` folder |
| Empty dropdowns | `data/msms.json` is missing or in the wrong folder |

## Possible next steps

Payments tracking, late/on-time marking, attendance charts, login roles, unit tests.