from app.user import User


class TeacherUser(User):
    """Represents a teacher."""
    def __init__(self, user_id, name, speciality):
        super().__init__(user_id, name)
        self.speciality = speciality

    def to_dict(self):
        d = super().to_dict()
        d["speciality"] = self.speciality
        return d

    @classmethod
    def from_dict(cls, d):
        return cls(d["id"], d["name"], d["speciality"])


class Course:
    """Represents a single course offered by the school, linked to a teacher."""
    def __init__(self, course_id, name, instrument, teacher_id):
        self.id = course_id
        self.name = name
        self.instrument = instrument
        self.teacher_id = teacher_id
        self.enrolled_student_ids = []
        self.lessons = []  # lesson dicts: lesson_id, day, start_time, room

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "instrument": self.instrument,
            "teacher_id": self.teacher_id,
            "enrolled_student_ids": list(self.enrolled_student_ids),
            "lessons": [dict(l) for l in self.lessons],
        }

    @classmethod
    def from_dict(cls, d):
        c = cls(d["id"], d["name"], d["instrument"], d["teacher_id"])
        c.enrolled_student_ids = list(d.get("enrolled_student_ids", []))
        c.lessons = [dict(l) for l in d.get("lessons", [])]
        return c