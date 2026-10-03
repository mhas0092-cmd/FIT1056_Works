import json
from datetime import datetime
from pathlib import Path

from app.student import StudentUser
from app.teacher import TeacherUser, Course

DEFAULT_PATH = Path(__file__).resolve().parent.parent / "data" / "msms.json"
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
LESSON_MINUTES = 60  # assumed lesson length, used for clash detection


def _mins(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


class ScheduleManager:
    """The main controller for all business logic and data handling."""

    def __init__(self, data_path=DEFAULT_PATH):
        self.data_path = Path(data_path)
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance = []  # dicts: student_id, course_id, timestamp
        self.next_lesson_id = 1
        self._load_data()

    # ---------- persistence ----------
    def _load_data(self):
        try:
            with open(self.data_path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")
            return
        except json.JSONDecodeError:
            print("Data file is corrupted. Starting with a clean state.")
            return

        self.students = [StudentUser.from_dict(d) for d in data.get("students", [])]
        self.teachers = [TeacherUser.from_dict(d) for d in data.get("teachers", [])]
        self.courses = [Course.from_dict(d) for d in data.get("courses", [])]
        self.attendance = list(data.get("attendance", []))

        lesson_ids = [l["lesson_id"] for c in self.courses for l in c.lessons]
        self.next_lesson_id = max(lesson_ids, default=0) + 1

    def _save_data(self):
        data_to_save = {
            "students": [s.to_dict() for s in self.students],
            "teachers": [t.to_dict() for t in self.teachers],
            "courses": [c.to_dict() for c in self.courses],
            "attendance": self.attendance,
        }
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_path, "w") as f:
            json.dump(data_to_save, f, indent=4)

    # ---------- lookups ----------
    def get_student(self, student_id):
        return next((s for s in self.students if s.id == student_id), None)

    def get_teacher(self, teacher_id):
        return next((t for t in self.teachers if t.id == teacher_id), None)

    def get_course(self, course_id):
        return next((c for c in self.courses if c.id == course_id), None)

    def search_students(self, query):
        q = query.strip().lower()
        return [s for s in self.students if q in s.name.lower()]

    # ---------- actions ----------
    def register_new_student(self, name, instrument):
        """Creates a student and enrolls them in the first course for the
        instrument. Returns the student, or None if no teacher is available."""
        name, instrument = name.strip(), instrument.strip()
        if not name or not instrument:
            return None
        teacher = next((t for t in self.teachers
                        if t.speciality.lower() == instrument.lower()), None)
        if teacher is None:
            print(f"No teacher available for {instrument}.")
            return None

        student = StudentUser(max((s.id for s in self.students), default=0) + 1, name)
        self.students.append(student)

        course = next((c for c in self.courses
                       if c.instrument.lower() == instrument.lower()
                       and c.teacher_id == teacher.id), None)
        if course is None:  # create a default course for this instrument
            course = Course(max((c.id for c in self.courses), default=100) + 1,
                            f"Beginner {teacher.speciality}",
                            teacher.speciality, teacher.id)
            self.courses.append(course)
        course.enrolled_student_ids.append(student.id)
        student.enrolled_course_ids.append(course.id)

        self._save_data()
        return student

    def check_in(self, student_id, course_id):
        """Records attendance. Returns (ok, message)."""
        student, course = self.get_student(student_id), self.get_course(course_id)
        if not student or not course:
            return False, "Unknown student or course."
        if course_id not in student.enrolled_course_ids:
            return False, f"{student.name} is not enrolled in {course.name}."
        today = datetime.now().date().isoformat()
        if any(a["student_id"] == student_id and a["course_id"] == course_id
               and a["timestamp"].startswith(today) for a in self.attendance):
            return False, f"{student.name} is already checked in for {course.name} today."
        self.attendance.append({"student_id": student_id, "course_id": course_id,
                                "timestamp": datetime.now().isoformat()})
        self._save_data()
        return True, f"Checked in {student.name} for {course.name}."

    def instruments(self):
        return sorted({t.speciality for t in self.teachers})

    def enroll(self, student_id, course_id):
        s, c = self.get_student(student_id), self.get_course(course_id)
        if not s or not c:
            return False, "Unknown student or course."
        if course_id in s.enrolled_course_ids:
            return False, f"{s.name} is already in {c.name}."
        s.enrolled_course_ids.append(course_id)
        c.enrolled_student_ids.append(student_id)
        self._save_data()
        return True, f"Enrolled {s.name} in {c.name}."

    def unenroll(self, student_id, course_id):
        s, c = self.get_student(student_id), self.get_course(course_id)
        if not s or not c or course_id not in s.enrolled_course_ids:
            return False, "Student is not enrolled in that course."
        s.enrolled_course_ids.remove(course_id)
        c.enrolled_student_ids.remove(student_id)
        self._save_data()
        return True, f"Removed {s.name} from {c.name}."

    def rename_student(self, student_id, new_name):
        s = self.get_student(student_id)
        if not s or not new_name.strip():
            return False, "Please enter a valid name."
        s.name = new_name.strip()
        self._save_data()
        return True, "Student renamed."

    def delete_student(self, student_id):
        s = self.get_student(student_id)
        if not s:
            return False, "Unknown student."
        for c in self.courses:
            if student_id in c.enrolled_student_ids:
                c.enrolled_student_ids.remove(student_id)
        self.students.remove(s)  # attendance history is kept
        self._save_data()
        return True, f"Deleted {s.name}."

    def add_teacher(self, name, speciality):
        name, speciality = name.strip(), speciality.strip()
        if not name or not speciality:
            return False, "Enter both a name and a speciality."
        tid = max((t.id for t in self.teachers), default=0) + 1
        self.teachers.append(TeacherUser(tid, name, speciality))
        self._save_data()
        return True, f"Added teacher {name}."

    def add_course(self, name, teacher_id):
        t = self.get_teacher(teacher_id)
        if not name.strip() or not t:
            return False, "Enter a course name and choose a teacher."
        cid = max((c.id for c in self.courses), default=100) + 1
        self.courses.append(Course(cid, name.strip(), t.speciality, t.id))
        self._save_data()
        return True, f"Added course {name.strip()}."

    def find_lesson_clash(self, course_id, day, start_time, room):
        """Returns a clash description, or None if the slot is free."""
        course = self.get_course(course_id)
        start = _mins(start_time)
        for c in self.courses:
            for l in c.lessons:
                if l["day"] != day or abs(_mins(l["start_time"]) - start) >= LESSON_MINUTES:
                    continue
                if l["room"].strip().lower() == room.strip().lower():
                    return f"{room} is already used by {c.name} at {l['start_time']}."
                if c.teacher_id == course.teacher_id:
                    t = self.get_teacher(c.teacher_id)
                    return f"{t.name} already teaches {c.name} at {l['start_time']}."
        return None

    def add_lesson(self, course_id, day, start_time, room):
        c = self.get_course(course_id)
        if not c or not room.strip():
            return False, "Choose a course and enter a room."
        clash = self.find_lesson_clash(course_id, day, start_time, room)
        if clash:
            return False, "Clash: " + clash
        c.lessons.append({"lesson_id": self.next_lesson_id, "day": day,
                          "start_time": start_time, "room": room.strip()})
        self.next_lesson_id += 1
        self._save_data()
        return True, f"Added {day} {start_time} lesson to {c.name}."

    def remove_lesson(self, course_id, lesson_id):
        c = self.get_course(course_id)
        if not c:
            return False, "Unknown course."
        c.lessons = [l for l in c.lessons if l["lesson_id"] != lesson_id]
        self._save_data()
        return True, "Lesson removed."

    def get_attendance_rows(self):
        rows = []
        for a in self.attendance:
            s, c = self.get_student(a["student_id"]), self.get_course(a["course_id"])
            rows.append({"Timestamp": a["timestamp"],
                         "Date": a["timestamp"][:10],
                         "Student": s.name if s else f"#{a['student_id']} (deleted)",
                         "Course": c.name if c else f"#{a['course_id']}"})
        return sorted(rows, key=lambda r: r["Timestamp"], reverse=True)

    # ---------- reporting ----------
    def get_roster(self, day):
        """Returns a list of row dicts for all lessons on the given day."""
        today = datetime.now().date().isoformat()
        rows = []
        for c in self.courses:
            teacher = self.get_teacher(c.teacher_id)
            for l in c.lessons:
                if l["day"] != day:
                    continue
                for sid in c.enrolled_student_ids:
                    s = self.get_student(sid)
                    checked = any(a["student_id"] == sid and a["course_id"] == c.id
                                  and a["timestamp"].startswith(today)
                                  for a in self.attendance)
                    rows.append({
                        "Time": l["start_time"],
                        "Room": l["room"],
                        "Course": c.name,
                        "Teacher": teacher.name if teacher else "Unassigned",
                        "Student": s.name if s else f"#{sid}",
                        "Checked in today": "Yes" if checked else "No",
                    })
        return sorted(rows, key=lambda r: (r["Time"], r["Room"], r["Student"]))