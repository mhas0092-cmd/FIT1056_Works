import json
import datetime
from app.student import StudentUser
from app.teacher import TeacherUser, Course


class ScheduleManager:
    """The main controller for all business logic and data handling."""

    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        self.attendance_log = []
        self._next_student_id = 1
        self._next_teacher_id = 1
        self._next_course_id = 1
        self._load_data()

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, "r") as f:
                data = json.load(f)

            # Reconstruct students
            self.students = []
            for s in data.get("students", []):
                student = StudentUser(s["id"], s["name"])
                student.enrolled_course_ids = s.get("enrolled_course_ids", [])
                self.students.append(student)

            # Reconstruct teachers
            self.teachers = []
            for t in data.get("teachers", []):
                teacher = TeacherUser(t["id"], t["name"], t.get("speciality", ""))
                self.teachers.append(teacher)

            # Reconstruct courses
            self.courses = []
            for c in data.get("courses", []):
                course = Course(
                    c["id"],
                    c["name"],
                    c.get("instrument", ""),
                    c.get("teacher_id")
                )
                course.enrolled_student_ids = c.get("enrolled_student_ids", [])
                course.lessons = c.get("lessons", [])
                self.courses.append(course)

            # Attendance log
            self.attendance_log = data.get("attendance", [])

            # Restore ID counters
            self._next_student_id = data.get("next_student_id", 1)
            self._next_teacher_id = data.get("next_teacher_id", 1)
            self._next_course_id = data.get("next_course_id", 1)

        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")
            self.students = []
            self.teachers = []
            self.courses = []
            self.attendance_log = []

    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        data_to_save = {
            "students": [s.__dict__ for s in self.students],
            "teachers": [t.__dict__ for t in self.teachers],
            "courses": [c.__dict__ for c in self.courses],
            "attendance": self.attendance_log,
            "next_student_id": self._next_student_id,
            "next_teacher_id": self._next_teacher_id,
            "next_course_id": self._next_course_id,
        }
        with open(self.data_path, "w") as f:
            json.dump(data_to_save, f, indent=4)

    # ---------- Helper lookup methods ----------
    def find_student_by_id(self, student_id):
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    def find_course_by_id(self, course_id):
        for course in self.courses:
            if course.id == course_id:
                return course
        return None

    def find_teacher_by_id(self, teacher_id):
        for teacher in self.teachers:
            if teacher.id == teacher_id:
                return teacher
        return None

    # ---------- Attendance ----------
    def check_in(self, student_id, course_id):
        """Records a student's attendance for a course after validation."""
        if not isinstance(student_id, int) or student_id <= 0:
            print("Error: Check-in failed. Student ID must be a positive integer.")
            return False
        if not isinstance(course_id, int) or course_id <= 0:
            print("Error: Check-in failed. Course ID must be a positive integer.")
            return False

        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)

        if not student:
            print(f"Error: Check-in failed. Student ID {student_id} not found.")
            return False
        if not course:
            print(f"Error: Check-in failed. Course ID {course_id} not found.")
            return False

        if course_id not in student.enrolled_course_ids:
            print(f"Warning: Student {student.name} is not currently enrolled in {course.name}.")

        timestamp = datetime.datetime.now().isoformat()
        check_in_record = {
            "student_id": student_id,
            "course_id": course_id,
            "timestamp": timestamp,
        }
        self.attendance_log.append(check_in_record)
        self._save_data()
        print(f"Success: Student {student.name} checked into {course.name}.")
        return True

    # ---------- Daily roster ----------
    def get_lessons_for_day(self, day):
        """Return a list of (course, lesson) pairs that occur on the given day."""
        results = []
        for course in self.courses:
            for lesson in course.lessons:
                if lesson.get("day", "").lower() == day.lower():
                    results.append((course, lesson))
        return results

    # ---------- Enrolment helpers ----------
    def enrol_student(self, student_id, course_id):
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)
        if not student or not course:
            return False
        if course_id not in student.enrolled_course_ids:
            student.enrolled_course_ids.append(course_id)
        if student_id not in course.enrolled_student_ids:
            course.enrolled_student_ids.append(student_id)
        self._save_data()
        return True

    def unenrol_student(self, student_id, course_id):
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)
        if not student or not course:
            return False
        if course_id in student.enrolled_course_ids:
            student.enrolled_course_ids.remove(course_id)
        if student_id in course.enrolled_student_ids:
            course.enrolled_student_ids.remove(student_id)
        self._save_data()
        return True

    def switch_student_course(self, student_id, from_course_id, to_course_id):
        """Move a student from one course to another."""
        if from_course_id == to_course_id:
            return False
        student = self.find_student_by_id(student_id)
        if not student:
            return False
        if from_course_id not in student.enrolled_course_ids:
            return False
        if not self.find_course_by_id(to_course_id):
            return False
        if not self.unenrol_student(student_id, from_course_id):
            return False
        return self.enrol_student(student_id, to_course_id)